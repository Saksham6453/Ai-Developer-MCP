import subprocess

from server.workspace import get_workspace_path


def git_status():
    workspace = get_workspace_path()

    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip() or "Working tree clean."


def git_diff():
    workspace = get_workspace_path()

    result = subprocess.run(
        ["git", "diff"],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip() or "No changes."


def git_log():
    workspace = get_workspace_path()

    result = subprocess.run(
        [
            "git",
            "log",
            "-10",
            "--oneline",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip() or "No commits found."