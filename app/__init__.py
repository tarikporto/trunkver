import logging

from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from os import getenv
from .git_reader import GitRepositoryReader
from .git_repository import GitRepository
from .config import config


def setup_logger(debug_flag=False):
    LOG_LEVEL = (
        logging.DEBUG if debug_flag else getenv("LOG_LEVEL", default=logging.WARNING)
    )
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=LOG_LEVEL,
    )


def get_cli_args() -> Namespace:
    parser = ArgumentParser(description="Calculates repository version.")

    parser.add_argument(
        "--path",
        "-p",
        default=config.DEFAULT_PATH,
        type=str,
        help="Path of GIT repository",
    )
    parser.add_argument(
        "--init",
        "-i",
        action="store_true",
        help="Generate trunkver configuration file (file will be created at working directory or, if --path argument is set, --path will be used as target path instead)",
    )
    parser.add_argument(
        "--version", "-v", action="version", version=version("trunkver")
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enter debug mode (more log messages)"
    )

    return parser.parse_args()


def run():
    args = get_cli_args()

    setup_logger(debug_flag=args.debug)
    logger = logging.getLogger(__name__)

    logger.debug(args)

    if args.init:
        config.generate_config_file(path=args.path)
        return

    config.load(path=args.path)

    git_repo_reader = GitRepositoryReader(args.path)
    repo = GitRepository(
        branch_name=git_repo_reader.read_branch_name(),
        commit_lines=git_repo_reader.read_commit_lines(
            sep=config.COMMIT_FIELD_SEPARATOR
        ),
    )

    print(repo.version)
