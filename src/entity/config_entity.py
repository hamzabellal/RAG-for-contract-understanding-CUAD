from dataclasses import dataclass
from pathlib import Path
from typing import List
from box import ConfigBox

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
    tier1_categories: List[str]
    tier3_categories: List[str]
    retrieve_top_k: int
    sparse_top_k: int
    rerank_top_n: int
    retrieve_top_k_tier3: int
    sparse_top_k_tier3: int
    rerank_top_n_tier3: int

@dataclass(frozen=True)
class GenerationConfig:
    root_dir: Path
    llm_model_name: str
    request_timeout: int
    temperature: float
    use_reasoning: bool