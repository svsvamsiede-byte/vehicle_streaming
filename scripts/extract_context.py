#!/usr/bin/env python3
"""
extract_context.py

Reads PROJECT_STATE.md from the docs/ directory,
locates the current task, extracts relevant context,
and writes it to WORKING_CONTEXT.md.

Usage:
    python scripts/extract_context.py
"""

from __future__ import annotations
import re
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
INPUT_FILE = DOCS_DIR / "PROJECT_STATE.md"
OUTPUT_FILE = DOCS_DIR / "WORKING_CONTEXT.md"


# ── Helpers ────────────────────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    """Read and return the contents of a file."""
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    """Write content to a file."""
    path.write_text(content, encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    """
    Extract content under a markdown heading.
    Supports headings like ## Heading, ### Heading, etc.
    Stops at the next heading of the same or higher level.
    """
    pattern = rf"^(#{{1,6}})\s*{re.escape(heading)}\s*$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""

    level = len(match.group(1))
    start = match.end()

    next_heading = re.search(rf"^#{{1,{level}}}\s", text[start:], re.MULTILINE)
    if next_heading:
        end = start + next_heading.start()
    else:
        end = len(text)

    return text[start:end].strip()


def _parse_current_working_context_table(text: str) -> dict[str, str]:
    """Parse the Current Working Context table into a key/value mapping."""
    mapping: dict[str, str] = {}
    section = extract_section(text, "Current Working Context")
    if not section:
        return mapping

    for line in section.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # Filter out empty strings from leading/trailing pipes
        parts = [p for p in parts if p]
        if len(parts) < 2 or parts[0].lower() == "field":
            continue
        key = parts[0]
        value = " | ".join(parts[1:])
        mapping[key] = value

    return mapping


def extract_current_task(text: str) -> dict[str, str]:
    """
    Locate the Current Working Context section and extract all relevant fields.
    """
    ctx = _parse_current_working_context_table(text)
    result: dict[str, str] = {}

    result["task"] = ctx.get("Current task", "N/A")
    result["acceptance_criteria"] = ctx.get("Acceptance criteria", "N/A")
    result["dependencies"] = ctx.get("Dependencies", "N/A")
    result["branch"] = ctx.get("Branch", "N/A")
    result["relevant_files"] = ctx.get("Expected files", "N/A")

    # Architecture decisions come from a dedicated section, not the context table
    arch_section = extract_section(text, "Relevant Architecture Decisions")
    if not arch_section:
        arch_section = extract_section(text, "Architecture Decisions")
    result["architecture_decisions"] = arch_section if arch_section else "N/A"

    return result


def build_working_context(data: dict[str, str]) -> str:
    """Build the WORKING_CONTEXT.md content from extracted data."""
    lines = [
        "# Working Context",
        "",
        "> Auto-generated from PROJECT_STATE.md",
        "",
        "---",
        "",
        "## Task",
        "",
        data.get("task", "N/A"),
        "",
        "## Acceptance Criteria",
        "",
        data.get("acceptance_criteria", "N/A"),
        "",
        "## Dependencies",
        "",
        data.get("dependencies", "N/A"),
        "",
        "## Branch",
        "",
        data.get("branch", "N/A"),
        "",
        "## Relevant Files",
        "",
        data.get("relevant_files", "N/A"),
        "",
        "## Relevant Architecture Decisions",
        "",
        data.get("architecture_decisions", "N/A"),
        "",
    ]
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    """Run the context extraction."""
    if not INPUT_FILE.exists():
        print(f"[ERROR] Input file not found: {INPUT_FILE}")
        print("Please ensure PROJECT_STATE.md exists in the docs/ directory.")
        return 1

    print(f"[INFO] Reading {INPUT_FILE}...")
    state_text = read_file(INPUT_FILE)

    print("[INFO] Extracting current task context...")
    extracted = extract_current_task(state_text)

    print("[INFO] Building WORKING_CONTEXT.md...")
    context_md = build_working_context(extracted)

    write_file(OUTPUT_FILE, context_md)
    print(f"[SUCCESS] Written to {OUTPUT_FILE}")

    print("\n--- Extracted Context ---")
    for key, value in extracted.items():
        preview = value[:60].replace("\n", " ") + ("..." if len(value) > 60 else "")
        print(f"  {key}: {preview}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
