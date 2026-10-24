import json
import os
import sys
from pathlib import Path

from llama_index.llms.ollama import Ollama
from tqdm import tqdm

from src.components.prompts import PROMPT, REASONING_INSTRUCTION
from src.components.retrieval import Retrieval
from src.entity.config_entity import GenerationConfig
from src.exception import CustomException
from src.logger import logging
from src.utils import save_json


class Generator:
    def __init__(self, config: GenerationConfig, retriever: Retrieval):
        self.generation_config = config
        self.retriever = retriever

    def _extract_answer(self, raw: str) -> str:
        return raw.split("Answer:", 1)[1].strip() if "Answer:" in raw else raw.strip()

    def initiate_generation(self):
        logging.info("Preparing llm model and prompt setup for generation")
        try:
            self.llm = Ollama(
                model = self.generation_config.llm_model_name,
                request_timeout = self.generation_config.request_timeout,
                temperature = self.generation_config.temperature
            )

            self.prompt_template = PROMPT
        except Exception as e:
            raise CustomException(e, sys)

    def generate(self, question: str, title: str) -> dict:
        logging.info("generating reponse...")
        retrieved_chunks = self.retriever.retrieve(question, title)
        prompt = self.prompt_template.format(context_str="\n\n".join(retrieved_chunks), query_str=question)

        if self.generation_config.use_reasoning:
            idx = prompt.rfind("Answer:")
            prompt = prompt[:idx] + REASONING_INSTRUCTION

        raw = str(self.llm.complete(prompt))
        answer = self._extract_answer(raw)
        return {"answer": answer, "contexts": retrieved_chunks}

    def run_batch(self, items: list[dict], output_path: Path) -> list[dict]:
        if os.path.exists(output_path):
            with open(output_path) as f:
                results = json.load(f)
            done = {(r["title"], r["question"]) for r in results}
        else:
            results, done = [], set()

        remaining = [r for r in items if (r["title"], r["question"]) not in done]
        logging.info(f"Batch processing: {len(results)} already done, {len(remaining)} remaining to process")

        for item in tqdm(remaining):
            try:
                output = self.generate(item["question"], item["title"])
            except Exception as e:
                output = {"answer": f"[ERROR: {type(e).__name__}: {e}]", "contexts": []}

            results.append({**item, "answer": output["answer"], "contexts": output["contexts"]})
            save_json(output_path, results)

        return results


        


        