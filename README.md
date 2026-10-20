# AgentEval Lab

AgentEval Lab is a platform for testing, evaluating, benchmarking, and detecting regressions in AI agents. It helps developers verify task correctness, tool use, business-rule compliance, changes against a baseline, and execution quality through latency, cost, and trace data.

## Project Documentation

- [Product Requirements](project-docs/docs/PRODUCT_REQUIREMENTS.md)
- [High-level System Design](project-docs/docs/SYSTEM_DESIGN.md)
- [Detailed Design](project-docs/docs/DETAILED_DESIGN.md)
- [Backend Implementation Plan](project-docs/docs/IMPLEMENTATION_PLAN.md)
- [Testing Flow](project-docs/docs/TESTING_FLOW.md)
- [Dataset Format](project-docs/docs/DATASET_FORMAT.md)
- [Evaluation Strategy](project-docs/docs/EVALUATION_STRATEGY.md)
- [Roadmap](project-docs/docs/ROADMAP.md)
- [Security and Cost Controls](project-docs/docs/SECURITY_AND_COST.md)
- [Sample dataset](project-docs/examples/datasets/order_agent_v1.json)

## MVP Scope

The first milestone focuses on immutable, versioned datasets and cases; HTTP and in-process Python agent adapters; deterministic mock tools; normalized execution traces; deterministic evaluators (with explicitly configured optional LLM judging); asynchronous experiment runs; baseline comparisons; machine-readable reports; and API/CLI workflows for experiments and CI gates.

The MVP is backend/API-first. A dashboard, dedicated workers, distributed queues, full multi-tenancy, and hosted execution are deferred until the core evaluation workflow is reliable. The design documents describe the target MVP; implementation is being delivered in milestones.

## MVP Architecture

- **API:** Python, FastAPI, and Pydantic
- **Database:** PostgreSQL, SQLAlchemy, and Alembic
- **Execution:** In-process background runner with explicit run states and bounded concurrency
- **Agent integrations:** HTTP and in-process Python adapters using one normalized contract
- **Interfaces:** API and minimal CLI over shared application services
- **Local model support:** Ollama for development
- **Tests and CI:** pytest and GitHub Actions

## Local Development

Requirements: Python 3.13 (selected by `.python-version`), `uv`, and Docker Engine with Compose v2.

```sh
cp .env.example .env
uv lock
uv sync --frozen
docker compose up -d --wait postgres
docker compose ps
uv run --package agenteval-api uvicorn app.main:app --reload
```

The API runs in the local Python environment; Compose starts PostgreSQL only. PostgreSQL is published on `127.0.0.1:55432`. Run `docker compose down` to stop it; the named development volume is preserved. Values in `.env.example` are local placeholders. Run `uv lock` after changing dependencies; use `uv sync --frozen` to install from the lockfile.

The FastAPI lifespan owns the database engine: create the engine and session factory at startup, then dispose of the engine at shutdown. Use a short-lived session per request or unit of work with explicit commit/rollback and guaranteed close. Never share sessions across concurrent tasks.
