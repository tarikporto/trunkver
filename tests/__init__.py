from pathlib import Path
from trunkver.config import config


class StaticLogFile:
    FOLDER = "commit_log_files"
    SEMVER = "semver.txt"
    GITVERSION_TEST = "gitversion-test.txt"


TEST_FOLDER = Path(__file__).parent.resolve()
CONFIGS_FOLDER = f"{TEST_FOLDER}/configs"


def load_test_config():
    config.load(CONFIGS_FOLDER)


def get_log_files(log_file_name: str):
    with open(f"{TEST_FOLDER}/{StaticLogFile.FOLDER}/{log_file_name}", "r") as file:
        return file.read().split("\n")
