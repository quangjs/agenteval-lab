# Milestone 1 — Foundation and Contracts

**Status:** Section 0 complete; section 1 partially implemented; lock/runtime checks blocked by environment  
**Scope:** Foundation only. Application implementation has not started.  
**Source:** `project-docs/docs/IMPLEMENTATION_PLAN.md` (Milestone 1), `DETAILED_DESIGN.md`, and `SYSTEM_DESIGN.md`.

## Objective

Establish the Python/FastAPI/PostgreSQL foundation and only the domain contracts needed by later milestones. Keep this milestone small: no dataset import workflow, agent adapters, experiment execution, evaluator implementations, CLI, worker process, queue, dashboard, authentication, or tenant authorization.

## Proposed repository layout

```text
pyproject.toml                    # workspace metadata and locked dependencies
apps/api/app/                     # FastAPI app, settings, lifespan, HTTP boundary
packages/agenteval/src/agenteval/
  domain/                         # framework-independent IDs, states, rules
  schemas/                        # Pydantic boundary contracts
  persistence/                    # SQLAlchemy mappings, engine, session factory
migrations/                       # Alembic environment and initial revision
tests/unit/                       # domain and schema checks; no database required
tests/integration/                # PostgreSQL migration and persistence checks
compose.yaml                      # local PostgreSQL service for development/tests
.env.example                      # names and safe local defaults only
```

The API application may depend on `agenteval`; the domain layer must not depend on FastAPI or SQLAlchemy. Pydantic schemas must not import ORM models. Persistence may map to domain types and may use SQLAlchemy. Alembic imports the persistence metadata. Section 0 selects `uv` and repository-root migrations.

## Work plan and progress

Implementation checkboxes remain unchecked until there is a code or test result to cite. Add validation commands and outcomes to the progress log as work is completed.

### 0. Review and resolve setup decisions

- [x] User approves this revised plan and authorizes work on section 0. Evidence: user message “Approve, start implement #0”.
- [x] Select Python environment/package manager and lockfile format: `uv` workspace with `pyproject.toml` and `uv.lock`.
- [x] Pin PostgreSQL for local development and integration tests: PostgreSQL 18, using the current 18.6 minor image initially. The official project lists PostgreSQL 18 as supported through November 14, 2030 and recommends current minor releases.
- [x] Use Docker Compose for PostgreSQL only; run the API from the local Python environment in M1. This keeps container scope to local infrastructure while the app scaffold remains directly debuggable.
- [x] Select SQLAlchemy 2.x async engine/session with `asyncpg`; create the engine at app lifespan startup and use short-lived sessions per request/unit of work.
- [x] Pin agent configuration by immutable, versioned `AgentConfig` row reference from `Experiment`; each changed configuration creates a new version. Do not create a separate snapshot table in M1.
- [x] Validate project ownership and matching dataset-version/case relationships at the application service boundary when those workflows are implemented. Keep ordinary foreign keys in the M1 schema; do not add composite-key scaffolding before those workflows exist.
- [x] Use opaque, non-empty version strings (sample format `1.0`) with uniqueness within the owning dataset or named agent config.
- [x] Use unique `Project.name`, `Dataset(project_id, name)`, and `AgentConfig(project_id, name, version)`; allow multiple agent-config versions under one name.
- [x] Define dataset hashing as SHA-256 over UTF-8 JSON serialized with sorted object keys, compact separators, non-ASCII preserved, and non-finite numbers rejected. Hash the immutable dataset content (metadata and cases), excluding generated database IDs and timestamps.
- [x] Keep Alembic migrations in the repository-root `migrations/` directory shown in this plan.

### 1. Repository and application scaffold

- [x] Add workspace/package metadata, runtime dependencies, and pytest/Ruff configuration. Evidence: root `pyproject.toml`, `apps/api/pyproject.toml`, and `packages/agenteval/pyproject.toml`; all parse as TOML.
- [ ] Generate `uv.lock` and verify `uv sync --frozen`. Blocked: `uv lock` failed to resolve PyPI because network DNS is unavailable; do not create a synthetic lockfile.
- [x] Create the API and shared core package layout and package initializers. Evidence: `apps/api/app/` and `packages/agenteval/src/agenteval/` files exist.
- [x] Create the minimal FastAPI application factory and `main` entry point with no feature routes. Evidence: `apps/api/app/main.py` parses; runtime import/OpenAPI smoke check remains pending dependency installation.
- [x] Add typed settings, `.env.example`, and `.gitignore` protection for `.env`. Evidence: `apps/api/app/settings.py`, `.env.example`, and `git check-ignore .env`.
- [x] Establish dependency direction: API → core; domain independent of FastAPI/SQLAlchemy; schemas independent of ORM. Evidence: no FastAPI or SQLAlchemy imports in the domain or schema packages.
- [x] Document database engine/session lifecycle: create the engine once at application startup, close it at shutdown, and create/close a session per request or unit of work. Commit or roll back explicitly. Never share a session across concurrent tasks or retain a request session for future background work. Evidence: `project-docs/README.md` local development section; engine code remains in section 2.
- [x] Document clean-environment, Docker startup, and API startup commands. Evidence: `project-docs/README.md` and `AGENTS.md`.
- [ ] Add migration and test commands to the local development guide after sections 2 and 4 create those workflows.

#### Docker and local development environment

- [x] Add a Compose definition for PostgreSQL 18.6 with a health check, named development volume, and loopback-only published port. Evidence: `compose.yaml`; `docker compose config --quiet` succeeds. Starting the service remains pending because the Docker daemon is stopped.
- [x] Keep local credentials in ignored `.env`; commit only `.env.example` placeholders and document local-only use. Evidence: `.gitignore`, `.env.example`, and `git check-ignore .env`.
- [x] Configure the host-run API/test process to connect through `localhost` and the published port using `DATABASE_URL`. Evidence: `.env.example` and typed `Settings.database_url`.
- [x] Keep the default Compose stack limited to PostgreSQL; the API runs in the local Python environment for M1. Evidence: `docker compose config` lists only `postgres`.
- [x] Document Docker Engine/Compose v2 prerequisites and startup/health-check/shutdown commands; normal shutdown preserves the named volume. Evidence: `project-docs/README.md`; runtime health/persistence validation remains pending Docker daemon availability.
- [ ] Configure integration tests to create a uniquely named disposable database on the local PostgreSQL service and drop only that database after migration checks; never run destructive migration tests against the persistent development database.
- [x] Document the available local loop: install the Python environment, copy/configure `.env`, start PostgreSQL, run the API, and stop services. Evidence: `project-docs/README.md` local development section.
- [ ] Extend the local loop with migration and test commands after sections 2 and 4 create those workflows.

### 2. Persistence foundation

- [ ] Add SQLAlchemy base, selected engine/session factory, and Alembic configuration using the same settings source without exposing credentials.
- [ ] Retain the foundational entities below and document each table, relationship, constraint, and index in the migration review.
- [ ] Generate the initial migration and validate upgrade, downgrade, and re-upgrade against a disposable PostgreSQL database.

#### Entity decisions

| Entity | Milestone 1 decision | Basis |
|---|---|---|
| `Project` | Retain as a real, single-user product resource. | Product requirements and user journey begin with creating a project; system design assigns project access and quotas. This is a local grouping boundary, not an organization, user, or tenant model. |
| `Dataset` | Retain. | Dataset management and the API sketch create datasets. Give it one required `project_id`. |
| `DatasetVersion` | Retain. | Published versions are immutable, experiments pin versions, and hashes support auditability/reproducibility. |
| `DatasetItem` | Retain. | It stores the input, context, expected result, assertions, fixtures, and tags defined by the dataset format. |
| `AgentConfig` | Retain. | The API sketch registers agents and experiments pin the selected configuration. Give it one required `project_id`; no secret values. |
| `Experiment` | Retain. | It is the durable run definition and needs the MVP lifecycle, dataset version, agent configuration reference/snapshot, and limits. The exact config-pinning representation remains an approval question. |
| `TestCaseRun` | Retain. | It represents one dataset item in one experiment and is needed for case states and the required distinction between failed evaluations and execution errors. |
| `AgentConfigSnapshot` table | Defer as a separate table. | Detailed design allows either a snapshot or immutable configuration-version reference; this extra entity is unnecessary until that pinning choice is made. Preserve the ability to pin configuration on `Experiment`. |
| `TraceSpan` | Defer. | The design lists trace fields but leaves payload storage as JSON or references and does not define retention/query needs. Specify it with trace capture in the execution milestone. |
| `EvaluationResult` | Defer. | Evaluator names, versions, evidence, and result details belong to evaluator workflows; no evaluator executes in Milestone 1. |
| `ExperimentMetric` | Defer. | Metric names, denominators, normalized usage, and aggregation are defined with reporting, not needed for the foundation. |
| `BaselineComparison` | Defer. | Comparison semantics and report shape belong to the comparison workflow; a nullable baseline reference on `Experiment` can be decided when that workflow is implemented. |

#### Integrity requirements for retained tables

- [ ] Use UUID primary keys for durable records.
- [ ] Require `Project.name`, `Dataset.name`, `AgentConfig.name`, and version fields to be non-empty. Apply the approved uniqueness rules in the following integrity requirements.
- [ ] `Project.name` is unique. `Dataset(project_id, name)` is unique. `AgentConfig(project_id, name, version)` is unique; names may be reused for later versions.
- [ ] `Dataset.project_id` and `AgentConfig.project_id` are `NOT NULL` foreign keys to `Project.id`.
- [ ] `DatasetVersion.dataset_id` is `NOT NULL`; unique `(dataset_id, version)`; require a non-empty content hash. Do not make the hash globally unique because the design uses it for auditability, not deduplication.
- [ ] `DatasetItem.dataset_version_id` is `NOT NULL`; unique `(dataset_version_id, case_id)` so case identifiers cannot collide within one immutable version.
- [ ] `AgentConfig.version` is a non-empty opaque string; unique `(project_id, name, version)` so a named configuration version is stable while allowing multiple versions under one name.
- [ ] `Experiment.project_id`, `dataset_version_id`, and `agent_config_id` are `NOT NULL` references. The later experiment-creation service validates that the dataset and agent config belong to the selected project.
- [ ] `TestCaseRun.experiment_id` and `dataset_item_id` are `NOT NULL` references; unique `(experiment_id, dataset_item_id)` so an experiment has at most one run row per case. The later execution service validates that each item belongs to the experiment's pinned dataset version.
- [ ] Require `created_at` on durable rows. `started_at` and `finished_at` are nullable until their corresponding lifecycle events occur; no default fabricated timestamps for unstarted work.
- [ ] Use `ON DELETE RESTRICT` for all MVP foreign keys. No hard-delete API or cascade behavior is in scope; preserve referenced evaluation history.
- [ ] Index every foreign-key column used for joins. Add indexes for `(project_id, created_at)` on experiments and `(experiment_id, status)` on case runs to support expected listing/progress reads. Unique constraints provide indexes for dataset version and item identity lookups.
- [ ] Add no nullable ownership/organization/user columns and no organization, membership, or authorization tables.

### 3. Contracts, versioning, and state machines

- [ ] Define framework-independent experiment/case state values and transition rules in the domain layer.
- [ ] Define Pydantic core schemas for IDs, non-empty identifiers, versions, UTC timestamps, and statuses. Do not design feature request/response schemas for dataset import, experiment execution, traces, or evaluators yet.
- [ ] Define experiment states: `queued`, `running`, `completed`, `failed`.
- [ ] Define case states: `pending`, `running`, `passed`, `failed`, `error`, `skipped`.
- [ ] Allowed experiment transitions: `queued → running` or `queued → failed` (failure to start); `running → completed` or `running → failed` (unrecoverable experiment-level failure). `completed` and `failed` are terminal.
- [ ] Allowed case transitions: `pending → running` or `pending → skipped` (excluded before execution); `running → passed`, `running → failed`, or `running → error`. `passed`, `failed`, `error`, and `skipped` are terminal.
- [ ] Define `failed` as a valid execution/evaluation that did not satisfy required expectations. Define `error` as an adapter, infrastructure, or evaluator failure that prevented a valid evaluation. Case errors do not by themselves make an experiment `failed`; an experiment may be `completed` with failed or errored cases once every case is terminal.
- [ ] Do not include `cancelled`, retry transitions, attempt scheduling, or recovery behavior in this milestone. Cancellation and durable retries are not required by the approved MVP design for the foundation.
- [ ] Dataset and agent configuration versions are explicit, non-empty opaque identifiers unique within their parent resource. Content hash applies to canonical dataset-version content and is not a substitute for the version identifier. Dataset version content includes its cases, expectations, assertions, fixtures, and relevant dataset metadata; generated database IDs and timestamps are excluded.
- [ ] Store timestamps as timezone-aware UTC values (`TIMESTAMPTZ` in PostgreSQL); reject naive input timestamps and serialize in ISO 8601 UTC form. Define one shared timestamp helper/validation rule rather than per-table conventions.

### 4. Automated checks and completion review

- [ ] Add unit tests for every allowed transition and representative forbidden transitions, including terminal-state changes and failed/error separation.
- [ ] Add unit tests for schema validation: UUIDs, non-empty IDs/version strings, timezone-aware datetime normalization, invalid states, and rejected naive datetimes.
- [ ] Add PostgreSQL integration tests that use a newly created disposable database, apply `alembic upgrade head`, assert expected tables/foreign keys/unique constraints/delete rules/indexes, run `alembic downgrade base`, confirm project tables are removed, then upgrade to `head` again. Never target a developer database.
- [ ] Include reproducible setup: pinned supported Python and PostgreSQL versions, dependency lock, Docker/Compose prerequisites, safe configuration example, and exact commands for environment creation, database startup, migration, app startup, unit tests, and integration tests.
- [ ] Verify a clean environment can start the Compose database, wait for its healthy state, connect from the local app/test environment, and shut down without losing the named development volume. Blocked here: Docker CLI is installed, but Docker Desktop has no executable and no daemon is reachable.
- [ ] Run the documented setup from a clean environment and record exact commands and outcomes.
- [ ] Confirm the minimal FastAPI app imports/starts and OpenAPI generation works without adding feature routes.
- [ ] Review the implementation diff against scope and this plan. Mark milestone complete only after all acceptance criteria have recorded evidence.

## Acceptance criteria

- A clean checkout can follow documented, pinned setup steps to install dependencies and connect to a disposable PostgreSQL instance.
- Docker Compose starts the pinned local PostgreSQL service, reports it healthy, and exposes it only on loopback; ordinary shutdown preserves development data.
- The app and test process can connect to the Compose database using the documented local configuration.
- The minimal FastAPI application imports, starts, and generates OpenAPI with the documented environment settings.
- `alembic upgrade head` creates exactly the approved Milestone 1 schema; downgrade to `base` removes it; a second upgrade succeeds, all against a disposable PostgreSQL database.
- Integration assertions verify all approved foreign keys, required nullability, uniqueness constraints, `ON DELETE RESTRICT` behavior, and listed indexes.
- Unit tests cover every state transition and schema rule listed above and pass without PostgreSQL.
- UTC-aware values persist and round-trip as UTC; naive datetime input is rejected.
- Package dependency checks/review show that domain rules do not import FastAPI/SQLAlchemy and Pydantic schemas do not import ORM models.
- No feature workflows or later-phase infrastructure are included.

## Scope exclusions

Dataset import/version publishing, agent adapters, mock tool runtime, experiment runner/background tasks, cancellation, retries, evaluators, traces, baseline comparisons, report export, CLI, external queue/workers, authentication/tenancy, dashboard, hosted execution, and later-phase features remain out of scope. Do not expand Milestone 1 to include them.

## Decision record

Section 0 is complete. The decisions above resolve the implementation setup questions using the approved scope and current design documents. The PostgreSQL version choice follows the project's [official versioning policy](https://www.postgresql.org/support/versioning/). If implementation evidence requires changing a decision, record the reason and update this plan before expanding scope.

## Progress log

| Date | Update | Evidence / follow-up |
|---|---|---|
| 2026-10-21 | Plan revised against review feedback; implementation remains unstarted. | Re-read implementation plan and both architecture documents; entity rationale, project ownership, integrity rules, state semantics, reproducibility criteria, and approval questions are recorded above. All implementation checklist items remain unchecked. |
| 2026-10-21 | Added Docker and local development environment tasks and acceptance criteria; implementation remains unstarted. | Plan now covers a pinned PostgreSQL Compose service, local configuration, health checks, persistent dev data, disposable integration databases, and documented developer commands. All implementation checklist items remain unchecked. |
| 2026-10-21 | Completed section 0 under user approval; application implementation remains unstarted. | Resolved toolchain, PostgreSQL 18.6 initial image, Compose scope, async SQLAlchemy, configuration pinning, consistency validation, version and naming policies, hash format, and migration location. Evidence includes this decision record, the approved scope, and the [PostgreSQL version policy](https://www.postgresql.org/support/versioning/). |
| 2026-10-21 | Started section 1; implemented workspace/package metadata, app scaffold, typed settings, dependency boundaries, and local PostgreSQL Compose setup. | Python AST/TOML parsing passed; `docker compose config --quiet` passed; `.env` ignore check passed. `uv lock` is blocked by PyPI DNS failure; FastAPI is not installed in the available interpreter; Docker daemon is unavailable. Lock/install, app startup/OpenAPI, PostgreSQL startup, and remaining local-loop verification stay unchecked. |
| 2026-10-21 | Attempted to bring up local Docker for section 1 validation. | `open /Applications/Docker.app` reports the app executable is missing; Docker has no reachable daemon. No containers were started. |
| 2026-10-21 | Relaxed the Python toolchain pin to the supported 3.13 release line after the exact 3.13.16 pin prevented `uv lock` on the developer machine. | `.python-version` now requests `3.13`, which is compatible with `requires-python = ">=3.13,<3.14"`; README and contributor setup guidance now match. `uv python find 3.13` resolves the installed Python 3.13.5. Exact clean-environment lock/sync verification remains pending because this environment cannot reach package/download hosts. |
| 2026-10-21 | Fixed editable wheel discovery for `agenteval-core`. | Added Hatchling wheel package selection `src/agenteval` in `packages/agenteval/pyproject.toml`. The OpenAPI smoke command now builds both `agenteval-api` and `agenteval-core`; execution then stops while downloading `annotated-types` because this environment cannot resolve `files.pythonhosted.org`. Full OpenAPI output remains pending. |
