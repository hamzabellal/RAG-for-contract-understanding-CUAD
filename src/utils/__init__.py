import json
import os
import re
import sys
from pathlib import Path
import psycopg2

import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from src.exception import CustomException
from src.logger import logging


@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise CustomException(e, sys)

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Created directory at {path}")


@ensure_annotations
def save_json(filepath: Path, obj: dict | list):
    try:
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(obj, f, indent=2)
    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def clean_content(text:str) -> str:
    logging.info("starting cleaning contracts text")
    try:
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = "\n".join(line.strip() for line in text.split('\n'))
        return text.strip()
    except Exception as e:
        raise CustomException(e, sys)


@ensure_annotations
def extract_category(question: str) -> str | None:
    logging.info("extracting corresponding category")
    try:
        match = re.search(r'"([^"]+)"', question)
        category = match.group(1) if match else None
        return category
    except Exception as e:
        raise CustomException(e, sys)

@ensure_annotations
def get_db_connection(api_config):
    return psycopg2.connect(
        host=api_config.feedback_db_host,
        port=api_config.feedback_db_port,
        user=api_config.feedback_db_user,
        password=api_config.feedback_db_password,
        dbname=api_config.feedback_db_name,
    )