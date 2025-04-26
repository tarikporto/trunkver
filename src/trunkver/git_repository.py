import logging
import re
from typing import List

from .config import ConfigFile, config
from .semantic_version import SemanticVersion

logger = logging.getLogger(__name__)


class GitCommit:
    EXTRA_FIELD_TAG_REGEX = r"tag: (.*)"

    def __init__(
        self, abbreviated_ref: str, ref: str, timestamp: int, message: str, extra: str
    ):
        self.abbreviated_ref = abbreviated_ref
        self.ref = ref
        self.timestamp = timestamp
        self.message = message
        self.extra = extra
        self.tags = []
        self.semver = None

        for info in extra.split(","):
            tag_match = re.search(self.EXTRA_FIELD_TAG_REGEX, info)
            if tag_match:
                (tag,) = tag_match.groups()
                self.tags.append(tag)
                semver_tag_match = re.search(
                    config.regex_patterns[ConfigFile.FIELD_PATTERN_SEMVER_TAG], tag
                )
                if semver_tag_match:
                    self.semver = SemanticVersion.parse(*semver_tag_match.groups())

    def __str__(self):
        return f"{self.abbreviated_ref} {self.ref} {self.timestamp} {self.message} {self.tags}"

    @property
    def has_semver_tag(self) -> bool:
        return self.semver != None


class GitRepository:

    def __init__(
        self,
        branch_name: str,
        commit_lines: List[str],
    ):
        self.branch_name = branch_name
        self.semver, commits_to_read = self._process_commit_lines(commit_lines)
        self._calculate_semver(commits_to_read)

    def _process_commit_lines(self, commit_lines: List[str]):
        commits_to_read = []
        latest_semver = None

        for line in commit_lines:
            logger.debug(line)

            commit = GitCommit(*re.search(config.COMMIT_REGEX, line).groups())
            logger.debug(commit)

            # only read commits since latest git tag with a semantic version
            if commit.has_semver_tag:
                latest_semver = commit.semver
                break

            commits_to_read.append(commit)

        semver = latest_semver if latest_semver else SemanticVersion()

        return semver, commits_to_read

    def _calculate_semver(self, commits_to_read: List[GitCommit]):
        logger.debug(f"Starting version: {self.semver}")

        commits_to_read.sort(key=lambda cmt: cmt.timestamp)
        for cmt in commits_to_read:
            logger.debug(f"Current version: {self.semver}")
            logger.debug(
                f"Current commit message: '{cmt.message}', timestamp: '{cmt.timestamp}'"
            )

            if re.search(
                config.regex_patterns[ConfigFile.FIELD_PATTERN_BUMP_MAJOR], cmt.message
            ):
                logger.debug(f"Bumping major version")
                self.semver.bump_major()
            elif re.search(
                config.regex_patterns[ConfigFile.FIELD_PATTERN_BUMP_MINOR], cmt.message
            ):
                logger.debug(f"Bumping minor version")
                self.semver.bump_minor()
            elif re.search(
                config.regex_patterns[ConfigFile.FIELD_PATTERN_BUMP_PATCH], cmt.message
            ):
                logger.debug(f"Bumping patch version")
                self.semver.bump_patch()
            else:
                self.semver.bump_commits()

    @property
    def version(self):
        return str(self.semver)

    @property
    def is_main_branch(self):
        return re.search(
            config.regex_patterns[ConfigFile.FIELD_PATTERN_MAIN_BRANCH],
            self.branch_name,
        )

    @property
    def is_feature_branch(self):
        return re.search(
            config.regex_patterns[ConfigFile.FIELD_PATTERN_FEATURE_BRANCH],
            self.branch_name,
        )

    @property
    def is_pull_request_branch(self):
        return re.search(
            config.regex_patterns[ConfigFile.FIELD_PATTERN_PR_BRANCH], self.branch_name
        )
