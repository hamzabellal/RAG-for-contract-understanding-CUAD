import pandas as pd
import pytest
from qdrant_client import QdrantClient
from src.entity.config_entity import EmbeddingIndexingConfig, RetrievalConfig
from src.components.embedding_indexing import EmbeddingIndexing
from src.components.retrieval import Retrieval


QDRANT_URL = "http://localhost:6333"
TEST_COLLECTION = "test_retrieval_collection"

def _qdrant_reachable() -> bool:
    try:
        QdrantClient(url=QDRANT_URL).get_collections()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _qdrant_reachable(), reason="Qdrant not reachable at localhost:6333"
)


@pytest.fixture
def chunk_file(tmp_path):
    df =  pd.DataFrame([
        {"title": "ContractA", "chunk_index": 0, "text": "PARTIES: This Agreement is between Acme Corp and Globex Inc."},
        {"title": "ContractA", "chunk_index": 1, "text": "This agreement is governed by the laws of Delaware."},
        {"title": "ContractB", "chunk_index": 0, "text": "This contract shall remain confidential for 5 years."}
    ])
    path = tmp_path / "chunks.parquet"
    df.to_parquet(path, index=False)
    return path

@pytest.fixture
def embedding_config(chunk_file, tmp_path):
    return EmbeddingIndexingConfig(
        root_dir = tmp_path,
        chunks_path = chunk_file,
        qdrant_url = QDRANT_URL,
        collection_name = TEST_COLLECTION,
        embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2",
        sparse_model_name = "Qdrant/bm25",
        report_path = tmp_path / "indexing_report.json"
    )

@pytest.fixture
def retrieval_config(chunk_file, tmp_path):
    return RetrievalConfig(
        root_dir = tmp_path,
        chunks_path = chunk_file,
        qdrant_url = QDRANT_URL,
        collection_name = TEST_COLLECTION,
        reranker_model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2",
        sparse_model_name = "Qdrant/bm25",
        tier1_categories = ["Parties"],
        tier3_categories = [],
        retrieve_top_k = 5,
        sparse_top_k = 5,
        rerank_top_n = 2,
        retrieve_top_k_tier3 = 5,
        sparse_top_k_tier3 = 5,
        rerank_top_n_tier3 = 2
    )

@pytest.fixture
def indexed_collection(embedding_config):
    client = QdrantClient(url=QDRANT_URL)
    if client.collection_exists(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)

    EmbeddingIndexing(embedding_config).initiate_embedding_indexing()

    yield

    if client.collection_exists(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)

@pytest.fixture
def retrieval(retrieval_config, indexed_collection):
    instance = Retrieval(retrieval_config)
    instance.initiate_retrieval()
    return instance


def test_retrieve_tier1_category_returns_first_chunk(retrieval):
    question = 'Highlight the parts (if any) of this contract related to "Parties" that should be reviewed by a lawyer. Details: The two or more parties who signed the contract'
    result = retrieval.retrieve(question, "ContractA")
    assert result == ["PARTIES: This Agreement is between Acme Corp and Globex Inc."]

def test_retrieve_non_tier1_category_returns_results(retrieval):
    question = 'Highlight the parts related to "Governing Law" that should be reviewed by a lawyer. Details: Which law governs.'
    result = retrieval.retrieve(question, "ContractA")
    assert len(result) == 2
    assert all(isinstance(r, str) and r for r in result)
