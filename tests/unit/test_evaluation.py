from types import SimpleNamespace
import pandas as pd
from src.components.evaluation import Evaluator

def make_evaluator(absence_phrases=None):
    config = SimpleNamespace(absence_phrases=absence_phrases or [
        "not present", "not specified", "not mentioned", "does not contain",
        "no clause", "not applicable", "not included", "not found", "n/a", "absent"
    ])
    return Evaluator(config=config, generator=None)

# testing classify function
def test_error_answer():
    evaluator = make_evaluator()
    assert evaluator.classify("[ERROR: Timeout: request failed]") == "error"

def test_true_negative():
    evaluator = make_evaluator()
    assert evaluator.classify("This clause is not present in this contract.") == "true negative"

def test_true_negative_case_insensitive():
    evaluator = make_evaluator()
    assert evaluator.classify("Not Present in this contract.") == "true negative"

def test_false_positive():
    evaluator = make_evaluator()
    assert evaluator.classify("The termination clause states that...") == "false positive"

# testing stratified_samples function
def test_caps_at_n_samples():
    evaluator = make_evaluator()
    pool = pd.DataFrame({"title": ["c1", "c2", "c3"], "category": ["A", "A", "A"]})
    result = evaluator.stratified_samples(pool, n_samples=2)
    assert len(result) == 2

def test_returns_all_when_fewer_than_n_samples():
    evaluator = make_evaluator()
    pool = pd.DataFrame({"title": ["c1", "c2"], "category": ["B", "B"]})
    result = evaluator.stratified_samples(pool, n_samples=5)
    assert len(result) == 2

def test_respects_each_category_independently():
    evaluator = make_evaluator()
    pool = pd.DataFrame({
        "title": ["c1", "c2", "c3", "c4", "c5"],
        "category": ["A", "A", "A", "B", "B"],
    })
    result = evaluator.stratified_samples(pool, n_samples=2)
    counts = result["category"].value_counts()
    assert counts["A"] == 2
    assert counts["B"] == 2
