from os import devnull
from subprocess import call, check_output, STDOUT
from typing import List
from .errors import GitRepositoryNotExistsError


class GitRepositoryReader:
    def __init__(self, path="."):
        self.path = path
        if not self._git_repo_exists():
            raise GitRepositoryNotExistsError(
                "GIT repository not detected on path '{}'".format(self.path)
            )

    def _git_repo_exists(self) -> bool:
        return (
            call(
                ["git", f"--git-dir={self.path}/.git", "branch"],
                stderr=STDOUT,
                stdout=open(devnull, "w"),
            )
            == 0
        )

    def read_commit_lines(self, sep=":::") -> List[str]:
        return (
            check_output(
                [
                    "git",
                    f"--git-dir={self.path}/.git",
                    "log",
                    f"--pretty=format:%h{sep}%H{sep}%at{sep}%s{sep}%D",
                ],
                stderr=STDOUT,
            )
            .decode("utf-8")
            .split("\n")
        )

    def read_branch_name(self) -> str:
        return check_output(
            ["git", f"--git-dir={self.path}/.git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).decode("utf-8")
