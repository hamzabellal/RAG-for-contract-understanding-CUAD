import sys
import os
import json
import pandas as pd
import mlflow
from mlflow import MlflowClient
from dotenv import load_dotenv
from collections import Counter
from langchain_anthropic import ChatAnthropic
from llama_index.embeddings.ollama import OllamaEmbedding
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall, answer_correctness
from ragas.run_config import RunConfig
from ragas.evaluation import evaluate, EvaluationDataset

from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import EvaluationConfig
from src.components.generation import Generator
from src.utils import save_json, clean_content, extract_category
from src.config.configuration import ConfigurationManager

class ChatAnthropicNoTemp(ChatAnthropic):
    def __setattr__(self, name, value):
        if name == "temperature":
            return
        super().__setattr__(name, value)


class Evaluator:
    def __init__(self, config: EvaluationConfig, generator: Generator = None):
        self.evaluation_config = config
        self.generator = generator

    def classify(self, answer: str) -> str:
        if answer.startswith("[ERROR"):
            return "error"
        answer_lower = answer.lower()
        if any(phrase in answer_lower for phrase in self.evaluation_config.absence_phrases):
            return "true negative"
        return "false positive"

    def stratified_samples(self, pool: pd.DataFrame, n_samples: int) -> pd.DataFrame:
        groups = [
            group.sample(min(len(group), n_samples), random_state=42)
            for _, group in pool.groupby("category")
        ]
        return pd.concat(groups, ignore_index=True)


    def build_eval_samples(self) -> tuple[list[dict], list[dict]]:
        logging.info("building evaluation samples...")
        try:
            pos_path = self.evaluation_config.positive_samples_path
            neg_path = self.evaluation_config.negative_samples_path

            if os.path.exists(pos_path) and os.path.exists(neg_path):
                with open(pos_path) as f:
                    positive_samples = json.load(f)
                with open(neg_path) as f:
                    negative_samples = json.load(f)
                logging.info(f"loaded existing evaluation samples : {len(positive_samples)} positive, {len(negative_samples)} negative")
                return positive_samples, negative_samples

            df = pd.read_json(self.evaluation_config.full_data_path, lines=True, compression="gzip")
            df["category"] = df["question"].apply(extract_category)
            df["answer_text"] = df["answers"].apply(lambda x: x["text"])

            grouped = (df.groupby(["title", "question", "category"])["answer_text"].apply(
                lambda lists: [item for sublist in lists for item in sublist]
            ).reset_index())

            positive_pool = grouped[grouped["answer_text"].str.len() > 0]
            negative_pool = grouped[grouped["answer_text"].str.len() == 0]

            positive_df = self.stratified_samples(positive_pool, self.evaluation_config.n_per_category_positive)
            negative_df = self.stratified_samples(negative_pool, self.evaluation_config.n_per_category_negative)

            positive_df["clean_answer_text"] = positive_df["answer_text"].apply(lambda x: [clean_content(ans) for ans in x])

            positive_samples = [
                {
                    "title": row["title"],
                    "question": row["question"],
                    "category": row["category"],
                    "ground_truth": " ".join(row["clean_answer_text"])
                }
                for _, row in positive_df.iterrows()
            ]
            negative_samples = [
                {
                    "title": row["title"],
                    "question": row["question"],
                    "category": row["category"]
                }
                for _, row in negative_df.iterrows()
            ]
            save_json(pos_path, positive_samples)
            save_json(neg_path, negative_samples)
            logging.info(f"evaluation samples built and saved : {len(positive_samples)} positive, {len(negative_samples)} negative")
            return positive_samples, negative_samples
        
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_evaluation(self):
        logging.info("preparing ragas judge")
        try:
            load_dotenv(override=True)

            claude_llm = ChatAnthropicNoTemp(model=self.evaluation_config.judge_model_name, max_tokens=4096)
            self.ragas_llm = LangchainLLMWrapper(claude_llm)

            judge_embed_model = OllamaEmbedding(model_name=self.evaluation_config.judge_embeddings_model_name)
            self.ragas_embeddings = LlamaIndexEmbeddingsWrapper(judge_embed_model)

            self.metrics = [faithfulness, answer_relevancy, context_precision, context_recall, answer_correctness]
            self.run_config = RunConfig(
                timeout = 180,
                max_workers = 4
            )

            logging.info("ragas judge ready")
        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluate_positive(self, results: list[dict]):
        logging.info("starting ragas evaluation")
        try:
            clean_results = [r for r in results if not r["answer"].startswith("[ERROR")]
            logging.info(f"{len(clean_results)} usable after removing errors({len(results) - len(clean_results)} errors)")

            output_path = self.evaluation_config.ragas_scores_path
            if os.path.exists(output_path):
                with open(output_path) as f:
                    existing_scores = json.load(f)
            else:
                existing_scores = []

            BATCH_SIZE = self.evaluation_config.batch_size
            start_index = len(existing_scores)
            n_batches = (len(clean_results) - 1) // BATCH_SIZE + 1 if clean_results else 0

            for i in range(start_index, len(clean_results), BATCH_SIZE):
                batch = clean_results[i:i + BATCH_SIZE]
                eval_batch = [
                    {
                        "user_input": r["question"],
                        "response": r["answer"],
                        "retrieved_contexts": r["contexts"],
                        "reference": r["ground_truth"]
                    }
                    for r in batch
                ]
                batch_dataset = EvaluationDataset.from_list(eval_batch)
                logging.info(f"ragas batch {i // BATCH_SIZE + 1}/{n_batches} ({len(batch)} examples)...")

                rs = evaluate(
                    dataset = batch_dataset,
                    llm = self.ragas_llm,
                    embeddings = self.ragas_embeddings,
                    metrics = self.metrics,
                    run_config = self.run_config
                )
                batch_scores = rs.to_pandas().to_dict(orient="records")

                for meta, scores in zip(batch, batch_scores):
                    existing_scores.append({"title": meta["title"], "category": meta["category"], **scores})

                save_json(output_path, existing_scores)

                df_partial = pd.DataFrame(existing_scores)
                for col in ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "answer_correctness"]:
                    mlflow.log_metric(col, df_partial[col].mean(), step=i)

            df_scores = pd.DataFrame(existing_scores)
            metric_cols = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "answer_correctness"]
            summary_global = df_scores[metric_cols].mean().to_dict()
            summary_by_category = df_scores.groupby("category")[metric_cols].mean().reset_index().to_dict(orient="records")

            save_json(self.evaluation_config.summary_global_path, summary_global)
            save_json(self.evaluation_config.summary_by_category_path, summary_by_category)
            logging.info(f"ragas evaluation completed and saved at {output_path}")

            return df_scores, summary_global, summary_by_category
        
        except Exception as e:
            raise CustomException(e, sys)

    def evaluate_negative(self, results: list[dict]):
        
        classifications = [self.classify(r["answer"]) for r in results]
        counts = Counter(classifications)
        total_classifiable = counts["true negative"] + counts["false positive"]
        fp_rate = counts["false positive"] / total_classifiable if total_classifiable else 0.0

        report = {
            "true_negative" : counts["true negative"],
            "false_positive" : counts["false positive"],
            "error" : counts.get("error", 0),
            "false_positive_rate" : fp_rate
        }
        logging.info(f"false positive rate : {fp_rate:.4f} ({counts['false positive']}/{total_classifiable})")
        save_json(self.evaluation_config.negative_report_path, report)
        logging.info(f"negative samples evaluation are saved at {self.evaluation_config.negative_report_path}")
        return report

    def run(self) -> dict:
        mlflow.set_tracking_uri(self.evaluation_config.mlflow_tracking_uri)
        
        try:
            client = MlflowClient()
            client.search_experiments(max_results=1)
        except Exception as e:
            raise CustomException(e, sys)

        mlflow.set_experiment(self.evaluation_config.mlflow_experiment_name)

        run_id_path = self.evaluation_config.mlflow_run_id_path
        resumed = False

        if os.path.exists(run_id_path):
            with open(run_id_path) as f:
                run_id = json.load(f)["run_id"]
            try:
                mlflow.start_run(run_id=run_id)
                resumed = True
                logging.info(f"resuming mlflow run {run_id}")
            except Exception:
                logging.info(f"could not resume mlflow run {run_id}, start a new one")

        if not resumed:
            active_run = mlflow.start_run()
            run_id = active_run.info.run_id
            save_json(run_id_path, {"run_id": run_id})
            logging.info(f"started new mlflow run {run_id}")


        config_manager = ConfigurationManager()

        def prefixed(prefix, config_obj):
            return {f"{prefix}.{k}": v for k, v in vars(config_obj).items()}

        params = {}

        params.update(prefixed("chunking", config_manager.get_chunking_config()))
        params.update(prefixed("embedding", config_manager.get_embedding_config()))
        params.update(prefixed("retrieval", config_manager.get_retrieval_config()))
        params.update(prefixed("generation", config_manager.get_generation_config()))
        params.update(prefixed("evaluation", config_manager.get_evaluation_config()))
        mlflow.log_params(params)
        
        positive_samples, negative_samples = self.build_eval_samples()

        positive_results = self.generator.run_batch(positive_samples, self.evaluation_config.positive_results_path)
        negative_results = self.generator.run_batch(negative_samples, self.evaluation_config.negative_results_path)

        self.initiate_evaluation()
        _, summary_global, _ = self.evaluate_positive(positive_results)
        negative_report = self.evaluate_negative(negative_results)

        for metric_name, value in summary_global.items():
            mlflow.log_metric(metric_name, value)
        mlflow.log_metric("false_positive_rate", negative_report["false_positive_rate"])

        mlflow.log_artifact(self.evaluation_config.summary_by_category_path)
        mlflow.log_artifact(self.evaluation_config.ragas_scores_path)

        mlflow.end_run()

        report = {
            "positive": summary_global,
            "negative": negative_report
        }
        logging.info(f"evaluation completed. Summary: {report}")
        return report
