#!/usr/bin/env python3
"""Validate a private network-state skill without changing it."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "profile.md",
    "references/devices.md",
    "references/services.md",
    "references/access-paths.md",
    "references/topology.md",
    "references/troubleshooting.md",
    "references/glossary.md",
)

MAX_SCAN_BYTES = 10 * 1024 * 1024
IGNORED_DIRECTORIES = {".git", "__pycache__"}

SECRET_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("OpenAI-style API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Stripe secret key", re.compile(r"\bsk_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    ("Tailscale authentication key", re.compile(r"\btskey-[A-Za-z0-9_-]{10,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("JWT-like token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("authorization header", re.compile(r"(?i)\bauthorization\s*:\s*(?:bearer|basic)\s+\S+")),
    ("credential in URL", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@")),
    (
        "credential assignment",
        re.compile(
            r"(?im)(?:^|[\s|`])(?:[a-z0-9.-]+[_-])?(?:password|passwd|passphrase|token|api[_ -]?key|auth[_ -]?key|private[_ -]?key|preshared[_ -]?key|pre-shared[_ -]?key|client[_ -]?secret|access[_ -]?key|secret[_ -]?access[_ -]?key|secret|cookie|session|recovery[_ -]?code)\s*[:=]\s*(?!unknown\b|none\b|<)[^\s`|]+"
        ),
    ),
)

RELATIVE_DEVICE_PATTERN = re.compile(
    r"(?im)^#{2,6}\s+(?:this machine|current machine|local machine|\u672c\u673a|\u8fd9\u53f0\u673a\u5668|\u5f53\u524d\u673a\u5668)\s*$"
)


def profile_field(text: str, label: str) -> str | None:
    match = re.search(
        rf"(?im)^-\s+{re.escape(label)}:\s+`?([^`\n]+?)`?\s*$",
        text,
    )
    if not match:
        return None
    return match.group(1).strip()


def default_state_path() -> Path:
    configured = os.environ.get("NETWORK_STATE_HOME")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".codex" / "skills" / "private-network-state"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check private skill structure and scan for obvious credential material."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=default_state_path(),
        help="Private skill directory (default: NETWORK_STATE_HOME or ~/.codex/skills/private-network-state)",
    )
    return parser.parse_args()


def profile_entries(root: Path) -> list[Path]:
    entries: list[Path] = []
    for current_dir, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(current_dir)
        kept_directories: list[str] = []
        for name in sorted(directory_names):
            path = current / name
            if path.is_symlink():
                entries.append(path)
            elif name not in IGNORED_DIRECTORIES:
                kept_directories.append(name)
        directory_names[:] = kept_directories
        entries.extend(current / name for name in sorted(file_names))
    return sorted(entries)


def main() -> int:
    args = parse_args()
    root = args.path.expanduser().resolve()
    skill_dir = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"Private skill directory does not exist: {root}", file=sys.stderr)
        return 2

    try:
        root.relative_to(skill_dir)
        errors.append("private skill is inside the installed plugin skill directory")
    except ValueError:
        pass

    for filename in REQUIRED_FILES:
        path = root / filename
        if not path.is_file():
            errors.append(f"missing required file: {filename}")

    profile_path = root / "profile.md"
    if profile_path.is_file():
        try:
            profile_text = profile_path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"profile.md: could not read synchronization settings: {exc}")
        else:
            sync_status = profile_field(profile_text, "Private GitHub synchronization")
            remote_name = profile_field(profile_text, "Git remote name")
            default_branch = profile_field(profile_text, "Default branch")

            if sync_status not in {"enabled", "disabled"}:
                errors.append("profile.md: private GitHub synchronization must be enabled or disabled")
            elif sync_status == "enabled":
                if not (root / ".gitignore").is_file():
                    errors.append("missing required file for private synchronization: .gitignore")
                if not remote_name or remote_name == "none":
                    errors.append("profile.md: enabled synchronization requires a Git remote name")
                if not default_branch or default_branch == "none":
                    errors.append("profile.md: enabled synchronization requires a default branch")
            else:
                if remote_name != "none" or default_branch != "none":
                    errors.append(
                        "profile.md: disabled synchronization requires remote name and branch to be none"
                    )

    if (root / ".git").exists():
        warnings.append("Git working files were checked, but Git history was not scanned")

    for path in profile_entries(root):
        relative = path.relative_to(root)
        if path.is_symlink():
            errors.append(f"{relative}: symbolic links are not allowed")
            continue
        if not path.is_file():
            continue
        if path.name == ".DS_Store" or path.name.startswith("._"):
            errors.append(f"{relative}: platform metadata file is not allowed")
            continue
        try:
            size = path.stat().st_size
            if size > MAX_SCAN_BYTES:
                errors.append(f"{relative}: file exceeds the 10 MiB scan limit")
                continue
            text = path.read_bytes().decode("utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"{relative}: could not read file: {exc}")
            continue

        if path.suffix.lower() == ".md" and RELATIVE_DEVICE_PATTERN.search(text):
            errors.append(f"{relative}: relative device heading is not allowed")
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                errors.append(f"{relative}:{line_number}: possible {label}")

        if os.name == "posix":
            file_mode = path.stat().st_mode & 0o777
            if file_mode & 0o077:
                warnings.append(f"{relative}: permissions are {file_mode:03o}; prefer 600")

    mode_warning = None
    if os.name == "posix":
        mode = root.stat().st_mode & 0o777
        if mode & 0o077:
            mode_warning = f"private skill directory permissions are {mode:03o}; prefer 700"

    if errors:
        print("Private skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("No files were changed.", file=sys.stderr)
        return 1

    print("Private skill validation passed.")
    print(f"path: {root}")
    print("credential scan: no obvious matches (heuristic, not a synchronization guarantee)")
    if mode_warning:
        warnings.insert(0, mode_warning)
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
