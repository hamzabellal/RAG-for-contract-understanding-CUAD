from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    data_source: str
    full_data_dir: Path
    contracts: Path
    cleaned_contracts: Path

@dataclass(frozen=True)
class ChunkingConfig:
    root_dir : Path
    data_source : Path
    chunks_path : Path
    chunk_size : int
    chunk_overlap : int
    tokenizer_name : str

@dataclass(frozen=True)
class EmbeddingIndexingConfig:
    root_dir: Path
    chunks_path: Path
    qdrant_url: str
    collection_name: str
    embedding_model_name: str
    sparse_model_name: str
    report_path: Path

@dataclass(frozen=True)
class RetrievalConfig:
    root_dir: Path
    chunks_path: Path
    qdrant_url: str
    collection_name: str
    reranker_model_name: str
    embedding_model_name: str
    sparse_model_name: str
    tier1_categories: list[str]
    tier3_categories: list[str]
    retrieve_top_k: int
    sparse_top_k: int
    rerank_top_n: int
    retrieve_top_k_tier3: int
    sparse_top_k_tier3: int
    rerank_top_n_tier3: int

@dataclass(frozen=True)
class GenerationConfig:
    root_dir: Path
    ollama_base_url: str
    llm_model_name: str
    request_timeout: int
    temperature: float
    use_reasoning: bool

@dataclass(frozen=True)
class EvaluationConfig:
    root_dir: Path
    full_data_path: Path
    positive_samples_path: Path
    negative_samples_path: Path
    positive_results_path: Path
    negative_results_path: Path
    ragas_scores_path: Path
    summary_global_path: Path
    summary_by_category_path: Path
    negative_report_path: Path
    mlflow_tracking_uri: str
    mlflow_run_id_path: Path
    mlflow_experiment_name: str
    n_per_category_positive: int
    n_per_category_negative: int
    judge_model_name: str
    judge_embeddings_model_name: str
    absence_phrases: list[str]
    batch_size : int

@dataclass(frozen=True)
class ApiConfig:
    root_dir: Path
    feedback_db_host: str
    feedback_db_port: int
    feedback_db_user: str
    feedback_db_password: str
    feedback_db_name: str

@dataclass(frozen=True)
class MonitoringConfig:
    root_dir: Path
    mlflow_tracking_uri: str
    mlflow_experiment_name: str
    feedback_window_days : int