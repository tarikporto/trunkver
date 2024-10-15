import pytest
from trunkver.semantic_version import SemanticVersion


@pytest.fixture
def starting_version():
    return SemanticVersion(
        major=0,
        minor=2,
        patch=1,
        commits=0,
    )


def test_semantic_version_bump_major(starting_version):

    expected_version = "2.0.0.0"

    semver = starting_version

    semver.bump_major()
    semver.bump_minor()
    semver.bump_patch()
    semver.bump_commits()
    semver.bump_major()

    assert str(semver) == expected_version


def test_semantic_version_bump_minor(starting_version):

    expected_version = "0.4.1.0"

    semver = starting_version

    semver.bump_minor()
    semver.bump_patch()
    semver.bump_patch()
    semver.bump_commits()
    semver.bump_minor()
    semver.bump_patch()

    assert str(semver) == expected_version


def test_semantic_version_bump_patch(starting_version):

    expected_version = "0.3.4.1"

    semver = starting_version

    semver.bump_minor()
    semver.bump_patch()
    semver.bump_patch()
    semver.bump_commits()
    semver.bump_patch()
    semver.bump_patch()
    semver.bump_commits()

    assert str(semver) == expected_version
