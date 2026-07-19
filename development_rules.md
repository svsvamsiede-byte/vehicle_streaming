# DEVELOPMENT_RULES.md

# AI Development Rules

These rules apply to EVERY implementation task.

The objective is to produce production-quality software that resembles code written by an experienced engineering team.

---

# 1. General Principles

- Prefer readability over cleverness.
- Produce maintainable code.
- Keep solutions simple unless complexity is required.
- Never generate placeholder implementations.
- Never leave TODOs.
- Never generate pseudocode.
- Never omit required functionality.

Every task should leave the repository in a working state.

---

# 2. Scope Rules

Implement ONLY the requested task.

Do NOT implement future tasks.

Do NOT add "nice-to-have" features.

Do NOT refactor unrelated code.

Do NOT modify unrelated files.

Only edit files listed in the task unless absolutely necessary.

If additional files are required, explain why.

---

# 3. Existing Code

Always inspect existing files before modifying them.

Prefer extending existing code rather than rewriting it.

Do not regenerate files that already exist.

Do not rename files unless explicitly instructed.

Preserve backward compatibility whenever possible.

Preserve public APIs unless the task explicitly requires changes.

Never delete existing functionality.

---

# 4. Architecture

Follow Clean Architecture where applicable.

Keep business logic independent of infrastructure.

Avoid tight coupling.

Prefer dependency injection over global state.

Prefer composition over inheritance.

Follow SOLID principles.

---

# 5. Python Standards

Python 3.12

PEP8

Type hints everywhere.

Docstrings for

- modules
- public classes
- public functions

Avoid wildcard imports.

Avoid unused imports.

Avoid global mutable state.

Prefer pathlib over os.path.

Prefer dataclasses where appropriate.

Prefer Enum instead of magic strings.

Avoid duplicated logic.

---

# 6. Logging

Use Python logging.

Never use print().

Important operations should be logged.

Include useful context.

Do not log sensitive information.

Use appropriate log levels.

DEBUG

INFO

WARNING

ERROR

CRITICAL

---

# 7. Error Handling

Never silently swallow exceptions.

Catch only expected exceptions.

Raise meaningful exceptions.

Provide actionable error messages.

Do not use bare except.

Avoid exception-driven control flow.

---

# 8. Configuration

Never hardcode

- ports
- hosts
- credentials
- passwords
- API keys

Read configuration from

.env

config.py

environment variables

---

# 9. Docker

Docker services should be reproducible.

Containers must start without manual intervention.

Use health checks where appropriate.

Keep images lightweight.

Avoid unnecessary dependencies.

---

# 10. Kafka

Topics should be configurable.

Do not hardcode broker addresses.

Use proper serializers.

Handle producer failures.

Handle consumer failures.

Support graceful shutdown.

---

# 11. Flink

Prefer Event Time.

Use Watermarks correctly.

Checkpointing should remain configurable.

Avoid unnecessary state.

Keep operators modular.

Avoid giant pipeline files.

---

# 12. Testing

Every feature should be testable.

Add unit tests when appropriate.

Avoid flaky tests.

Tests should be deterministic.

---

# 13. Code Quality

Code must pass

ruff

mypy

pytest

without modification.

Avoid duplicated logic.

Keep functions short.

Prefer descriptive names.

Avoid deeply nested logic.

---

# 14. Documentation

Document public APIs.

Document configuration.

Document non-obvious decisions.

Avoid excessive comments.

Code should be self-explanatory.

---

# 15. Git

Every task should produce a commit-worthy change.

Do not mix unrelated changes.

Keep commits focused.

---

# 16. Performance

Avoid unnecessary allocations.

Avoid repeated work.

Prefer streaming over buffering where possible.

Do not prematurely optimize.

---

# 17. Security

Never commit secrets.

Never hardcode credentials.

Validate external input.

Escape user-controlled values where necessary.

---

# 18. AI-Specific Rules

Never invent missing requirements.

Never fabricate APIs.

Never fabricate library behavior.

If a dependency is unknown, state the assumption.

If required information is missing, stop and explain.

Never create placeholder implementations.

Never create fake test data unless requested.

Never remove existing functionality to simplify implementation.

---

# 19. Completion Checklist

Before considering a task complete verify:

✓ Project builds

✓ Imports succeed

✓ Code is formatted

✓ Lint passes

✓ Types pass

✓ Tests pass

✓ Logging added

✓ Docstrings added

✓ No TODOs

✓ No placeholder code

✓ Only expected files changed

✓ Repository remains runnable
