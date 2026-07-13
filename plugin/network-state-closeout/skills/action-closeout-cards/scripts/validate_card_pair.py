#!/usr/bin/env python3
"""Validate a network-state status/process card handoff pair without changing it."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MAX_BYTES = 2 * 1024 * 1024
ALLOWED_STATES = {"pending", "applied", "blocked", "skipped"}
ALLOWED_DETAILS = {"private", "alias-only"}
ALLOWED_METHODS = {"user-confirmed", "observed", "config-confirmed"}
HANDOFF_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{5,79}$")
ISO_TIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")
UUID_PATTERN = re.compile(
    r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
)
IPV4_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?![A-Za-z0-9])"
)
MAC_PATTERN = re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])")
URL_PATTERN = re.compile(r"(?i)\b(?:https?|ssh|git)://[^\s`<>]+")

SECRET_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("API key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("JWT-like token", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("credential URL", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@")),
    (
        "credential assignment",
        re.compile(
            r"(?i)\b(?:password|passwd|token|api[_ -]?key|auth[_ -]?key|secret|cookie)\b\s*[:=]\s*(?!unknown\b|none\b|<)[^\s`]+"
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a network-state card handoff pair.")
    parser.add_argument("--status-card", type=Path, required=True)
    parser.add_argument("--process-card", type=Path, required=True)
    return parser.parse_args()


def read_card(path: Path, label: str, errors: list[str]) -> str:
    if path.is_symlink():
        errors.append(f"{label}: symbolic links are not allowed")
        return ""
    if not path.is_file():
        errors.append(f"{label}: file does not exist: {path}")
        return ""
    if path.stat().st_size > MAX_BYTES:
        errors.append(f"{label}: file exceeds the 2 MiB limit")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: could not read UTF-8 text: {exc}")
        return ""


def field(text: str, label: str) -> str | None:
    match = re.search(
        rf"(?im)^\|\s*{re.escape(label)}\s*\|\s*`?([^|`\n]+?)`?\s*\|\s*$",
        text,
    )
    return match.group(1).strip() if match else None


def handoff_section(text: str) -> str | None:
    match = re.search(r"(?ms)^## Network-state handoff\s*$\n(.*?)(?=^##\s|\Z)", text)
    return match.group(1) if match else None


def check_card(
    text: str,
    expected_role: str,
    label: str,
    errors: list[str],
) -> dict[str, str]:
    values: dict[str, str] = {}
    section = handoff_section(text)
    if section is None:
        errors.append(f"{label}: missing '## Network-state handoff'")
        return values

    required_headings = (
        "### Durable state candidates"
        if expected_role == "status"
        else "### Durable route and troubleshooting candidates"
    )
    if required_headings not in section:
        errors.append(f"{label}: missing '{required_headings}'")
    if "### Ingestion receipt" not in section:
        errors.append(f"{label}: missing '### Ingestion receipt'")
    if re.search(r"<[^>\n]{1,200}>", section):
        errors.append(f"{label}: unresolved placeholder in handoff section")

    for name in (
        "Handoff ID",
        "Card role",
        "Ingestion state",
        "Detail level",
        "Verified at",
        "Verification method",
        "Target records",
        "Applied at",
        "Applied targets",
        "Network-state validation",
        "Network-state commit",
        "Block reason",
    ):
        value = field(section, name)
        if value is None:
            errors.append(f"{label}: missing handoff field '{name}'")
        else:
            values[name] = value

    if values.get("Card role") != expected_role:
        errors.append(f"{label}: Card role must be {expected_role}")
    if values.get("Ingestion state") not in ALLOWED_STATES:
        errors.append(f"{label}: unsupported Ingestion state")
    if values.get("Detail level") not in ALLOWED_DETAILS:
        errors.append(f"{label}: Detail level must be private or alias-only")
    if values.get("Verification method") not in ALLOWED_METHODS:
        errors.append(f"{label}: unsupported Verification method")
    if not ISO_TIME_PATTERN.match(values.get("Verified at", "")):
        errors.append(f"{label}: Verified at must be an ISO 8601 timestamp")
    if not HANDOFF_ID_PATTERN.match(values.get("Handoff ID", "")):
        errors.append(f"{label}: Handoff ID must be a stable lower-case hyphenated ID")
    if values.get("Target records") in {None, "none", "unknown"}:
        errors.append(f"{label}: Target records must name at least one canonical target")

    if values.get("Ingestion state") == "applied":
        if not ISO_TIME_PATTERN.match(values.get("Applied at", "")):
            errors.append(f"{label}: applied handoff requires an ISO Applied at value")
        if values.get("Applied targets") in {None, "none", "unknown"}:
            errors.append(f"{label}: applied handoff requires Applied targets")
        if values.get("Network-state validation") != "passed":
            errors.append(f"{label}: applied handoff requires passed network-state validation")
        commit = values.get("Network-state commit", "")
        if commit != "local-only" and not re.fullmatch(r"[0-9a-f]{7,40}", commit):
            errors.append(f"{label}: applied handoff requires a commit hash or local-only")
    if values.get("Ingestion state") == "blocked" and values.get("Block reason") in {
        None,
        "none",
        "unknown",
    }:
        errors.append(f"{label}: blocked handoff requires Block reason")

    for secret_label, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{label}:{line}: possible {secret_label}")
    for match in UUID_PATTERN.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: UUID values are not allowed")

    if values.get("Detail level") == "alias-only":
        for endpoint_label, pattern in (
            ("IPv4 address", IPV4_PATTERN),
            ("MAC address", MAC_PATTERN),
            ("concrete URL", URL_PATTERN),
        ):
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label}:{line}: alias-only card contains {endpoint_label}")

    return values


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    status_text = read_card(args.status_card, "status card", errors)
    process_text = read_card(args.process_card, "process card", errors)
    status = check_card(status_text, "status", "status card", errors)
    process = check_card(process_text, "process", "process card", errors)

    for name in (
        "Handoff ID",
        "Ingestion state",
        "Detail level",
        "Verified at",
        "Verification method",
        "Applied at",
        "Applied targets",
        "Network-state validation",
        "Network-state commit",
        "Block reason",
    ):
        if status.get(name) and process.get(name) and status[name] != process[name]:
            errors.append(f"card pair: {name} values do not match")

    if errors:
        print("Card pair validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Card pair validation passed.")
    print(f"handoff_id: {status['Handoff ID']}")
    print(f"ingestion_state: {status['Ingestion state']}")
    print(f"detail_level: {status['Detail level']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
