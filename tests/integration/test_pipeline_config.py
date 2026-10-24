import subprocess
import sys
from pathlib import Path

import yaml

from main import STAGES
from src.config.configuration import ConfigurationManager

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXPECTED_STAGES = [
    "data_ingestion",
    "chunking",
    "embedding_indexing",
    "eval_samples",
    "generation",
    "evaluation",
]

def test_all_stage_configs_build_without_error():
    config_manager = ConfigurationManager()
    config_manager.get_data_ingestion_config()
    config_manager.get_chunking_config()
    config_manager.get_embedding_config()
    config_manager.get_retrieval_config()
    config_manager.get_generation_config()
    config_manager.get_evaluation_config()

def test_main_help_lists_all_stages():
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        capture_output=True,
        text=True,
        check=False,
        cwd=PROJECT_ROOT,
    )
    assert result.returncode == 0
    for stage in EXPECTED_STAGES:
        assert stage in result.stdout

def test_main_stages_match_dvc_yaml_stages():
    with open(PROJECT_ROOT / "dvc.yaml") as f:
        dvc_config = yaml.safe_load(f)

    dvc_stage_names = set(dvc_config["stages"].keys())
    main_stage_names = set(STAGES)

    assert dvc_stage_names == main_stage_names