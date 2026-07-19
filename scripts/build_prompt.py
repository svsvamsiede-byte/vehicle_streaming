#!/usr/bin/env python3
"""
build_prompt.py

Builds a comprehensive AI coding prompt by reading WORKING_CONTEXT.md,
AI_CONTEXT.md, and DEVELOPMENT_RULES.md, then producing a single
instruction block ready to paste into an AI assistant.

Usage:
    python scripts/build_prompt.py > prompt.txt
    # Or simply:
    python scripts/build_prompt.py | pbcopy  # macOS
    python scripts/build_prompt.py | xclip -selection clipboard  # Linux
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
ROOT_DIR = Path(__file__).resolve().parent.parent

WORKING_CONTEXT_FILE = DOCS_DIR / "WORKING_CONTEXT.md"
AI_CONTEXT_FILE = DOCS_DIR / "AI_CONTEXT.md"
DEV_RULES_FILE = DOCS_DIR / "DEVELOPMENT_RULES.md"


# ── File Reading ───────────────────────────────────────────────────────────────

def read_file_safely(path: Path, label: str) -> str:
    """Read a file, printing a clear error if missing."""
    if not path.exists():
        print(f"[ERROR] {label} not found: {path}", file=sys.stderr)
        print(f"[HINT] Run `python scripts/extract_context.py` first to generate {WORKING_CONTEXT_FILE.name}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


# ── Prompt Assembly ────────────────────────────────────────────────────────────

def build_prompt(
    working_context: str,
    ai_context: str,
    dev_rules: str,
    include_repo_tree: bool = False,
) -> str:
    """
    Assemble the final prompt from all context sources.

    The prompt instructs the AI to:
    1. Read and understand the working context (current task)
    2. Follow the architecture and data contracts from AI_CONTEXT.md
    3. Adhere strictly to DEVELOPMENT_RULES.md
    4. Implement ONLY the current task without scope creep
    5. Output only modified files
    """
    lines: list[str] = []

    # ── Header ─────────────────────────────────────────────────────────────────
    lines.extend([
        "=" * 72,
        "AI CODING PROMPT — Production-Grade Streaming Lakehouse",
        "=" * 72,
        "",
        "You are a Senior Software Engineer implementing an atomic task",
        "for a production-grade streaming data platform.",
        "",
        "DO NOT modify PROJECT_STATE.md.",
        "DO NOT implement future tasks.",
        "DO NOT add nice-to-have features.",
        "",
        "-" * 72,
        "SECTION 1: CURRENT TASK CONTEXT",
        "-" * 72,
        "",
        working_context,
        "",
    ])

    # ── Architecture Context ─────────────────────────────────────────────────────
    lines.extend([
        "-" * 72,
        "SECTION 2: PROJECT ARCHITECTURE & DATA CONTRACTS",
        "-" * 72,
        "",
        "Read and internalize the following architecture context before",
        "implementing. Respect all data contracts, naming conventions,",
        "and technology decisions.",
        "",
        ai_context,
        "",
    ])

    # ── Development Rules ──────────────────────────────────────────────────────
    lines.extend([
        "-" * 72,
        "SECTION 3: DEVELOPMENT RULES (MUST FOLLOW)",
        "-" * 72,
        "",
        "Every line of code you produce MUST comply with ALL rules below.",
        "Violations are not acceptable.",
        "",
        dev_rules,
        "",
    ])

    # ── Final Instructions ─────────────────────────────────────────────────────
    lines.extend([
        "-" * 72,
        "SECTION 4: IMPLEMENTATION INSTRUCTIONS",
        "-" * 72,
        "",
        "1. Implement ONLY the task described in Section 1.",
        "2. Follow ALL rules in Section 3 without exception.",
        "3. Respect ALL architecture decisions and data contracts in Section 2.",
        "4. Output ONLY the file(s) required by the current task.",
        "5. Provide COMPLETE file contents — no partial snippets or diffs.",
        "6. Include docstrings (Google style) for all public APIs.",
        "7. Include type hints on all functions and classes.",
        "8. Use Python logging; never use print().",
        "9. Add unit tests if the file contains business logic.",
        "10. Run ruff check, ruff format, and mypy before finishing.",
        "11. Do not create placeholder implementations or TODO comments.",
        "12. Do not modify unrelated files.",
        "13. Do not update PROJECT_STATE.md — that is done separately.",
        "",
        "=" * 72,
        "END OF PROMPT",
        "=" * 72,
        "",
    ])

    return "\n".join(lines)


# ── Repository Tree (Optional) ─────────────────────────────────────────────────

def get_repo_tree(root: Path, max_depth: int = 3) -> str:
    """
    Generate a simple tree representation of the repository.
    Respects .gitignore if present.
    """
    lines: list[str] = ["Repository Structure:", ""]

    def walk(current: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            return

        try:
            entries = sorted(
                [e for e in current.iterdir() if not e.name.startswith(".")],
                key=lambda e: (not e.is_dir(), e.name.lower()),
            )
        except PermissionError:
            return

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                walk(entry, prefix + extension, depth + 1)

    walk(root, "", 0)
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> int:
    """Parse arguments and build the prompt."""
    parser = argparse.ArgumentParser(
        description="Build a comprehensive AI coding prompt from project context files.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write prompt to file instead of stdout",
    )
    parser.add_argument(
        "--tree",
        "-t",
        action="store_true",
        help="Include repository tree in the prompt",
    )
    parser.add_argument(
        "--max-depth",
        "-d",
        type=int,
        default=3,
        help="Maximum depth for repository tree (default: 3)",
    )

    args = parser.parse_args()

    # Read all context files
    print("[INFO] Reading WORKING_CONTEXT.md...", file=sys.stderr)
    working_context = read_file_safely(WORKING_CONTEXT_FILE, "Working context")

    print("[INFO] Reading AI_CONTEXT.md...", file=sys.stderr)
    ai_context = read_file_safely(AI_CONTEXT_FILE, "AI context")

    print("[INFO] Reading DEVELOPMENT_RULES.md...", file=sys.stderr)
    dev_rules = read_file_safely(DEV_RULES_FILE, "Development rules")

    # Optional tree
    tree_section = ""
    if args.tree:
        print("[INFO] Generating repository tree...", file=sys.stderr)
        tree_section = "\n" + get_repo_tree(ROOT_DIR, args.max_depth) + "\n"

    # Build prompt
    print("[INFO] Assembling prompt...", file=sys.stderr)
    prompt = build_prompt(working_context, ai_context, dev_rules, args.tree)

    if tree_section:
        # Insert tree before final instructions
        insert_point = prompt.find("-" * 72 + "\nSECTION 4")
        if insert_point != -1:
            prompt = prompt[:insert_point] + tree_section + prompt[insert_point:]

    # Output
    if args.output:
        args.output.write_text(prompt, encoding="utf-8")
        print(f"[SUCCESS] Prompt written to {args.output}", file=sys.stderr)
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
