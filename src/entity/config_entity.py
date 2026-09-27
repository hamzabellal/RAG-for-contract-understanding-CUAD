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
