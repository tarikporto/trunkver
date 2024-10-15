import pytest
from tests import get_path, LogFile, get_log_files
from trunkver.config import config
from trunkver.semantic_version import SemanticVersion


class TestSemanticVersion:
    def test_semantic_version_bump_major(self):

        expected_version = "2.0.0.0"

        semver = SemanticVersion(
            major=0,
            minor=2,
            patch=1,
            commits=0,
        )

        semver.bump_major()
        semver.bump_minor()
        semver.bump_patch()
        semver.bump_commits()
        semver.bump_major()

        assert str(semver) == expected_version

    def test_semantic_version_bump_minor(self):

        expected_version = "0.4.1.0"

        semver = SemanticVersion(
            major=0,
            minor=2,
            patch=1,
            commits=0,
        )

        semver.bump_minor()
        semver.bump_patch()
        semver.bump_patch()
        semver.bump_commits()
        semver.bump_minor()
        semver.bump_patch()

        assert str(semver) == expected_version

    def test_semantic_version_bump_patch(self):

        expected_version = "0.3.4.1"

        semver = SemanticVersion(
            major=0,
            minor=2,
            patch=1,
            commits=0,
        )

        semver.bump_minor()
        semver.bump_patch()
        semver.bump_patch()
        semver.bump_commits()
        semver.bump_patch()
        semver.bump_patch()
        semver.bump_commits()

        assert str(semver) == expected_version
