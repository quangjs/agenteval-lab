# Repository Guidelines

## Project Structure & Module Organization

This checkout is a documentation-first project specification; the product has not been implemented yet. `project-docs/README.md` is the entry point. Product and technical guidance lives in `project-docs/docs/` (requirements, system and detailed designs, testing flow, dataset format, evaluation strategy, roadmap, and security/cost controls). The sample dataset is at `project-docs/examples/datasets/order_agent_v1.json`. Keep new material in the matching directory and update the README links when adding a document. There are currently no source or test directories.

## Build, Test, and Development Commands

No build, test, or local-run commands are configured in this checkout. The README proposes Next.js/TypeScript, FastAPI/Python, pytest, and GitHub Actions as a future stack; treat these as design intent, not runnable commands. For documentation-only changes, review Markdown links and JSON examples manually. When implementation tooling is introduced, document the actual setup and commands here and in the README.

## Writing and Data Conventions

Write concise Markdown with descriptive headings, short lists, and fenced code blocks labeled with their language. Keep terminology and lifecycle names consistent with the system design. Dataset examples should be valid JSON, use descriptive `snake_case` fields, stable test-case IDs such as `TC001`, and fictional fixture values. Published dataset versions are immutable: changes to cases, expectations, fixtures, or assertions should produce a new version.

## Testing Guidelines

There is no automated test suite or coverage target yet. Validate edited JSON with a parser and check that relative Markdown links resolve. For future code, follow the proposed pytest convention and keep deterministic mock-tool cases suitable for repeatable CI runs.

## Commit & Pull Request Guidelines

Git metadata is not present in this checkout, so no repository-specific commit convention can be inferred. Use a short imperative commit subject (for example, `docs: clarify dataset versioning`). Pull requests should explain the user-facing or design change, list affected documents/data, link related work when available, and include screenshots only for visual changes. Call out any changes to schemas, lifecycle states, or security/cost assumptions.

## Security and Configuration

Use fictional data in examples; do not commit credentials, customer data, or real agent traces. Follow `project-docs/docs/SECURITY_AND_COST.md` when designing configuration or execution behavior, and keep secrets in environment/deployment configuration rather than documentation fixtures.
