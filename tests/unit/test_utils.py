from src.utils import extract_category, clean_content

def test_extract_category_returns_category_in_quotes():
    question = 'Highlight the parts related to "Governing Law" that...'
    assert extract_category(question) == "Governing Law"

def test_extract_category_absent_category():
    assert extract_category("no category here") is None

def test_extract_category_empty_question():
    assert extract_category("") is None

def test_extract_category_empty_quotes():
    assert extract_category('""') is None

def test_extract_category_multiple_quotes():
    question = 'Highlight the parts (if any) of this contract related to "Unlimited/All-You-Can-Eat-License" that should be reviewed by a lawyer. Details: "Is there a clause granting one party an enterprise, call you can eat or unlimited usage license?"'
    assert extract_category(question) == "Unlimited/All-You-Can-Eat-License"

def test_clean_content_reduces_multiple_spaces():
    assert clean_content("hello    world") == "hello world"

def test_clean_content_reduces_excessive_newlines():
    text = "line1\n\n\n\nline2"
    assert clean_content(text) == "line1\n\nline2"

def test_clean_content_strips_line_whitspaces():
    text = "  line1  \n  line2  "
    assert clean_content(text) == "line1\nline2"

def test_clean_content_idempotent_on_clean_text():
    text = "line1\n\nline2"
    assert clean_content(text) == text

def test_clean_content_empty_string():
    assert clean_content("") == ""

def test_clean_content_whitespace_only():
    assert clean_content("  \n\n  \n ") == ""