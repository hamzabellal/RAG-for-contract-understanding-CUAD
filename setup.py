from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1"

REPO_NAME = "RAG-for-contract-understanding-CUAD"
AUTHOR_USERNAME = "hamzabellal"
AUTHOR_EMAIL = "hamzabellal1900@gmail.com"

setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOR_USERNAME,
    author_email=AUTHOR_EMAIL,
    long_description=long_description,
    url=f"https://github.com/{AUTHOR_USERNAME}/{REPO_NAME}",
    packages=find_packages()
)