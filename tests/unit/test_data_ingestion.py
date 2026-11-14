from src.components.data_ingestion import DataIngestion

data_ingestion = DataIngestion(config=None)

# testing extract_unique_contracts function
def test_deduplicates_by_title():
    data = [
        {"title": "A", "context": "first content A"},
        {"title": "B", "context": "content B"},
        {"title": "A", "context": "duplicate content A, should be ignored"},
    ]
    assert data_ingestion.extract_unique_contracts(data) == [
        {"title": "A", "content": "first content A"},
        {"title": "B", "content": "content B"},
    ]

def test_no_duplicates():
    data = [
        {"title": "A", "context": "content A"},
        {"title": "B", "context": "content B"},
    ]
    assert data_ingestion.extract_unique_contracts(data) == [
        {"title": "A", "content": "content A"},
        {"title": "B", "content": "content B"},
    ]

def test_empty_input():
    assert data_ingestion.extract_unique_contracts([]) == []
