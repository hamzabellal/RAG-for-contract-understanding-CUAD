from src.components.generation import Generator

generator = Generator(config=None, retriever=None)

# testing _extract_answer function
def test_with_reasoning_prefix():
    raw = "Reasoning: the clause addresses termination.\nAnswer: Either party may terminate upon 30 days notice."
    assert generator._extract_answer(raw) == "Either party may terminate upon 30 days notice."

def test_without_answer_marker():
    raw = "Either party may terminate upon 30 days notice."
    assert generator._extract_answer(raw) == "Either party may terminate upon 30 days notice."

def test_strips_whitespace():
    raw = "Answer:   Either party may terminate.   "
    assert generator._extract_answer(raw) == "Either party may terminate."

def test_keeps_text_after_first_marker_only():
    raw = "Answer: first mention\nAnswer: second mention"
    assert generator._extract_answer(raw) == "first mention\nAnswer: second mention"
