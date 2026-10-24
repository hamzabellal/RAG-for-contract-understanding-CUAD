from src.components.retrieval import Retrieval

retrieval = Retrieval(config=None)

# testing strip_boilerplate function
def test_returns_category_and_detail():
    question = 'Highlight the parts (if any) of this contract related to "Unlimited/All-You-Can-Eat-License" that should be reviewed by a lawyer. Details: Is there a clause granting one party an enterprise, call you can eat or unlimited usage license?'
    assert retrieval.strip_boilerplate(question) == '"Unlimited/All-You-Can-Eat-License". Is there a clause granting one party an enterprise, call you can eat or unlimited usage license?'

def test_quotes_not_present():
    question = 'Highlight the parts (if any) of this contract related to Unlimited/All-You-Can-Eat-License that should be reviewed by a lawyer. Details: Is there a clause granting one party an enterprise, call you can eat or unlimited usage license?'
    assert retrieval.strip_boilerplate(question) == '. Is there a clause granting one party an enterprise, call you can eat or unlimited usage license?'

def test_detail_not_present():
    question = 'Highlight the parts (if any) of this contract related to "Unlimited/All-You-Can-Eat-License" that should be reviewed by a lawyer.'
    assert retrieval.strip_boilerplate(question) == '"Unlimited/All-You-Can-Eat-License".'

def test_no_quotes_no_detail():
    question = 'review the contract'
    assert retrieval.strip_boilerplate(question) == '.'