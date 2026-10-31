import os
from pathlib import Path

from src.constants import *
from src.entity.config_entity import *
from src.utils import create_directories, read_yaml


class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            data_source = config.data_source,
            root_dir = Path(config.root_dir),
            full_data_dir = Path(config.full_data_dir),
            contracts = Path(config.contracts),
            cleaned_contracts = Path(config.cleaned_contracts)
        )

        return data_ingestion_config

    def get_chunking_config(self) -> ChunkingConfig:
        config = self.config.chunking
        params = self.params.chunking

        create_directories([config.root_dir])

        chunking_config = ChunkingConfig(
            root_dir = Path(config.root_dir),
            data_source = Path(config.data_source),
            chunks_path = Path(config.chunks_path),
            chunk_size = params.chunk_size,
            chunk_overlap = params.chunk_overlap,
            tokenizer_name = params.tokenizer
        )

        return chunking_config
    
    def get_embedding_config(self) -> EmbeddingIndexingConfig:
        config = self.config.embedding
        params = self.params.embedding

        create_directories([config.root_dir])

        embedding_config = EmbeddingIndexingConfig(
            root_dir = Path(config.root_dir),
            chunks_path = Path(config.chunks_path),
            qdrant_url = os.environ.get("QDRANT_URL", config.qdrant_url),
            collection_name = config.collection_name,
            embedding_model_name = params.embedding_model_name,
            sparse_model_name = params.sparse_model_name,
            report_path = Path(config.report_path)
        )

        return embedding_config

    def get_retrieval_config(self) -> RetrievalConfig:
        config = self.config.retrieval
        params = self.params.retrieval

        create_directories([config.root_dir])

        retrieval_config = RetrievalConfig(
            root_dir = Path(config.root_dir),
            chunks_path = Path(config.chunks_path),
            qdrant_url = os.environ.get("QDRANT_URL", config.qdrant_url),
            collection_name = config.collection_name,
            reranker_model_name = params.reranker_model_name,
            embedding_model_name = params.embedding_model_name,
            sparse_model_name = params.sparse_model_name,
            tier1_categories = params.tier1_categories,
            tier3_categories = params.tier3_categories,
            retrieve_top_k = params.retrieve_top_k,
            sparse_top_k = params.sparse_top_k,
            rerank_top_n = params.rerank_top_n,
            retrieve_top_k_tier3 = params.retrieve_top_k_tier3,
            sparse_top_k_tier3 = params.sparse_top_k_tier3,
            rerank_top_n_tier3 = params.rerank_top_n_tier3
        )

        return retrieval_config

    def get_generation_config(self) -> GenerationConfig:
        config = self.config.generation
        params = self.params.generation

        create_directories([config.root_dir])

        generation_config = GenerationConfig(
            root_dir = Path(config.root_dir),
            ollama_base_url = os.environ.get("OLLAMA_BASE_URL", config.ollama_base_url),
            llm_model_name = params.llm_model_name,
            request_timeout = params.request_timeout,
            temperature = params.temperature,
            use_reasoning = params.use_reasoning
        )

        return generation_config

    def get_evaluation_config(self) -> EvaluationConfig:
        config = self.config.evaluation
        params = self.params.evaluation

        create_directories([config.root_dir])

        evaluation_config = EvaluationConfig(
            root_dir = Path(config.root_dir),
            full_data_path = Path(config.full_data_path),
            positive_samples_path = Path(config.positive_samples_path),
            negative_samples_path = Path(config.negative_samples_path),
            positive_results_path = Path(config.positive_results_path),
            negative_results_path = Path(config.negative_results_path),
            ragas_scores_path = Path(config.ragas_scores_path),
            summary_global_path = Path(config.summary_global_path),
            summary_by_category_path = Path(config.summary_by_category_path),
            negative_report_path = Path(config.negative_report_path),
            mlflow_run_id_path = Path(config.mlflow_run_id_path),
            mlflow_tracking_uri = config.mlflow_tracking_uri,
            mlflow_experiment_name = config.mlflow_experiment_name,
            n_per_category_positive = params.n_per_category_positive,
            n_per_category_negative = params.n_per_category_negative,
            judge_model_name = params.judge_model_name,
            judge_embeddings_model_name = params.judge_embeddings_model_name,
            absence_phrases = params.absence_phrases,
            batch_size = params.batch_size
        )

        return evaluation_config