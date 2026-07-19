#!/usr/bin/env python3
"""
dev.py — Orchestrator for the AI-assisted development workflow.

This script is the single entry point for the development workflow.
It does NOT generate prompts or parse state — it delegates those jobs to
dedicated scripts and only coordinates their execution.

Subcommands
-----------
start       Prepare a task: verify repo state, generate context and prompt,
            optionally copy prompt to clipboard, and show next git commands.

complete    Finish a task: record commit details, advance PROJECT_STATE.md,
            regenerate WORKING_CONTEXT.md, and print the next task.

status      Show the current task, branch, progress, and next task.

prompt      Regenerate WORKING_CONTEXT.md and prompts/current_prompt.md.

next        Show the current task with acceptance criteria, dependencies,
            and expected files.

verify      Run the verification toolchain (ruff, mypy, pytest,
            docker compose config) and summarize results.

Examples
--------
    python scripts/dev.py start
    python scripts/dev.py complete
    python scripts/dev.py status
    python scripts/dev.py prompt
    python scripts/dev.py next
    python scripts/dev.py verify
"""

from __future__ import annotations

import argparse
import platform
import re
import subprocess
import sys
from pathlib import Path


# ── Configuration ──────────────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DOCS_DIR = ROOT_DIR / "docs"
PROMPTS_DIR = ROOT_DIR / "prompts"
STATE_FILE = DOCS_DIR / "PROJECT_STATE.md"
WORKING_CONTEXT_FILE = DOCS_DIR / "WORKING_CONTEXT.md"
CURRENT_PROMPT_FILE = PROMPTS_DIR / "current_prompt.md"

CLIPBOARD_COMMANDS = {
    "Darwin": ["pbcopy"],
    "Linux": ["xclip", "-selection", "clipboard"],
    "Windows": ["clip.exe"],
}


# ── Subprocess helpers ─────────────────────────────────────────────────────────


def run(
    *cmd: str,
    cwd: Path | None = None,
    check: bool = False,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a command and return the completed process."""
    return subprocess.run(
        cmd,
        cwd=str(cwd or ROOT_DIR),
        check=check,
        capture_output=capture,
        text=True,
    )


def run_script(name: str, *args: str) -> int:
    """Run a helper script from the scripts/ directory."""
    script_path = SCRIPTS_DIR / name
    if not script_path.exists():
        print(f"[ERROR] Helper script not found: {script_path}")
        return 1

    result = run(str(sys.executable), str(script_path), *args)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


# ── Git helpers ────────────────────────────────────────────────────────────────


def is_git_repository() -> bool:
    """Return True if the project root is inside a git repository."""
    return (ROOT_DIR / ".git").exists() or (
        run("git", "rev-parse", "--is-inside-work-tree", capture=True).returncode == 0
    )


def git_status() -> str:
    """Return the short porcelain git status output."""
    result = run("git", "status", "--porcelain")
    return result.stdout.strip()


def is_repo_clean() -> bool:
    """Return True if the working tree has no uncommitted changes."""
    return git_status() == ""


def current_branch() -> str:
    """Return the current git branch, or 'main' as a safe default."""
    result = run("git", "branch", "--show-current")
    branch = result.stdout.strip()
    return branch if branch else "main"


def latest_commit_hash() -> str:
    """Return the hash of the latest commit."""
    result = run("git", "log", "-1", "--format=%H")
    return result.stdout.strip()


def latest_commit_message() -> str:
    """Return the subject of the latest commit."""
    result = run("git", "log", "-1", "--format=%s")
    return result.stdout.strip()


# ── State parsing helpers ──────────────────────────────────────────────────────


def read_state() -> str:
    """Read PROJECT_STATE.md, raising a clear error if missing."""
    if not STATE_FILE.exists():
        print(f"[ERROR] State file not found: {STATE_FILE}")
        print("[HINT] Create docs/PROJECT_STATE.md before running dev.py.")
        sys.exit(1)
    return STATE_FILE.read_text(encoding="utf-8")


def parse_table(state_text: str, heading: str) -> dict[str, str]:
    """Parse a markdown table under the given heading into key/value pairs."""
    context: dict[str, str] = {}
    match = re.search(
        rf"^#+\s+{re.escape(heading)}\s*$\n\n(.*?)(?=^#+\s+|\Z)",
        state_text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return context

    for line in match.group(1).splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 2:
            continue
        key = parts[0]
        if key.lower() == "field" or key.startswith("-"):
            continue
        context[key] = " | ".join(parts[1:])
    return context


def current_task_info(state_text: str) -> dict[str, str]:
    """Return a normalized dictionary describing the current task."""
    ctx = parse_table(state_text, "Current Working Context")
    summary = parse_table(state_text, "Project Status Summary")
    task_field = ctx.get("Current task", summary.get("Current task", "—"))
    task_id, _, task_name = task_field.partition(" — ")
    if not task_name:
        task_name = task_field

    next_field = summary.get("Next task", "—")
    next_id, _, next_name = next_field.partition(" — ")
    if not next_name:
        next_name = next_field

    return {
        "milestone": ctx.get("Current milestone", "—"),
        "epic": ctx.get("Current epic", "—"),
        "task_id": task_id.strip() or "—",
        "task_name": task_name.strip() or "—",
        "task_description": ctx.get("Task description", task_name.strip() or "—"),
        "acceptance_criteria": ctx.get("Acceptance criteria", "—"),
        "dependencies": ctx.get("Dependencies", "—"),
        "expected_files": ctx.get("Expected files", "—"),
        "next_id": next_id.strip() or "—",
        "next_name": next_name.strip() or "—",
    }


def overall_progress(state_text: str) -> str:
    """Return the overall completion percentage from PROJECT_STATE.md."""
    match = re.search(r"\| Overall Progress \| (.*?) \|", state_text)
    if match:
        return match.group(1).strip()
    return "—"


def branch_for_task(task_id: str) -> str:
    """Return the suggested feature branch name for a task."""
    return f"feature/{task_id}"


# ── Clipboard helper ───────────────────────────────────────────────────────────


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard. Return True on success."""
    system = platform.system()
    command = CLIPBOARD_COMMANDS.get(system)

    if not command:
        print(f"[WARN] Clipboard copy not supported on {system}")
        return False

    try:
        proc = subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True,
            check=True,
        )
        return proc.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"[WARN] Could not copy to clipboard: {exc}")
        return False


# ── Output helpers ─────────────────────────────────────────────────────────────


def print_header(title: str) -> None:
    """Print a centered banner."""
    width = max(len(title) + 4, 40)
    print("=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_section(title: str, body: str) -> None:
    """Print a titled section."""
    print(f"\n{title}")
    print("-" * len(title))
    print(body)


# ── Command implementations ────────────────────────────────────────────────────


def cmd_start(args: argparse.Namespace) -> int:
    """Run the start workflow."""
    print_header("Streaming Lakehouse Development")

    state_text = read_state()
    info = current_task_info(state_text)

    # Repository cleanliness check
    if is_git_repository():
        if is_repo_clean():
            print("\n[OK] Repository is clean.")
        else:
            print("\n[WARN] Repository has uncommitted changes:")
            print(git_status())
            print("[HINT] Commit or stash changes before starting a new task.")
    else:
        print("\n[INFO] Not a git repository — skipping cleanliness check.")

    # Display current task summary
    print_section("Current Task", f"{info['task_id']}\n{info['task_name']}")
    print_section("Branch", branch_for_task(info["task_id"]))
    print_section("Milestone", info["milestone"])
    print_section("Epic", info["epic"])

    # Acceptance criteria may already be rendered in WORKING_CONTEXT.md after
    # extract_context runs; print a concise preview here.
    acceptance = info["acceptance_criteria"]
    if acceptance and acceptance != "—":
        # Normalize bullets for display.
        preview = acceptance.replace("; ", "\n- ").replace(";", "\n- ")
        if not preview.startswith("- "):
            preview = "- " + preview
        print_section("Acceptance Criteria", preview)

    # Generate working context and prompt
    print("\n[INFO] Generating working context...")
    if run_script("extract_context.py") != 0:
        print("[ERROR] Failed to generate WORKING_CONTEXT.md")
        return 1

    print("\n[INFO] Generating prompt...")
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    if run_script("build_prompt.py", "--output", str(CURRENT_PROMPT_FILE)) != 0:
        print("[ERROR] Failed to generate prompt")
        return 1

    print(f"\n[SUCCESS] Prompt saved to {CURRENT_PROMPT_FILE}")

    if not args.no_clipboard:
        try:
            prompt_text = CURRENT_PROMPT_FILE.read_text(encoding="utf-8")
            if copy_to_clipboard(prompt_text):
                print("[SUCCESS] Prompt copied to clipboard")
        except OSError as exc:
            print(f"[WARN] Could not read prompt for clipboard copy: {exc}")

    # Show next git commands
    print_section(
        "Next commands",
        f"git checkout -b {branch_for_task(info['task_id'])}\n"
        f"# Implement the task, then:\n"
        f"git add .\n"
        f'git commit -m "{info["task_id"]} {info["task_name"]}"',
    )

    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Run the complete workflow."""
    print_header("Complete Task")

    # Optional verification
    if not args.skip_verify:
        print("\n[INFO] Running verification commands...")
        cmd_verify(args)
        proceed = input("\nProceed with completion? [Y/n]: ").strip().lower()
        if proceed and proceed not in {"y", "yes"}:
            print("[INFO] Aborting completion.")
            return 0

    # Commit hash
    if args.commit_hash:
        commit_hash = args.commit_hash
    elif is_git_repository() and latest_commit_hash():
        commit_hash = latest_commit_hash()
    else:
        commit_hash = input("Commit hash (or 'none'): ").strip()

    if commit_hash.lower() in {"none", "-", ""}:
        commit_hash = "—"

    # Commit message
    if args.commit_message:
        commit_message = args.commit_message
    elif is_git_repository() and latest_commit_message():
        commit_message = latest_commit_message()
        print(f"\n[INFO] Using latest commit message: {commit_message}")
    else:
        commit_message = input("Commit message: ").strip()

    print(f"\nLatest commit:\n{commit_hash}\n")
    print(f"Message:\n{commit_message}\n")

    # Advance state
    print("[INFO] Updating PROJECT_STATE.md...")
    if run_script("update_project_state.py", "--next") != 0:
        print("[ERROR] Failed to update PROJECT_STATE.md")
        return 1

    # Regenerate working context for the next task
    print("\n[INFO] Regenerating WORKING_CONTEXT.md for next task...")
    if run_script("extract_context.py") != 0:
        print("[WARN] Failed to regenerate WORKING_CONTEXT.md")

    # Read updated state and print next task
    updated_state = read_state()
    updated_info = current_task_info(updated_state)
    print_section(
        "Next Task",
        f"{updated_info['task_id']}\n{updated_info['task_name']}",
    )
    if updated_info["task_description"] not in {"—", updated_info["task_name"]}:
        print_section("Description", updated_info["task_description"])

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show current task, branch, progress, and next task."""
    state_text = read_state()
    info = current_task_info(state_text)

    print_header("Project Status")
    print_section("Current task", f"{info['task_id']} — {info['task_name']}")
    print_section("Current branch", current_branch())
    print_section("Progress", overall_progress(state_text))
    print_section("Next task", f"{info['next_id']} — {info['next_name']}")

    if is_git_repository() and not is_repo_clean():
        print("\n[WARN] Working tree has uncommitted changes.")

    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    """Generate WORKING_CONTEXT.md and prompts/current_prompt.md."""
    print_header("Generate Prompt")

    print("\n[INFO] Running extract_context.py...")
    if run_script("extract_context.py") != 0:
        return 1

    print("\n[INFO] Running build_prompt.py...")
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    if run_script("build_prompt.py", "--output", str(CURRENT_PROMPT_FILE)) != 0:
        return 1

    print(f"\n[SUCCESS] Prompt saved to {CURRENT_PROMPT_FILE}")

    if not args.no_clipboard:
        try:
            prompt_text = CURRENT_PROMPT_FILE.read_text(encoding="utf-8")
            if copy_to_clipboard(prompt_text):
                print("[SUCCESS] Prompt copied to clipboard")
        except OSError as exc:
            print(f"[WARN] Could not read prompt for clipboard copy: {exc}")

    return 0


def cmd_next(args: argparse.Namespace) -> int:
    """Show details for the current task."""
    state_text = read_state()
    info = current_task_info(state_text)

    print_header("Current Task Details")
    print_section("Task", f"{info['task_id']} — {info['task_name']}")
    print_section("Branch", branch_for_task(info["task_id"]))
    print_section("Milestone", info["milestone"])
    print_section("Epic", info["epic"])

    if info["task_description"] not in {"—", info["task_name"]}:
        print_section("Description", info["task_description"])

    if info["acceptance_criteria"] != "—":
        print_section("Acceptance Criteria", info["acceptance_criteria"])

    if info["dependencies"] != "—":
        print_section("Dependencies", info["dependencies"])

    if info["expected_files"] != "—":
        print_section("Expected Files", info["expected_files"])

    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Run verification commands and summarize results."""
    print_header("Verification")

    checks = [
        ("ruff check", ["ruff", "check", "."]),
        ("ruff format", ["ruff", "format", "--check", "."]),
        ("mypy", ["mypy", "."]),
        ("pytest", ["pytest"]),
        ("docker compose config", ["docker", "compose", "config"]),
    ]

    results: list[tuple[str, int, str]] = []
    overall_failed = False

    for name, cmd in checks:
        print(f"\n[INFO] Running {name}...")
        try:
            result = run(*cmd)
        except (FileNotFoundError, PermissionError) as exc:
            overall_failed = True
            results.append((name, 127, "MISSING"))
            print(f"[MISSING] {name}: {exc}")
            continue

        status = "PASS" if result.returncode == 0 else "FAIL"
        if result.returncode != 0:
            overall_failed = True
        results.append((name, result.returncode, status))
        print(f"[{status}] {name}")
        if result.returncode != 0:
            if result.stdout:
                print(result.stdout[:800])
            if result.stderr:
                print(result.stderr[:800], file=sys.stderr)

    print("\n" + "=" * 40)
    print("Verification Summary")
    print("=" * 40)
    for name, code, status in results:
        print(f"  [{status}] {name} (exit {code})")

    return 1 if overall_failed else 0


# ── CLI ────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="dev.py",
        description="Orchestrator for the AI-assisted development workflow.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    start_parser = subparsers.add_parser(
        "start",
        help="Prepare a task: generate context, prompt, and next git commands.",
    )
    start_parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Do not copy the generated prompt to the clipboard.",
    )
    start_parser.set_defaults(func=cmd_start)

    # complete
    complete_parser = subparsers.add_parser(
        "complete",
        help="Finish a task: update state and show the next task.",
    )
    complete_parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip running verification commands before completion.",
    )
    complete_parser.add_argument(
        "--commit-hash",
        type=str,
        help="Commit hash to record (defaults to the latest commit).",
    )
    complete_parser.add_argument(
        "--commit-message",
        type=str,
        help="Commit message to display (defaults to the latest commit message).",
    )
    complete_parser.set_defaults(func=cmd_complete)

    # status
    status_parser = subparsers.add_parser(
        "status",
        help="Show the current task, branch, progress, and next task.",
    )
    status_parser.set_defaults(func=cmd_status)

    # prompt
    prompt_parser = subparsers.add_parser(
        "prompt",
        help="Generate WORKING_CONTEXT.md and prompts/current_prompt.md.",
    )
    prompt_parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Do not copy the generated prompt to the clipboard.",
    )
    prompt_parser.set_defaults(func=cmd_prompt)

    # next
    next_parser = subparsers.add_parser(
        "next",
        help="Show the current task details.",
    )
    next_parser.set_defaults(func=cmd_next)

    # verify
    verify_parser = subparsers.add_parser(
        "verify",
        help="Run ruff, mypy, pytest, and docker compose config.",
    )
    verify_parser.set_defaults(func=cmd_verify)

    return parser


def main() -> int:
    """Parse CLI arguments and dispatch to the appropriate subcommand."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
