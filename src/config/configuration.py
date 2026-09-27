from src.utils import read_yaml, create_directories
from src.constants import *
from src.entity.config_entity import *

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
            root_dir = config.root_dir,
            full_data_dir = config.full_data_dir,
            contracts = config.contracts,
            cleaned_contracts = config.cleaned_contracts
        )

        return data_ingestion_config

    def get_chunking_config(self) -> ChunkingConfig:
        config = self.config.chunking
        params = self.params.chunking

        create_directories([config.root_dir])

        chunking_config = ChunkingConfig(
            root_dir = config.root_dir,
            data_source = config.data_source,
            chunks_path = config.chunks_path,
            chunk_size = params.chunk_size,
            chunk_overlap = params.chunk_overlap,
            tokenizer_name = params.tokenizer
        )

        return chunking_config