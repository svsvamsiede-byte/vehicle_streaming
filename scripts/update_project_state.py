#!/usr/bin/env python3
"""
update_project_state.py

Updates PROJECT_STATE.md after a task is completed.
Marks the current task as COMPLETED, updates progress percentages,
advances to the next task, and updates milestone/epic status.

Usage:
    python scripts/update_project_state.py --task M1-E1-T01 --status COMPLETED
    python scripts/update_project_state.py --next
"""

from __future__ import annotations
import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
STATE_FILE = DOCS_DIR / "PROJECT_STATE.md"


class TaskStatus(str, Enum):
    """Valid task statuses."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"


# ── Data Structures ────────────────────────────────────────────────────────────


@dataclass
class Task:
    """Represents an atomic task."""

    task_id: str
    task_name: str
    milestone: str
    epic: str
    status: str
    dependencies: str
    expected_files: str
    git_commit: str
    branch: str
    notes: str


@dataclass
class Milestone:
    """Represents a milestone."""

    name: str
    status: str
    progress: str
    notes: str


@dataclass
class Epic:
    """Represents an epic."""

    name: str
    status: str
    progress: str
    current_task: str


# ── File I/O ───────────────────────────────────────────────────────────────────


def read_state() -> str:
    """Read the current PROJECT_STATE.md content."""
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}")
    return STATE_FILE.read_text(encoding="utf-8")


def write_state(content: str) -> None:
    """Write updated content back to PROJECT_STATE.md."""
    STATE_FILE.write_text(content, encoding="utf-8")


# ── Parsing ────────────────────────────────────────────────────────────────────


def parse_tasks(text: str) -> list[Task]:
    """Parse all tasks from the Atomic Task Tracker table."""
    # Find the Atomic Task Tracker section
    section_match = re.search(
        r"# Atomic Task Tracker\n\n(.*?)(?=##? |\Z)",
        text,
        re.DOTALL,
    )
    if not section_match:
        return []

    section = section_match.group(1)
    lines = section.strip().split("\n")

    tasks: list[Task] = []
    header_found = False

    for line in lines:
        # Skip markdown table formatting
        if line.startswith("| ") and not line.startswith("|-"):
            if not header_found:
                header_found = True
                continue

            parts = [p.strip() for p in line.split("|")]
            # Filter empty strings from leading/trailing pipes
            parts = [p for p in parts if p]

            if len(parts) >= 10:
                tasks.append(
                    Task(
                        task_id=parts[0],
                        task_name=parts[1],
                        milestone=parts[2],
                        epic=parts[3],
                        status=parts[4],
                        dependencies=parts[5],
                        expected_files=parts[6],
                        git_commit=parts[7],
                        branch=parts[8],
                        notes=parts[9] if len(parts) > 9 else "",
                    )
                )

    return tasks


def parse_current_context(text: str) -> dict[str, str]:
    """Extract current working context fields."""
    context: dict[str, str] = {}

    # Extract from Current Working Context section
    section_match = re.search(
        r"^#+\s+Current Working Context\s*$\n\n(.*?)(?=^#+\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not section_match:
        return context

    section = section_match.group(1)
    for line in section.split("\n"):
        match = re.match(r"\| (.*?) \| (.*?) \|", line)
        if match and match.group(1).strip() != "Field":
            context[match.group(1).strip()] = match.group(2).strip()

    return context


# ── Updates ─────────────────────────────────────────────────────────────────────


def update_task_status(tasks: list[Task], task_id: str, status: str) -> list[Task]:
    """Update the status of a specific task."""
    updated = False
    for task in tasks:
        if task.task_id == task_id:
            task.status = status
            updated = True
            break

    if not updated:
        raise ValueError(f"Task {task_id} not found in task tracker")

    return tasks


def find_next_task(tasks: list[Task], current_task_id: str) -> Task | None:
    """Find the next logical task after the current one."""
    current_idx = None
    for i, task in enumerate(tasks):
        if task.task_id == current_task_id:
            current_idx = i
            break

    if current_idx is None:
        return None

    # Look for next NOT_STARTED task, preferring same milestone/epic
    current_milestone = tasks[current_idx].milestone
    current_epic = tasks[current_idx].epic

    # First: same epic, next in list
    for i in range(current_idx + 1, len(tasks)):
        if tasks[i].status == TaskStatus.NOT_STARTED.value:
            if (
                tasks[i].milestone == current_milestone
                and tasks[i].epic == current_epic
            ):
                return tasks[i]

    # Second: same milestone, any epic
    for i in range(current_idx + 1, len(tasks)):
        if tasks[i].status == TaskStatus.NOT_STARTED.value:
            if tasks[i].milestone == current_milestone:
                return tasks[i]

    # Third: any next task
    for i in range(current_idx + 1, len(tasks)):
        if tasks[i].status == TaskStatus.NOT_STARTED.value:
            return tasks[i]

    return None


def calculate_progress(tasks: list[Task]) -> tuple[int, int, int]:
    """Calculate completion statistics."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED.value)
    in_progress = sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS.value)
    return total, completed, in_progress


def rebuild_task_table(tasks: list[Task]) -> str:
    """Rebuild the Atomic Task Tracker markdown table."""
    lines = [
        "## Atomic Task Tracker",
        "",
        "| Task ID | Task Name | Milestone | Epic | Status | Dependencies | Expected Files | Git Commit | Branch | Notes |",
        "|---------|-----------|-----------|------|--------|--------------|----------------|------------|--------|-------|",
    ]

    for task in tasks:
        lines.append(
            f"| {task.task_id} | {task.task_name} | {task.milestone} | {task.epic} | "
            f"{task.status} | {task.dependencies} | {task.expected_files} | "
            f"{task.git_commit} | {task.branch} | {task.notes} |"
        )

    lines.append("")
    return "\n".join(lines)


def rebuild_current_context(context: dict[str, str]) -> str:
    """Rebuild the Current Working Context section."""
    lines = ["## Current Working Context", "", "| Field | Value |", "|-------|-------|"]

    for key, value in context.items():
        lines.append(f"| {key} | {value} |")

    lines.append("")
    return "\n".join(lines)


def update_milestone_status(text: str, tasks: list[Task]) -> str:
    """Update milestone progress based on task completion."""
    # Extract milestone names from tasks
    milestone_tasks: dict[str, list[Task]] = {}
    for task in tasks:
        ms = task.milestone
        if ms not in milestone_tasks:
            milestone_tasks[ms] = []
        milestone_tasks[ms].append(task)

    # Update each milestone section
    for milestone_name, ms_tasks in milestone_tasks.items():
        total = len(ms_tasks)
        completed = sum(1 for t in ms_tasks if t.status == TaskStatus.COMPLETED.value)
        progress = int((completed / total) * 100) if total > 0 else 0

        # Determine status
        if progress == 100:
            status = "COMPLETED"
        elif progress > 0:
            status = "IN_PROGRESS"
        else:
            status = "NOT_STARTED"

        # Update milestone table row
        pattern = rf"(\| {re.escape(milestone_name)} \|) .*? (\| .*? \| .*? \|)"
        replacement = f"\\1 {status} | {progress}% \\2"
        text = re.sub(pattern, replacement, text, count=1)

    return text


def update_epic_status(text: str, tasks: list[Task]) -> str:
    """Update epic progress based on task completion."""
    epic_tasks: dict[str, list[Task]] = {}
    for task in tasks:
        epic = task.epic
        if epic not in epic_tasks:
            epic_tasks[epic] = []
        epic_tasks[epic].append(task)

    for epic_name, ep_tasks in epic_tasks.items():
        total = len(ep_tasks)
        completed = sum(1 for t in ep_tasks if t.status == TaskStatus.COMPLETED.value)
        progress = int((completed / total) * 100) if total > 0 else 0

        if progress == 100:
            status = "COMPLETED"
        elif progress > 0:
            status = "IN_PROGRESS"
        else:
            status = "NOT_STARTED"

        # Find current task for this epic
        current = None
        for t in ep_tasks:
            if t.status == TaskStatus.IN_PROGRESS.value:
                current = t.task_id
                break
        if not current:
            for t in ep_tasks:
                if t.status == TaskStatus.NOT_STARTED.value:
                    current = t.task_id
                    break

        current_display = current if current else "—"

        pattern = rf"(\| {re.escape(epic_name)} \|) .*? (\| .*? \|) .*? (\| .*? \|)"
        replacement = f"\\1 {status} | {progress}% \\2 {current_display} \\3"
        text = re.sub(pattern, replacement, text, count=1)

    return text


def update_overall_progress(text: str, total: int, completed: int) -> str:
    """Update overall completion percentage."""
    progress = int((completed / total) * 100) if total > 0 else 0

    # Update Overall Progress field
    text = re.sub(
        r"(\| Overall Progress \|) .*? (\|)",
        f"\\1 {progress}% \\2",
        text,
    )

    # Update Overall completion percentage
    text = re.sub(
        r"(\| Overall completion percentage \|) .*? (\|)",
        f"\\1 {progress}% \\2",
        text,
    )

    return text


# ── Main Operations ────────────────────────────────────────────────────────────


def mark_task_complete(task_id: str) -> None:
    """Mark a specific task as completed and update state."""
    text = read_state()
    tasks = parse_tasks(text)

    # Update task status
    tasks = update_task_status(tasks, task_id, TaskStatus.COMPLETED.value)

    # Calculate progress
    total, completed, _ = calculate_progress(tasks)

    # Update milestone and epic tables
    text = update_milestone_status(text, tasks)
    text = update_epic_status(text, tasks)
    text = update_overall_progress(text, total, completed)

    # Rebuild task table
    old_table = re.search(r"## Atomic Task Tracker\n\n.*?\n(?=## |\Z)", text, re.DOTALL)
    if old_table:
        new_table = rebuild_task_table(tasks)
        text = text[: old_table.start()] + new_table + "\n" + text[old_table.end() :]

    # Update completed tasks section
    completed_section = re.search(
        r"## Completed Tasks\n\n(.*?)(?=## |\Z)", text, re.DOTALL
    )
    if completed_section:
        existing = completed_section.group(1).strip()
        if existing == "No completed tasks.":
            new_completed = f"- {task_id}"
        else:
            new_completed = f"{existing}\n- {task_id}"

        text = (
            text[: completed_section.start(1)]
            + new_completed
            + text[completed_section.end(1) :]
        )

    write_state(text)
    print(f"[SUCCESS] Task {task_id} marked as COMPLETED")
    print(
        f"[INFO] Overall progress: {completed}/{total} tasks ({int((completed / total) * 100)}%)"
    )


def advance_to_next() -> None:
    """Advance from current task to the next one."""
    text = read_state()
    tasks = parse_tasks(text)
    context = parse_current_context(text)

    current_task_field = context.get("Current task", "")
    if not current_task_field or current_task_field == "—":
        print("[ERROR] No current task found in context")
        sys.exit(1)

    current_task_id = current_task_field.split(" — ")[0].strip()

    # Mark current as completed
    tasks = update_task_status(tasks, current_task_id, TaskStatus.COMPLETED.value)

    # Find next task
    next_task = find_next_task(tasks, current_task_id)

    if not next_task:
        print("[INFO] No more tasks found. Project complete!")
        # Update context to reflect completion
        text = re.sub(
            r"(\| Current task \|) .*? (\|)",
            "\\1 — \\2",
            text,
        )
        text = re.sub(
            r"(\| Next task \|) .*? (\|)",
            "\\1 — \\2",
            text,
        )
        text = re.sub(
            r"(\| Current epic \|) .*? (\|)",
            "\\1 — \\2",
            text,
        )
        text = re.sub(
            r"(\| Current milestone \|) .*? (\|)",
            "\\1 — \\2",
            text,
        )
        text = re.sub(
            r"(\| Task description \|) .*? (\|)",
            "\\1 — \\2",
            text,
        )

        # Calculate and update progress
        total, completed, _ = calculate_progress(tasks)
        text = update_milestone_status(text, tasks)
        text = update_epic_status(text, tasks)
        text = update_overall_progress(text, total, completed)

        # Rebuild task table so the current task shows COMPLETED
        old_table = re.search(
            r"## Atomic Task Tracker\n\n.*?\n(?=## |\Z)", text, re.DOTALL
        )
        if old_table:
            new_table = rebuild_task_table(tasks)
            text = (
                text[: old_table.start()] + new_table + "\n" + text[old_table.end() :]
            )

        # Update completed tasks
        completed_section = re.search(
            r"## Completed Tasks\n\n(.*?)(?=## |\Z)", text, re.DOTALL
        )
        if completed_section:
            existing = completed_section.group(1).strip()
            if existing == "No completed tasks.":
                new_completed = f"- {current_task_id}"
            else:
                new_completed = f"{existing}\n- {current_task_id}"

            text = (
                text[: completed_section.start(1)]
                + new_completed
                + text[completed_section.end(1) :]
            )

        write_state(text)
        print(
            f"[INFO] Overall progress: {completed}/{total} tasks ({int((completed / total) * 100)}%)"
        )
        return

    # Update next task to IN_PROGRESS
    for task in tasks:
        if task.task_id == next_task.task_id:
            task.status = TaskStatus.IN_PROGRESS.value
            break

    # Update context
    text = re.sub(
        r"(\| Current task \|) .*? (\|)",
        f"\\1 {next_task.task_id} — {next_task.task_name} \\2",
        text,
    )

    # Find next-next task for the "Next task" field
    next_next = find_next_task(tasks, next_task.task_id)
    next_task_display = (
        f"{next_next.task_id} — {next_next.task_name}" if next_next else "—"
    )
    text = re.sub(
        r"(\| Next task \|) .*? (\|)",
        f"\\1 {next_task_display} \\2",
        text,
    )

    text = re.sub(
        r"(\| Current epic \|) .*? (\|)",
        f"\\1 {next_task.epic} \\2",
        text,
    )

    text = re.sub(
        r"(\| Current milestone \|) .*? (\|)",
        f"\\1 {next_task.milestone} \\2",
        text,
    )

    # Update task description
    text = re.sub(
        r"(\| Task description \|) .*? (\|)",
        f"\\1 {next_task.task_name} \\2",
        text,
    )

    # Update expected files and dependencies from the task tracker
    text = re.sub(
        r"(\| Expected files \|) .*? (\|)",
        f"\\1 {next_task.expected_files} \\2",
        text,
    )
    text = re.sub(
        r"(\| Dependencies \|) .*? (\|)",
        f"\\1 {next_task.dependencies} \\2",
        text,
    )

    # Acceptance criteria are not stored in the task tracker; clear the stale value
    text = re.sub(
        r"(\| Acceptance criteria \|) .*? (\|)",
        "\\1 — \\2",
        text,
    )

    # Calculate and update progress
    total, completed, _ = calculate_progress(tasks)
    text = update_milestone_status(text, tasks)
    text = update_epic_status(text, tasks)
    text = update_overall_progress(text, total, completed)

    # Rebuild task table
    old_table = re.search(r"## Atomic Task Tracker\n\n.*?\n(?=## |\Z)", text, re.DOTALL)
    if old_table:
        new_table = rebuild_task_table(tasks)
        text = text[: old_table.start()] + new_table + "\n" + text[old_table.end() :]

    # Update completed tasks
    completed_section = re.search(
        r"## Completed Tasks\n\n(.*?)(?=## |\Z)", text, re.DOTALL
    )
    if completed_section:
        existing = completed_section.group(1).strip()
        if existing == "No completed tasks.":
            new_completed = f"- {current_task_id}"
        else:
            new_completed = f"{existing}\n- {current_task_id}"

        text = (
            text[: completed_section.start(1)]
            + new_completed
            + text[completed_section.end(1) :]
        )

    write_state(text)
    print(f"[SUCCESS] Advanced to {next_task.task_id}: {next_task.task_name}")
    print(
        f"[INFO] Overall progress: {completed}/{total} tasks ({int((completed / total) * 100)}%)"
    )


# ── CLI ────────────────────────────────────────────────────────────────────────


def main() -> int:
    """Parse arguments and execute the appropriate command."""
    parser = argparse.ArgumentParser(
        description="Update PROJECT_STATE.md after task completion or advancement.",
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Task ID to mark as completed (e.g., M1-E1-T01)",
    )
    parser.add_argument(
        "--status",
        type=str,
        choices=[s.value for s in TaskStatus],
        default=TaskStatus.COMPLETED.value,
        help="New status for the task",
    )
    parser.add_argument(
        "--next",
        action="store_true",
        help="Advance to the next task after completing current",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show current progress summary",
    )

    args = parser.parse_args()

    if args.progress:
        text = read_state()
        tasks = parse_tasks(text)
        total, completed, in_progress = calculate_progress(tasks)
        print(f"Total tasks: {total}")
        print(f"Completed: {completed}")
        print(f"In Progress: {in_progress}")
        print(f"Remaining: {total - completed - in_progress}")
        overall = int((completed / total) * 100) if total > 0 else 0
        print(f"Overall: {overall}%")
        return 0

    if args.next:
        advance_to_next()
        return 0

    if args.task:
        if args.status == TaskStatus.COMPLETED.value:
            mark_task_complete(args.task)
        else:
            text = read_state()
            tasks = parse_tasks(text)
            tasks = update_task_status(tasks, args.task, args.status)
            # Rebuild and write
            old_table = re.search(
                r"## Atomic Task Tracker\n\n.*?\n(?=## |\Z)", text, re.DOTALL
            )
            if old_table:
                new_table = rebuild_task_table(tasks)
                text = (
                    text[: old_table.start()]
                    + new_table
                    + "\n"
                    + text[old_table.end() :]
                )
            write_state(text)
            print(f"[SUCCESS] Task {args.task} marked as {args.status}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
