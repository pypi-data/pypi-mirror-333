import re
import subprocess
from typing import Iterable


class GitBranch:
    def __init__(self, name: str, sha: str) -> None:
        self.name = name
        self.sha = sha

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"GitBranch(name='{self.name}', sha='{self.sha}')"


def _run_cmd(command: list[str]) -> list[str]:
    try:
        return [
            line.decode().strip()
            for line in subprocess.check_output(command).splitlines()
        ]
    except subprocess.CalledProcessError as exc:
        print(f"Error: {exc}")
        return []


def _check_regex(regex: str | Iterable[str] | None, value: str) -> bool:
    if regex:
        if isinstance(regex, Iterable):
            return all(re.search(r, value) for r in regex)
        return bool(re.search(regex, value))
    return True


def get_branches(regex: str | Iterable[str] | None = None) -> list[GitBranch]:
    # run git shell command to get all branches
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    return [branch for branch in branches if _check_regex(regex, branch.name)]


def get_parents(
    child_branch: GitBranch, regex: str | Iterable[str] | None = None
) -> list[GitBranch]:
    # run git shell command to get all branches that contain a specific branch
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--contains",
            child_branch.sha,
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    # filter out child branch
    branches = [branch for branch in branches if branch.sha != child_branch.sha]

    return [branch for branch in branches if _check_regex(regex, branch.name)]


def get_merged(name: str, regex: str | Iterable[str] | None = None) -> list[GitBranch]:
    # run git shell command to get all branches that contain a specific branch
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--merged",
            name,
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    return [branch for branch in branches if _check_regex(regex, branch.name)]
