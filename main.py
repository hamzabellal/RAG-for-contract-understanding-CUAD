import argparse
import sys

from src.config.configuration import ConfigurationManager
from src.exception import CustomException
from src.logger import logging
from src.pipeline.chunking import ChunkingPipeline
from src.pipeline.data_ingestion import DataIngestionPipeline
from src.pipeline.embedding_indexing import EmbeddingIndexingPipeline
from src.pipeline.eval_samples import EvalSamplesPipeline
from src.pipeline.evaluation import EvaluationPipeline
from src.pipeline.generation import GenerationPipeline


def run_data_ingestion():
    DataIngestionPipeline().main()


def run_chunking():
    ChunkingPipeline().main()


def run_embedding_indexing():
    EmbeddingIndexingPipeline().main()


def run_eval_samples():
    EvalSamplesPipeline().main()


def run_generation():
    positive_samples, negative_samples = EvalSamplesPipeline().main()
    generator = GenerationPipeline().main()
    config = ConfigurationManager()
    evaluation_config = config.get_evaluation_config()
    generator.run_batch(positive_samples, evaluation_config.positive_results_path)
    generator.run_batch(negative_samples, evaluation_config.negative_results_path)


def run_evaluation():
    evaluator = EvaluationPipeline().main()
    evaluator.run()


STAGES = {
    "data_ingestion": run_data_ingestion,
    "chunking": run_chunking,
    "embedding_indexing": run_embedding_indexing,
    "eval_samples": run_eval_samples,
    "generation": run_generation,
    "evaluation": run_evaluation,
}


def run_stage(name):
    logging.info(f"stage {name} started")
    try:
        STAGES[name]()
    except Exception as e:
        raise CustomException(e, sys)
    logging.info(f"stage {name} completed\n\n")


def main():
    parser = argparse.ArgumentParser(description="Run the CUAD RAG pipeline")
    parser.add_argument("stage", nargs="?", choices=list(STAGES), help="stage to run; omit to run all stages in order")
    args = parser.parse_args()

    stages = [args.stage] if args.stage else list(STAGES)
    for name in stages:
        run_stage(name)


if __name__ == "__main__":
    main()
