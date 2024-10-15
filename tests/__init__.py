from pathlib import Path


class LogFile:
    FOLDER = "commit_log_files"
    SEMVER = "semver.txt"
    GITVERSION_TEST = "gitversion-test.txt"


TEST_FOLDER = Path(__file__).parent.resolve()
CONFIGS_FOLDER = f"{TEST_FOLDER}/configs"


def get_log_files(log_file_name: str):
    with open(f"{TEST_FOLDER}/{LogFile.FOLDER}/{log_file_name}", "r") as file:
        return file.read().split("\n")


def get_path():
    return f"{CONFIGS_FOLDER}"
