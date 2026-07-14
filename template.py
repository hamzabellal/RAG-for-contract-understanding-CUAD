import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s : ')

list_of_files = [
    ".gitignore",
    ".github/workflows/.gitkeep",
    "src/__init__.py",
    "src/logger.py",
    "src/exception.py",
    "src/utils/__init__.py",
    "src/config/__init__.py",
    "src/config/configuration.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/components/__init__.py",
    "src/pipeline/__init__.py",
    "src/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "main.py",
    "notebook/trials.ipynb",
    "docker/Dockerfile",
    "docker/.dockerignore",
    "docker/docker-compose.yml",
    "api/__init__.py",
    "api/main.py",

]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filename}")

    else:
        logging.info(f"{filename} already exits")

