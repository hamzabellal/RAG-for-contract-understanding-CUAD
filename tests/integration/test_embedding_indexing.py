import pandas as pd
import pytest
from qdrant_client import QdrantClient

from src.components.embedding_indexing import EmbeddingIndexing
from src.entity.config_entity import EmbeddingIndexingConfig

QDRANT_URL = "http://localhost:6333"
TEST_COLLECTION = "test_integration_collection"

def _qdrant_reachable() -> bool:
    try:
        QdrantClient(url=QDRANT_URL).get_collections()
        return True
    except Exception:
        return False

pytest.mark.skipif(
    not _qdrant_reachable(), reason="Qdrant not reachable at localhost:6333"
)

@pytest.fixture
def chunks_file(tmp_path):
    df = pd.DataFrame([
        {"title": "ContractA", "chunk_index": 0, "text": "This agreement is governed by the laws of Delaware."},
        {"title": "ContractA", "chunk_index": 1, "text": "Either party may terminate this agreement with 30 days notice."},
        {"title": "ContractB", "chunk_index": 0, "text": "This contract shall remain confidential."},
    ])

    path = tmp_path / "chunks.parquet"
    df.to_parquet(path, index=False)
    return path

@pytest.fixture
def embedding_config(chunks_file, tmp_path):
    return EmbeddingIndexingConfig(
        root_dir=tmp_path,
        chunks_path=chunks_file,
        qdrant_url=QDRANT_URL,
        collection_name=TEST_COLLECTION,
        embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",
        sparse_model_name="Qdrant/bm25",
        report_path=tmp_path / "indexing_report.json",
    )

def _delete_test_collection():
    client = QdrantClient(url=QDRANT_URL)
    if client.collection_exists(TEST_COLLECTION):
        client.delete_collection(TEST_COLLECTION)

def test_embedding_indexing_writes_expected_points(embedding_config):
    _delete_test_collection()
    try:
        embedder = EmbeddingIndexing(embedding_config)
        report = embedder.initiate_embedding_indexing()

        assert report["points_count"] == 3
        assert report["collection_name"] == TEST_COLLECTION

        client = QdrantClient(url=QDRANT_URL)
        collection_info = client.get_collection(TEST_COLLECTION)
        assert collection_info.points_count == 3
    finally:
        _delete_test_collection()