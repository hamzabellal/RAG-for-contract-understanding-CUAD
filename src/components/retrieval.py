import sys
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import RetrievalConfig
import re
import pandas as pd
from pathlib import Path
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import SentenceTransformerRerank
from qdrant_client import QdrantClient


class Retrieval:
    def __init__(self, config: RetrievalConfig):
        self.retrieval_config = config

    def extract_category(self, question: str) -> str:
        logging.info("extracting corresponding category")
        match = re.search(r'"([^"]+)"', question)
        category = match.group(1) if match else None
        return category

    def strip_boilerplate(self, question: str) -> str:
        match = re.search(r'"([^"]+)"', question)
        category = match.group(0) if match else ""
        detail = question.split("Details: ", 1)[1] if "Details: " in question else ""
        return f"{category}. {detail}".strip()

    def initiate_retrieval(self):
        logging.info("preparing retrieval component")
        try:
            self.chunks_df = pd.read_parquet(self.retrieval_config.chunks_path)

            self.embed_model = HuggingFaceEmbedding(model_name=self.retrieval_config.embedding_model_name)
            self.reranker = SentenceTransformerRerank(model=self.retrieval_config.reranker_model_name,
                                                      top_n=self.retrieval_config.rerank_top_n)

            client = QdrantClient(url=self.retrieval_config.qdrant_url)
            vector_store = QdrantVectorStore(
                collection_name = self.retrieval_config.collection_name,
                client = client,
                enable_hybrid = True,
                fastembed_sparse_model = self.retrieval_config.sparse_model_name
            )
            self.index = VectorStoreIndex.from_vector_store(vector_store, embed_model = self.embed_model)

            logging.info("retrieval component ready")

        except Exception as e:
            raise CustomException(e, sys)

    def _get_tier1_chunk(self, title: str) -> str:
        logging.info(f"getting first chunk of document {title}")
        exact_contract = self.chunks_df[self.chunks_df["title"] == title].sort_values("chunk_index", ascending=True)
        return exact_contract.iloc[0]["text"]
    
    def _retrieve_and_rerank(self, question: str, title: str, category: str) -> list[str]:
        retrieve_top_k = self.retrieval_config.retrieve_top_k_tier3 if category in self.retrieval_config.tier3_categories else self.retrieval_config.retrieve_top_k
        sparse_top_k =  self.retrieval_config.sparse_top_k_tier3 if category in self.retrieval_config.tier3_categories else self.retrieval_config.sparse_top_k
        rerank_top_n = self.retrieval_config.rerank_top_n_tier3 if category in self.retrieval_config.tier3_categories else self.retrieval_config.rerank_top_n

        filters = MetadataFilters(filters=[ExactMatchFilter(key="title", value=title)])
        retriever = self.index.as_retriever(
            similarity_top_k = retrieve_top_k,
            sparse_top_k = sparse_top_k,
            vector_store_query_mode = "hybrid",
            filters = filters
        )
        logging.info("retrieving...")
        candidates = retriever.retrieve(question)

        self.reranker.top_n = rerank_top_n
        short_question = self.strip_boilerplate(question)
        logging.info("reranking...")
        reranked = self.reranker.postprocess_nodes(candidates, query_str=short_question)
    
        return [n.get_content() for n in reranked]
        
    def retrieve(self, question:str, title:str) -> list[str]:
        category = self.extract_category(question)
        logging.info("start retrieving and reranking")
        if category in self.retrieval_config.tier1_categories:
            return [self._get_tier1_chunk(title)]
        return self._retrieve_and_rerank(question, title, category)