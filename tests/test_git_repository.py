import pytest
from tests import get_path, LogFile, get_log_files
from trunkver.config import config
from trunkver.git_repository import GitRepository


class TestGitRepository:
    def test_git_repository_semver(self):

        expected_version = "0.2.1.0"
        log_files = get_log_files(LogFile.SEMVER)

        config.load(get_path())
        git_repo = GitRepository(branch_name="main", commit_lines=log_files)

        assert git_repo.version == expected_version

    def test_git_repository_gitversion(self):

        expected_version = "0.6.26.2"
        log_files = get_log_files(LogFile.GITVERSION_TEST)

        config.load(get_path())
        git_repo = GitRepository(branch_name="main", commit_lines=log_files)

        assert git_repo.version == expected_version
