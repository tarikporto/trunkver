import pytest
from tests import get_log_files, load_test_config, StaticLogFile
from trunkver.git_repository import GitRepository


@pytest.fixture
def git_repo_semver_main():
    log_files = get_log_files(StaticLogFile.SEMVER)
    load_test_config()
    return GitRepository(branch_name="main", commit_lines=log_files)


@pytest.fixture
def git_repo_gitversion_main():
    log_files = get_log_files(StaticLogFile.GITVERSION_TEST)
    load_test_config()
    return GitRepository(branch_name="main", commit_lines=log_files)


def test_git_repository_semver(git_repo_semver_main):

    expected_version = "0.2.1.0"
    assert git_repo_semver_main.version == expected_version


def test_git_repository_gitversion(git_repo_gitversion_main):

    expected_version = "0.6.26.2"
    assert git_repo_gitversion_main.version == expected_version
