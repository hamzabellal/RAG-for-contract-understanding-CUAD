import sys
import os
from pathlib import Path
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from src.logger import logging
from src.exception import CustomException
from ensure import ensure_annotations

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file {path_to_yaml} loaded succesfully")
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