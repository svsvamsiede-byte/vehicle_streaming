#!/usr/bin/env python3
"""Build a task-aware AI coding prompt from project context files.

This script assembles a focused prompt for the current task by reading
WORKING_CONTEXT.md, AI_CONTEXT.md, and DEVELOPMENT_RULES.md, then including
only the sections relevant to the task instead of concatenating the entire
context every time.

Usage:
    python scripts/build_prompt.py > prompt.txt
    python scripts/build_prompt.py --full > prompt.txt
    python scripts/build_prompt.py | pbcopy  # macOS
"""

from __future__ import annotations

import argparse
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# ── Configuration ──────────────────────────────────────────────────────────────

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
ROOT_DIR = Path(__file__).resolve().parent.parent

WORKING_CONTEXT_FILE = DOCS_DIR / "WORKING_CONTEXT.md"
AI_CONTEXT_FILE = DOCS_DIR / "AI_CONTEXT.md"
DEV_RULES_FILE = DOCS_DIR / "DEVELOPMENT_RULES.md"

LOGGER = logging.getLogger(__name__)

# Keywords found in the task text/relevant files mapped to relevance tags.
TASK_KEYWORDS: dict[str, str] = {
    ".env": "env",
    "docker-compose": "docker",
    "docker": "docker",
    "compose": "docker",
    "KAFKA_PORT": "env",
    "kafka": "kafka",
    "flink": "flink",
    "iceberg": "iceberg",
    "minio": "minio",
    "trino": "trino",
    "grafana": "grafana",
    "prometheus": "prometheus",
    "tests": "tests",
    "test": "tests",
    "producer": "producer",
    "simulator": "producer",
}

# Map relevance tags to AI_CONTEXT.md sections.
AI_SECTION_RELEVANCE: dict[str, list[str]] = {
    "env": [
        "Repository Architecture",
        "Architectural Principles",
    ],
    "docker": [
        "Repository Architecture",
        "Architectural Principles",
    ],
    "kafka": [
        "Architecture Overview",
        "Data Contracts",
    ],
    "flink": [
        "Architecture Overview",
        "Data Contracts",
        "Performance Goals",
    ],
    "iceberg": [
        "Architecture Overview",
        "Data Contracts",
    ],
    "minio": [
        "Architecture Overview",
    ],
    "trino": [
        "Architecture Overview",
    ],
    "grafana": [
        "Architectural Principles",
        "Monitoring Philosophy",
    ],
    "prometheus": [
        "Architectural Principles",
        "Monitoring Philosophy",
    ],
    "tests": [
        "Repository Architecture",
        "Repository Conventions",
    ],
    "producer": [
        "Architecture Overview",
        "Repository Architecture",
        "Data Contracts",
    ],
}

# Map relevance tags to DEVELOPMENT_RULES.md sections.
RULES_SECTION_RELEVANCE: dict[str, list[str]] = {
    "env": [
        "8. Configuration",
        "17. Security",
    ],
    "docker": [
        "4. Architecture",
        "8. Configuration",
        "9. Docker",
        "17. Security",
    ],
    "kafka": [
        "8. Configuration",
        "10. Kafka",
    ],
    "flink": [
        "4. Architecture",
        "8. Configuration",
        "11. Flink",
        "16. Performance",
    ],
    "iceberg": [
        "8. Configuration",
        "13. Code Quality",
    ],
    "minio": [
        "8. Configuration",
        "17. Security",
    ],
    "trino": [
        "8. Configuration",
    ],
    "grafana": [
        "8. Configuration",
    ],
    "prometheus": [
        "8. Configuration",
    ],
    "tests": [
        "3. Existing Code",
        "12. Testing",
        "13. Code Quality",
    ],
    "producer": [
        "4. Architecture",
        "5. Python Standards",
        "6. Logging",
        "7. Error Handling",
        "8. Configuration",
        "10. Kafka",
    ],
}

# Sections that are always included regardless of task keywords.
ALWAYS_AI_SECTIONS: list[str] = ["Architectural Principles"]
ALWAYS_RULES_SECTIONS: list[str] = [
    "1. General Principles",
    "2. Scope Rules",
    "18. AI-Specific Rules",
    "19. Completion Checklist",
]


# ── Data Classes ───────────────────────────────────────────────────────────────


@dataclass
class TaskContext:
    """Structured representation of the current task from WORKING_CONTEXT.md."""

    task_id: str = ""
    title: str = ""
    status: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    branch: str = ""
    relevant_files: list[str] = field(default_factory=list)
    architecture_decisions: list[str] = field(default_factory=list)
    raw_text: str = ""


# ── File Reading ───────────────────────────────────────────────────────────────


def read_file_safely(path: Path, label: str) -> str:
    """Read a file, raising a clear error if it is missing.

    Args:
        path: Path to the file to read.
        label: Human-readable label for the file.

    Returns:
        File contents as a string.

    Raises:
        SystemExit: If the file does not exist.
    """
    if not path.exists():
        LOGGER.error("%s not found: %s", label, path)
        LOGGER.error(
            "Run `python scripts/extract_context.py` first to generate %s",
            WORKING_CONTEXT_FILE.name,
        )
        raise SystemExit(1)
    return path.read_text(encoding="utf-8")


# ── Markdown Parsing ───────────────────────────────────────────────────────────


def parse_markdown_sections(text: str) -> dict[str, str]:
    """Split markdown text into top-level (#) sections.

    Args:
        text: Markdown document text.

    Returns:
        Mapping of section title to section body (excluding the title line).
    """
    sections: dict[str, str] = {}
    current_title: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("# "):
            if current_title is not None:
                sections[current_title] = "\n".join(current_lines).strip("\n")
            current_title = line[2:].strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections[current_title] = "\n".join(current_lines).strip("\n")

    return sections


def extract_section(text: str, header: str) -> str:
    """Extract the body of a markdown section by its header.

    Args:
        text: Markdown document text.
        header: Section header without leading hashes.

    Returns:
        Section body, or an empty string if not found.
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)", re.M | re.S
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def parse_bullet_list(text: str) -> list[str]:
    """Parse a markdown list block into items.

    Handles both bullet/numbered lists and plain line- or semicolon-separated
    blocks (as produced by ``extract_context.py`` for some fields).

    Args:
        text: Markdown list block.

    Returns:
        List items with leading markers stripped.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bullet_pattern = re.compile(r"^[-*]\s+(.*)")
    number_pattern = re.compile(r"^[0-9]+\.\s+(.*)")

    has_markers = any(
        bullet_pattern.match(line) or number_pattern.match(line) for line in lines
    )
    if has_markers:
        items: list[str] = []
        for line in lines:
            match = bullet_pattern.match(line) or number_pattern.match(line)
            if match:
                items.append(match.group(1).strip())
        return items

    # Plain text separated by newlines or semicolons.
    items = [item.strip() for item in re.split(r"[;\n]", text) if item.strip()]
    return items


def parse_architecture_decisions(text: str) -> list[str]:
    """Parse architecture decision rows from a markdown table.

    Args:
        text: Markdown text containing the decisions table.

    Returns:
        Raw table rows for decisions, excluding the header/separator.
    """
    decisions: list[str] = []
    in_decisions = False
    for line in text.splitlines():
        if "| Decision ID |" in line:
            in_decisions = True
            continue
        if in_decisions and line.startswith("| AD-"):
            decisions.append(line.strip())
    return decisions


def extract_task_context(working_context: str) -> TaskContext:
    """Parse WORKING_CONTEXT.md into a structured TaskContext.

    Args:
        working_context: Raw contents of WORKING_CONTEXT.md.

    Returns:
        Structured task context.
    """
    task_text = extract_section(working_context, "Task")
    task_id, _, title = task_text.partition(" — ")
    if not title:
        title = task_text

    acceptance = parse_bullet_list(
        extract_section(working_context, "Acceptance Criteria")
    )
    dependencies = parse_bullet_list(extract_section(working_context, "Dependencies"))
    branch = extract_section(working_context, "Branch")
    relevant_files = parse_bullet_list(
        extract_section(working_context, "Relevant Files")
    )
    decisions = parse_architecture_decisions(working_context)

    return TaskContext(
        task_id=task_id.strip(),
        title=title.strip(),
        status=extract_section(working_context, "Status"),
        acceptance_criteria=acceptance,
        dependencies=dependencies,
        branch=branch.strip(),
        relevant_files=relevant_files,
        architecture_decisions=decisions,
        raw_text=working_context,
    )


# ── Task-aware Section Selection ───────────────────────────────────────────────


def _find_keyword_matches(haystack: str, keywords: dict[str, str]) -> set[str]:
    """Find keyword matches, preferring longer keywords over their substrings.

    Args:
        haystack: Lowercased text to search.
        keywords: Mapping from keyword substring to relevance tag.

    Returns:
        Set of relevance tags derived from the haystack.
    """
    sorted_keywords = sorted(
        keywords.items(), key=lambda item: len(item[0]), reverse=True
    )
    covered_spans: list[tuple[int, int]] = []
    tags: set[str] = set()

    for keyword, tag in sorted_keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for match in pattern.finditer(haystack):
            start, end = match.span()
            if any(
                c_start <= start and end <= c_end for c_start, c_end in covered_spans
            ):
                continue
            tags.add(tag)
            covered_spans.append((start, end))

    return tags


def extract_task_keywords(task: TaskContext) -> set[str]:
    """Derive relevance keywords from the task context.

    Keywords from the task title, ID, relevant files, and acceptance criteria
    are considered primary. Keywords from dependencies, branch, and architecture
    decisions are secondary and only used when no primary keywords are found.
    Longer keywords are preferred over their substrings (e.g., ``KAFKA_PORT``
    maps to ``env`` rather than also pulling in Kafka rules).

    Args:
        task: Parsed task context.

    Returns:
        Set of relevance tags (e.g., "docker", "kafka", "flink").
    """
    primary_haystack = " ".join(
        [
            task.task_id,
            task.title,
            " ".join(task.relevant_files),
            " ".join(task.acceptance_criteria),
        ]
    ).lower()

    secondary_haystack = " ".join(
        [
            " ".join(task.dependencies),
            task.branch,
            " ".join(task.architecture_decisions),
        ]
    ).lower()

    primary_tags = _find_keyword_matches(primary_haystack, TASK_KEYWORDS)
    secondary_tags = _find_keyword_matches(secondary_haystack, TASK_KEYWORDS)

    return primary_tags if primary_tags else secondary_tags


def _normalize_section_name(name: str) -> str:
    """Normalize a section name for matching.

    Args:
        name: Section name from markdown.

    Returns:
        Lowercased, whitespace-normalized name.
    """
    return " ".join(name.split()).lower()


def select_relevant_sections(
    sections: dict[str, str],
    keywords: set[str],
    relevance_map: dict[str, list[str]],
    always_include: list[str],
) -> dict[str, str]:
    """Pick markdown sections relevant to the current task keywords.

    Args:
        sections: Parsed markdown sections.
        keywords: Relevance tags derived from the task.
        relevance_map: Mapping from tag to list of section names.
        always_include: Section names to always include.

    Returns:
        Ordered mapping of selected section names to bodies.
    """
    normalized: dict[str, str] = {_normalize_section_name(k): k for k in sections}
    selected_names: list[str] = []

    for tag in sorted(keywords):
        for name in relevance_map.get(tag, []):
            if name not in selected_names:
                selected_names.append(name)

    for name in always_include:
        if name not in selected_names:
            selected_names.append(name)

    result: dict[str, str] = {}
    for name in selected_names:
        normalized_name = _normalize_section_name(name)
        if normalized_name in normalized:
            original_name = normalized[normalized_name]
            result[original_name] = sections[original_name]
        else:
            LOGGER.warning("Referenced section not found: %s", name)
    return result


def filter_architecture_decisions(
    decisions: list[str], keywords: set[str]
) -> list[str]:
    """Return architecture decisions that mention any task keyword.

    Matching uses word boundaries to avoid substring false positives.

    Args:
        decisions: Raw decision table rows.
        keywords: Relevance tags derived from the task.

    Returns:
        Decision rows relevant to the task; all decisions if no keywords match.
    """
    if not keywords or not decisions:
        return decisions

    relevant: list[str] = []
    for row in decisions:
        if any(
            re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE).search(row)
            for keyword in keywords
        ):
            relevant.append(row)

    # Fallback to all decisions if the filter removed everything.
    return relevant if relevant else decisions


# ── Prompt Assembly ────────────────────────────────────────────────────────────


def _format_architecture_decisions(decisions: list[str]) -> str:
    """Format decision rows back into a markdown table fragment.

    Args:
        decisions: Raw decision table rows.

    Returns:
        Markdown table with header and separator, or empty string.
    """
    if not decisions:
        return ""
    header = "| Decision ID | Date | Decision | Reason | Impact |"
    separator = "|-------------|------|----------|--------|--------|"
    return "\n".join([header, separator, *decisions])


def _format_task_context(task: TaskContext) -> str:
    """Render the current task context as markdown.

    Args:
        task: Parsed task context.

    Returns:
        Markdown representation of the task context.
    """
    lines: list[str] = [
        "# Working Context",
        "",
        "> Auto-generated from PROJECT_STATE.md",
        "",
    ]

    if task.status:
        lines.extend(["## Status", "", task.status, ""])

    lines.extend(
        [
            "## Task",
            "",
            f"{task.task_id} — {task.title}" if task.task_id else task.title,
            "",
        ]
    )

    if task.acceptance_criteria:
        lines.extend(["## Acceptance Criteria", ""])
        lines.extend(f"- {item}" for item in task.acceptance_criteria)
        lines.append("")

    if task.dependencies:
        lines.extend(["## Dependencies", ""])
        lines.extend(f"- {item}" for item in task.dependencies)
        lines.append("")

    if task.branch:
        lines.extend(["## Branch", "", task.branch, ""])

    if task.relevant_files:
        lines.extend(["## Relevant Files", ""])
        lines.extend(f"- {item}" for item in task.relevant_files)
        lines.append("")

    if task.architecture_decisions:
        lines.extend(["## Relevant Architecture Decisions", ""])
        lines.append(_format_architecture_decisions(task.architecture_decisions))
        lines.append("")

    return "\n".join(lines)


def _format_sections(sections: dict[str, str]) -> str:
    """Render selected markdown sections back into a document.

    Args:
        sections: Mapping of section title to body.

    Returns:
        Markdown document fragment.
    """
    parts: list[str] = []
    for title, body in sections.items():
        parts.extend([f"# {title}", "", body, ""])
    return "\n".join(parts).strip("\n")


def build_prompt(
    working_context: str,
    ai_context: str,
    dev_rules: str,
    *,
    mode: Literal["compact", "full"] = "compact",
    include_repo_tree: bool = False,
    root_dir: Path = ROOT_DIR,
    max_depth: int = 3,
) -> str:
    """Assemble the final prompt from all context sources.

    Args:
        working_context: Raw WORKING_CONTEXT.md text.
        ai_context: Raw AI_CONTEXT.md text.
        dev_rules: Raw DEVELOPMENT_RULES.md text.
        mode: "compact" includes only task-relevant sections; "full" includes everything.
        include_repo_tree: Whether to append a repository tree section.
        root_dir: Root directory for the optional tree.
        max_depth: Maximum depth for the optional tree.

    Returns:
        The assembled prompt string.
    """
    task = extract_task_context(working_context)

    if mode == "full":
        task.architecture_decisions = parse_architecture_decisions(working_context)
        ai_sections = parse_markdown_sections(ai_context)
        rules_sections = parse_markdown_sections(dev_rules)
    else:
        keywords = extract_task_keywords(task)
        LOGGER.info("Detected task keywords: %s", sorted(keywords) or "none")

        task.architecture_decisions = filter_architecture_decisions(
            task.architecture_decisions, keywords
        )
        ai_sections = select_relevant_sections(
            parse_markdown_sections(ai_context),
            keywords,
            AI_SECTION_RELEVANCE,
            ALWAYS_AI_SECTIONS,
        )
        rules_sections = select_relevant_sections(
            parse_markdown_sections(dev_rules),
            keywords,
            RULES_SECTION_RELEVANCE,
            ALWAYS_RULES_SECTIONS,
        )

    task_context_text = _format_task_context(task)
    ai_context_text = _format_sections(ai_sections)
    rules_text = _format_sections(rules_sections)

    lines: list[str] = [
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
        task_context_text,
        "",
        "-" * 72,
        "SECTION 2: RELEVANT PROJECT CONTEXT",
        "-" * 72,
        "",
        "Read and internalize the following architecture context before",
        "implementing. Respect all data contracts, naming conventions,",
        "and technology decisions.",
        "",
        ai_context_text,
        "",
        "-" * 72,
        "SECTION 3: RELEVANT DEVELOPMENT RULES",
        "-" * 72,
        "",
        "Every line of code you produce MUST comply with ALL rules below.",
        "Violations are not acceptable.",
        "",
        rules_text,
        "",
    ]

    if include_repo_tree:
        lines.extend(["-" * 72, "SECTION 4: REPOSITORY STRUCTURE", "-" * 72, ""])
        lines.extend(get_repo_tree(root_dir, max_depth).splitlines())
        lines.append("")
        instruction_section = 5
    else:
        instruction_section = 4

    lines.extend(
        [
            "-" * 72,
            f"SECTION {instruction_section}: IMPLEMENTATION INSTRUCTIONS",
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
        ]
    )

    return "\n".join(lines)


# ── Repository Tree (Optional) ─────────────────────────────────────────────────


def get_repo_tree(root: Path, max_depth: int = 3) -> str:
    """Generate a simple tree representation of the repository.

    Args:
        root: Repository root directory.
        max_depth: Maximum recursion depth.

    Returns:
        Tree string with a header.
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
        description="Build a task-aware AI coding prompt from project context files.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Write prompt to file instead of stdout",
    )
    parser.add_argument(
        "--full",
        "-f",
        action="store_true",
        help="Include the full AI_CONTEXT.md and DEVELOPMENT_RULES.md",
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
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print info messages to stderr",
    )

    args = parser.parse_args()

    level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    LOGGER.info("Reading WORKING_CONTEXT.md...")
    working_context = read_file_safely(WORKING_CONTEXT_FILE, "Working context")

    LOGGER.info("Reading AI_CONTEXT.md...")
    ai_context = read_file_safely(AI_CONTEXT_FILE, "AI context")

    LOGGER.info("Reading DEVELOPMENT_RULES.md...")
    dev_rules = read_file_safely(DEV_RULES_FILE, "Development rules")

    mode: Literal["compact", "full"] = "full" if args.full else "compact"
    LOGGER.info("Building prompt in '%s' mode...", mode)

    prompt = build_prompt(
        working_context,
        ai_context,
        dev_rules,
        mode=mode,
        include_repo_tree=args.tree,
        max_depth=args.max_depth,
    )

    if args.output:
        args.output.write_text(prompt, encoding="utf-8")
        LOGGER.info("Prompt written to %s", args.output)
    else:
        print(prompt)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
