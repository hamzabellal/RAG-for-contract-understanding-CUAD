import sys
from collections import defaultdict

import pandas as pd
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from transformers import AutoTokenizer

from src.entity.config_entity import ChunkingConfig
from src.exception import CustomException
from src.logger import logging


class Chunker:
    def __init__(self, config: ChunkingConfig):
        self.chunking_config = config

    def initiate_chunking(self):
        logging.info("starting chunking component")
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.chunking_config.tokenizer_name)
            logging.info("creating tokenizer object")

            Splitter = SentenceSplitter(
                chunk_size=self.chunking_config.chunk_size,
                chunk_overlap=self.chunking_config.chunk_overlap,
                tokenizer=tokenizer.encode
            )

            unique_contracts = pd.read_parquet(self.chunking_config.data_source)
            contracts = unique_contracts.to_dict(orient="records")
            documents = [
                Document(text=contract["clean_content"], metadata={"title": contract["title"]})
                for contract in contracts
            ]

            nodes = Splitter.get_nodes_from_documents(documents)
            logging.info("chunks created successfully")

            token_counts = [len(tokenizer.encode(n.get_content())) for n in nodes]
            logging.info(f"number of chunks: {len(nodes)}")
            logging.info(f"chunk token length - min: {min(token_counts)}, max: {max(token_counts)}")

            counters = defaultdict(int)
            for n in nodes:
                title = n.metadata["title"]
                n.metadata["chunk_index"] = counters[title]
                counters[title] += 1
            logging.info("adding chunk_index to metadata")

            rows = [
                {"title" : n.metadata["title"], "chunk_index" : n.metadata["chunk_index"], "text" : n.get_content()} 
                for n in nodes
            ]
            df_chunks = pd.DataFrame(rows)
            df_chunks.to_parquet(self.chunking_config.chunks_path, index=False)
            logging.info(f"nodes saved at {self.chunking_config.chunks_path} successfully")

            return self.chunking_config.chunks_path

        except Exception as e:
            raise CustomException(e, sys)