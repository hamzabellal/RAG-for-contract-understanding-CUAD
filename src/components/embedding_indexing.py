from src.logger import logging
from src.exception import CustomException
import sys
import pandas as pd
from datetime import datetime
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from qdrant_client import QdrantClient
from src.entity.config_entity import EmbeddingIndexingConfig
from src.utils import save_json
import uuid


class EmbeddingIndexing:
    def __init__(self, config: EmbeddingIndexingConfig):
        self.embedding_indexing_config = config

    def initiate_embedding_indexing(self):
        logging.info("starting embedding and indexing component")
        try:
            all_chunks = pd.read_parquet(self.embedding_indexing_config.chunks_path)
            nodes = all_chunks.to_dict(orient="records")
            textnodes = [
                TextNode(text=node["text"], 
                         metadata={"title": node["title"], "chunk_index": node["chunk_index"]},
                         id_ = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{node['title']}_{node['chunk_index']}"))
                )
                for node in nodes
            ]
            logging.info("TextNode objects from chunks successfully created")

            embed_model = HuggingFaceEmbedding(model_name = self.embedding_indexing_config.embedding_model_name)
            logging.info("embedding model called")

            client = QdrantClient(url=self.embedding_indexing_config.qdrant_url)
            logging.info("connected to Qdrant server")

            logging.info("building vector store")
            vector_store = QdrantVectorStore(collection_name=self.embedding_indexing_config.collection_name,
                                             client=client,
                                             enable_hybrid=True,
                                             fastembed_sparse_model=self.embedding_indexing_config.sparse_model_name)
            

            logging.info("building index...")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex(textnodes, storage_context=storage_context, embed_model=embed_model)

            logging.info("indexing done successfully")

            collection_info = client.get_collection(self.embedding_indexing_config.collection_name)
            report = {
                "collection_name": self.embedding_indexing_config.collection_name,
                "points_count": collection_info.points_count,
                "embedding_model": self.embedding_indexing_config.embedding_model_name,
                "sparse_model": self.embedding_indexing_config.sparse_model_name,
                "timestamp": datetime.now().isoformat(),
            }

            save_json(self.embedding_indexing_config.report_path, report)
            logging.info(f"indexing report saved at {self.embedding_indexing_config.report_path}")

            return report
        except Exception as e:
            raise CustomException(e, sys)