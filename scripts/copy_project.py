from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_IGNORE = (".git", "__pycache__", ".pytest_cache", ".streamlit", "local_copy", "project_copy")


def _build_ignore(include_git: bool, extra_ignore: Sequence[str] | None) -> Iterable[str] | None:
    """Build ignore patterns for copytree.

    When include_git is True, we return None to avoid ignoring the .git directory.
    Otherwise we merge default patterns with any user provided ones.
    """

    if include_git:
        return None
    if extra_ignore:
        return tuple(DEFAULT_IGNORE) + tuple(extra_ignore)
    return DEFAULT_IGNORE


def copy_project(destination: Path, include_git: bool = False, extra_ignore: Sequence[str] | None = None) -> Path:
    source_root = Path(__file__).resolve().parent.parent
    dest_path = Path(destination).expanduser().resolve()

    if dest_path.exists():
        raise FileExistsError(f"Destination already exists: {dest_path}")

    ignore_patterns = _build_ignore(include_git, extra_ignore)
    shutil.copytree(source_root, dest_path, ignore=shutil.ignore_patterns(*(ignore_patterns or ())))
    return dest_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy the entire project to a local directory.")
    parser.add_argument(
        "destination",
        nargs="?",
        default="local_copy",
        help="Target directory name or path for the copied project (default: local_copy)",
    )
    parser.add_argument(
        "--include-git",
        action="store_true",
        help="Include the .git directory when copying (default: False)",
    )
    parser.add_argument(
        "--ignore",
        action="append",
        dest="extra_ignore",
        default=[],
        help="Additional glob patterns to ignore (can be specified multiple times)",
    )
    args = parser.parse_args()

    dest_path = copy_project(
        Path(args.destination), include_git=args.include_git, extra_ignore=args.extra_ignore
    )
    print(f"Copied project to {dest_path}")


if __name__ == "__main__":
    main()
