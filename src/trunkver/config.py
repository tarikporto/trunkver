import io
import logging
import re
import yaml

logger = logging.getLogger(__name__)


class ConfigFile:
    NAME = "trunkver.yml"
    FIELD_PATTERNS = "patterns"
    FIELD_PATTERN_BUMP_MAJOR = "bump_major_marker"
    FIELD_PATTERN_BUMP_MINOR = "bump_minor_marker"
    FIELD_PATTERN_BUMP_PATCH = "bump_patch_marker"
    FIELD_PATTERN_SKIP_BUMP = "skip_bump_marker"
    FIELD_PATTERN_SEMVER_TAG = "semver_tag"
    FIELD_PATTERN_MAIN_BRANCH = "main_branch"
    FIELD_PATTERN_FEATURE_BRANCH = "feature_branch"
    FIELD_PATTERN_PR_BRANCH = "pr_branch"

    DEFAULT = {
        FIELD_PATTERNS: {
            FIELD_PATTERN_BUMP_MAJOR: "\\+(breaking|major)\\b",
            FIELD_PATTERN_BUMP_MINOR: "\\+(feature|minor)\\b",
            FIELD_PATTERN_BUMP_PATCH: "\\+(fix|patch|docs|ci)\\b",
            FIELD_PATTERN_SKIP_BUMP: "\\+(none|skip)\\b",
            FIELD_PATTERN_SEMVER_TAG: "[vV]?([\\d]+)\\.([\\d]+)\\.([\\d]+)\\.?([\\d]+)?",
            FIELD_PATTERN_MAIN_BRANCH: "^master$|^main$",
            FIELD_PATTERN_FEATURE_BRANCH: "^feature[/-][a-z]{2,}[a-zA-Z0-9._-]+$",
            FIELD_PATTERN_PR_BRANCH: "^(pull|pull\\-requests|pr)[/-]",
        },
    }


class Config:
    DEFAULT_PATH = "."
    COMMIT_FIELD_SEPARATOR = ";;;;;;;;"
    COMMIT_REGEX = (
        r"(.*)"
        + re.escape(COMMIT_FIELD_SEPARATOR)
        + r"(.*)"
        + re.escape(COMMIT_FIELD_SEPARATOR)
        + r"(.*)"
        + re.escape(COMMIT_FIELD_SEPARATOR)
        + r"(.*)"
        + re.escape(COMMIT_FIELD_SEPARATOR)
        + r"(.*)?"
    )

    def __init__(self):
        pass

    def _read_config(self):
        try:
            with open(self.file_path, "r") as stream:
                logger.debug("Config file found at '{}':".format(self.file_path))
                return yaml.safe_load(stream)
        except FileNotFoundError:
            logger.debug(
                "Config file not found at '{}'. Using default values:".format(
                    self.file_path
                )
            )
            return ConfigFile.DEFAULT.copy()

    @property
    def file_path(self):
        return f"{self.path}/{ConfigFile.NAME}"

    def load(self, path=DEFAULT_PATH):
        self.path = path
        config_default = ConfigFile.DEFAULT.copy()

        logger.debug("Default config:")
        logger.debug(config_default)

        config_read = self._read_config()
        logger.debug(config_read)

        config_regex_patterns = {
            **config_default[ConfigFile.FIELD_PATTERNS],
            **config_read[ConfigFile.FIELD_PATTERNS],
        }

        logger.debug("Resulting config:")
        logger.debug(config_regex_patterns)

        self.regex_patterns = dict(
            map(
                lambda item: (item[0], re.compile(item[1])),
                config_regex_patterns.items(),
            )
        )

        logger.debug(self.regex_patterns)

    def generate_config_file(self, path=DEFAULT_PATH):
        self.path = path
        with io.open(self.file_path, "w", encoding="utf8") as outfile:
            yaml.dump(
                ConfigFile.DEFAULT,
                outfile,
                default_flow_style=False,
                allow_unicode=True,
            )
        print(f"Created file '{self.file_path}'")


config = Config()
