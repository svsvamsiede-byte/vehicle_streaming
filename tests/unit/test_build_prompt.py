"""Unit tests for scripts/build_prompt.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from build_prompt import (
    AI_SECTION_RELEVANCE,
    ALWAYS_AI_SECTIONS,
    TaskContext,
    build_prompt,
    extract_task_context,
    extract_task_keywords,
    filter_architecture_decisions,
    parse_architecture_decisions,
    parse_bullet_list,
    parse_markdown_sections,
    select_relevant_sections,
)


SAMPLE_WORKING_CONTEXT = """# Working Context

> Auto-generated from PROJECT_STATE.md

---

## Task

M1-E1-T01 — Create `.env` Environment File

## Acceptance Criteria

All services reference variables from `.env`;
No hardcoded secrets in `docker-compose.yml`;
`source .env && echo $KAFKA_PORT` returns expected value

## Dependencies

None

## Branch

N/A

## Relevant Files

`.env`

## Relevant Architecture Decisions

| Decision ID | Date | Decision | Reason | Impact |
|-------------|------|----------|--------|--------|
| AD-001 | 2026-07-19 | Kafka before Flink | Events must land in Kafka before Flink consumes them | Decouples ingestion |
| AD-007 | 2026-07-19 | Docker Compose for Local Deployment | All services containerized | Simplifies onboarding |
| AD-011 | 2026-07-19 | MinIO as Object Storage | S3-compatible API | Cost-free local development |
"""

SAMPLE_AI_CONTEXT = """# Project Summary

Summary text.

# Architecture Overview

Architecture text.

# Repository Architecture

Repository text.

# Data Contracts

Data contracts text.

# Architectural Principles

Principles text.

# Operational Model

Operational model text.
"""

SAMPLE_DEV_RULES = """# AI Development Rules

---

# 1. General Principles

General principles.

# 2. Scope Rules

Scope rules.

# 8. Configuration

Configuration rules.

# 9. Docker

Docker rules.

# 17. Security

Security rules.

# 18. AI-Specific Rules

AI rules.

# 19. Completion Checklist

Checklist.
"""


def test_extract_task_context_parses_basic_fields() -> None:
    """Task metadata is extracted from WORKING_CONTEXT.md."""
    task = extract_task_context(SAMPLE_WORKING_CONTEXT)

    assert task.task_id == "M1-E1-T01"
    assert task.title == "Create `.env` Environment File"
    assert task.branch == "N/A"
    assert task.relevant_files == ["`.env`"]
    assert len(task.architecture_decisions) == 3


def test_extract_task_context_splits_bullet_criteria() -> None:
    """Semicolon-separated acceptance criteria are split into bullets."""
    task = extract_task_context(SAMPLE_WORKING_CONTEXT)

    assert len(task.acceptance_criteria) == 3
    assert "No hardcoded secrets in `docker-compose.yml`" in task.acceptance_criteria


def test_parse_architecture_decisions_extracts_rows() -> None:
    """Decision table rows are extracted excluding header and separator."""
    decisions = parse_architecture_decisions(SAMPLE_WORKING_CONTEXT)

    assert len(decisions) == 3
    assert all(row.startswith("| AD-") for row in decisions)


def test_extract_task_keywords_detects_env_and_docker() -> None:
    """Primary keywords from task text and files map to relevance tags."""
    task = extract_task_context(SAMPLE_WORKING_CONTEXT)
    keywords = extract_task_keywords(task)

    assert "env" in keywords
    assert "docker" in keywords
    assert "kafka" not in keywords


def test_select_relevant_sections_includes_always_sections() -> None:
    """Always-included sections are present even with no keywords."""
    sections = parse_markdown_sections(SAMPLE_AI_CONTEXT)
    selected = select_relevant_sections(
        sections,
        set(),
        AI_SECTION_RELEVANCE,
        ALWAYS_AI_SECTIONS,
    )

    assert "Architectural Principles" in selected


def test_select_relevant_sections_includes_tagged_sections() -> None:
    """Tag-mapped sections are included for the current keywords."""
    sections = parse_markdown_sections(SAMPLE_AI_CONTEXT)
    selected = select_relevant_sections(
        sections,
        {"env", "docker"},
        AI_SECTION_RELEVANCE,
        ALWAYS_AI_SECTIONS,
    )

    assert "Repository Architecture" in selected
    assert "Architectural Principles" in selected


def test_select_relevant_sections_warns_on_missing_section(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Missing section references are skipped with a warning."""
    sections = parse_markdown_sections(SAMPLE_AI_CONTEXT)

    with caplog.at_level("WARNING"):
        select_relevant_sections(
            sections,
            {"flink"},
            {"flink": ["Nonexistent Section"]},
            [],
        )

    assert "Nonexistent Section" in caplog.text


def test_filter_architecture_decisions_reduces_to_matching_keywords() -> None:
    """Decisions mentioning task keywords are retained."""
    task = extract_task_context(SAMPLE_WORKING_CONTEXT)
    keywords = extract_task_keywords(task)
    filtered = filter_architecture_decisions(task.architecture_decisions, keywords)

    assert len(filtered) == 1
    assert all("Docker" in row for row in filtered)


def test_filter_architecture_decisions_falls_back_when_empty() -> None:
    """If keyword filtering yields nothing, all decisions are returned."""
    decisions = parse_architecture_decisions(SAMPLE_WORKING_CONTEXT)
    filtered = filter_architecture_decisions(decisions, {"nonexistent"})

    assert len(filtered) == 3


def test_build_prompt_compact_is_smaller_than_full() -> None:
    """Compact mode produces a smaller prompt than full mode."""
    compact = build_prompt(
        SAMPLE_WORKING_CONTEXT,
        SAMPLE_AI_CONTEXT,
        SAMPLE_DEV_RULES,
        mode="compact",
    )
    full = build_prompt(
        SAMPLE_WORKING_CONTEXT,
        SAMPLE_AI_CONTEXT,
        SAMPLE_DEV_RULES,
        mode="full",
    )

    assert len(compact) < len(full)
    assert "RELEVANT PROJECT CONTEXT" in compact
    assert "RELEVANT DEVELOPMENT RULES" in compact


def test_build_prompt_compact_includes_expected_sections() -> None:
    """Compact prompt includes task context and relevant sections."""
    prompt = build_prompt(
        SAMPLE_WORKING_CONTEXT,
        SAMPLE_AI_CONTEXT,
        SAMPLE_DEV_RULES,
        mode="compact",
    )

    assert "M1-E1-T01" in prompt
    assert "Create `.env` Environment File" in prompt
    assert "Architectural Principles" in prompt
    assert "8. Configuration" in prompt
    assert "9. Docker" in prompt


def test_build_prompt_full_includes_all_sections() -> None:
    """Full mode includes every section from the source documents."""
    prompt = build_prompt(
        SAMPLE_WORKING_CONTEXT,
        SAMPLE_AI_CONTEXT,
        SAMPLE_DEV_RULES,
        mode="full",
    )

    assert "Project Summary" in prompt
    assert "Data Contracts" in prompt
    assert "1. General Principles" in prompt
    assert "19. Completion Checklist" in prompt


def test_parse_bullet_list_handles_bullets_and_numbers() -> None:
    """Bullet and numbered list items are parsed."""
    text = "- first\n- second\n1. third\n* fourth"
    items = parse_bullet_list(text)

    assert items == ["first", "second", "third", "fourth"]


def test_task_context_defaults() -> None:
    """TaskContext fields default to sensible empty values."""
    task = TaskContext()

    assert task.task_id == ""
    assert task.acceptance_criteria == []
