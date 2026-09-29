from src.utils import read_yaml, create_directories
from src.constants import *
from src.entity.config_entity import *
from pathlib import Path

class ConfigurationManager():
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
            qdrant_url = config.qdrant_url,
            collection_name = config.collection_name,
            embedding_model_name = params.embedding_model_name,
            sparse_model_name = params.sparse_model_name,
            report_path = Path(config.report_path)
        )

        return embedding_config