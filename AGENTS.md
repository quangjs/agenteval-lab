# Repository Guidelines

## Project Structure & Module Organization

This repository contains the AgentEval Lab specification and the first backend scaffold. `apps/api/` holds the FastAPI application, `packages/agenteval/` holds shared domain/persistence packages, and `project-docs/` holds design documentation and the sample dataset. `migrations/` and `tests/` will be added in later sections of Milestone 1. Update documentation links when adding project documents.

## Build, Test, and Development Commands

Use Python 3.13, `uv`, and Docker Compose v2. Run `uv lock` after dependency changes, then `uv sync --frozen` to install the locked workspace dependencies. Start local PostgreSQL with `docker compose up -d --wait postgres`, and run the API with `uv run --package agenteval-api uvicorn app.main:app --reload`. Run `uv run pytest` for tests as they are added. `docker compose down` preserves the named database volume. Never use local Compose credentials outside development.

## Writing and Data Conventions

Write concise Markdown with descriptive headings, short lists, and fenced code blocks labeled with their language. Keep terminology and lifecycle names consistent with the system design. Dataset examples should be valid JSON, use descriptive `snake_case` fields, stable test-case IDs such as `TC001`, and fictional fixture values. Published dataset versions are immutable: changes to cases, expectations, fixtures, or assertions should produce a new version.

## Testing Guidelines

Tests use pytest. Keep domain/schema unit tests runnable without PostgreSQL and isolate migration integration tests to disposable databases. Use deterministic fixtures for repeatable evaluation behavior. Validate edited JSON with a parser and check relative Markdown links.

## Commit & Pull Request Guidelines

The history currently contains only the initial project commit, so no established commit convention can be inferred. Use a short imperative commit subject (for example, `feat: add API scaffold`). Pull requests should explain the change, list affected packages/documents, link related work when available, and include screenshots only for visual changes. Call out changes to schemas, lifecycle states, or security/cost assumptions.

## Security and Configuration

Use fictional data in examples; do not commit credentials, customer data, or real agent traces. Follow `project-docs/docs/SECURITY_AND_COST.md` when designing configuration or execution behavior, and keep secrets in environment/deployment configuration rather than documentation fixtures.
