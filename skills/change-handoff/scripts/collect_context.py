#!/usr/bin/env python3
"""Collect local Git revision and path state; never fetch or write repo files."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


class ContextError(Exception):
    """An expected collection failure with a safe user-facing message."""


def git(repo, *args):
    env = os.environ.copy()
    env["GIT_OPTIONAL_LOCKS"] = "0"
    # Explicit paths must not be redirected by a caller's Git environment.
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-C", str(repo), *args],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False,
        )
    except FileNotFoundError as exc:
        raise ContextError("Git executable is unavailable") from exc
    if result.returncode:
        # Do not echo arbitrary repository/configuration output into reports.
        raise ContextError("Git could not complete: " + args[0])
    return result.stdout


def decode(value):
    return value.decode("utf-8", errors="surrogateescape")


def resolve_commit(repo, ref):
    if not ref or ref.startswith("-"):
        raise ContextError("Commit reference must be nonempty and not an option")
    try:
        return decode(git(repo, "rev-parse", "--verify", "--end-of-options",
                          ref + "^{commit}")).strip()
    except ContextError as exc:
        raise ContextError("Commit reference is unavailable: " + ref) from exc


def changes(repo, *args):
    # No rename inference: paths are independently added/deleted for stable output.
    raw = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
              "--name-status", "-z", *args, "--")
    fields = raw.split(b"\0")
    if fields[-1] == b"":
        fields.pop()
    return [{"status": decode(fields[i]), "path": decode(fields[i + 1])}
            for i in range(0, len(fields), 2)]


def collect(repo, base=None):
    root = decode(git(repo, "rev-parse", "--show-toplevel")).strip()
    root_path = Path(root)
    try:
        head = resolve_commit(root_path, "HEAD")
    except ContextError:
        # Only an unborn symbolic HEAD is an expected missing-HEAD state.
        symbolic = decode(git(root_path, "symbolic-ref", "-q", "HEAD")).strip()
        refs = git(root_path, "for-each-ref", "--format=%(refname)", symbolic)
        if refs.strip():
            raise ContextError("HEAD exists but cannot be resolved")
        head = None
    base_sha = resolve_commit(root_path, base) if base is not None else None
    if base_sha and not head:
        raise ContextError("Cannot compare a base commit without HEAD")
    staged_args = ("--cached", head) if head else ("--cached",)
    staged = changes(root_path, *staged_args)
    unstaged = changes(root_path)
    untracked = [decode(p) for p in git(
        root_path, "ls-files", "--others", "--exclude-standard", "-z"
    ).split(b"\0") if p]
    unmerged = [decode(p) for p in git(
        root_path, "diff", "--name-only", "--diff-filter=U", "-z", "--"
    ).split(b"\0") if p]
    return {
        "schema_version": 1,
        "repository": root,
        "base": base_sha,
        "head": head,
        "committed_changes": changes(root_path, base_sha, head) if base_sha else None,
        "staged_changes": staged,
        "unstaged_changes": unstaged,
        "untracked_paths": untracked,
        "unmerged_paths": unmerged,
        "has_uncommitted_changes": bool(staged or unstaged or untracked),
        "limitations": [
            "Path state is not evidence of task ownership, behavior, or test results.",
            "No base means committed comparison is unavailable, not empty.",
            "Ignored files and untracked file contents are not inspected.",
            "Submodule internals and unsaved editor content are not inspected.",
            "Collection is not atomic; rerun if the repository changes concurrently.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository path (default: .)")
    parser.add_argument("--base", help="Explicit task base ref; never inferred")
    args = parser.parse_args()
    try:
        context = collect(args.repo, args.base)
    except (ContextError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1
    print(json.dumps(context, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
