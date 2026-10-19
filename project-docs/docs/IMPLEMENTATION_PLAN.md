# Backend Implementation Plan

## 1. Goal and delivery rule

Prove one reliable evaluation workflow before adding distributed infrastructure or a user interface:

`versioned dataset → controlled agent run → trace → deterministic evaluation → baseline comparison → JSON report → CLI gate`

The MVP is a single-user, local-first FastAPI service backed by PostgreSQL. FastAPI background execution is sufficient only while runs fit the reliability and concurrency limits defined below. Each increment must add automated tests for its core contract before the next increment begins.

## 2. MVP implementation sequence

### Milestone 1 — Foundation and contracts

Create the Python package layout, FastAPI application, PostgreSQL configuration, SQLAlchemy models, Alembic migrations, Pydantic request/response schemas, and test fixtures. Define stable IDs, UTC timestamps, explicit version fields, and the experiment/case state machines.

**Done when:** migrations create the core schema and unit tests cover state transitions and schema validation.

### Milestone 2 — Versioned datasets

Implement dataset creation, JSON/JSONL import validation, content hashing, immutable publishing, and retrieval. Reject mutation of a published version; model edits as a new version. Add CLI dataset import and API contract tests.

**Done when:** the sample order dataset imports, can be retrieved by version, and invalid or mutated published data is rejected.

### Milestone 3 — Agent and tool contracts

Implement the normalized request/result schema, adapter registry, trusted in-process Python adapter, HTTP adapter, and deterministic mock-tool runtime. Capture telemetry capability explicitly for HTTP agents. Do not support uploaded Python code.

**Done when:** the same case can run through both adapters and produce a valid normalized result; Python-agent tests verify tool calls against mock fixtures.

### Milestone 4 — Execution and trace capture

Implement `ExecutionService` with FastAPI background execution, bounded concurrency, per-case timeout, explicit attempts, idempotent finalization, and structured error persistence. Persist ordered tool calls, spans, latency, and raw usage when supplied.

**Done when:** a 20–30-case experiment progresses through valid states, records partial outcomes after a case error, and returns a final report after all work ends.

### Milestone 5 — Deterministic evaluation and reports

Implement the evaluator interface plus schema/output, tool selection, argument, trajectory, and business-rule evaluators. Persist per-evaluator evidence and calculate a case decision from hard constraints and configured thresholds. Add baseline comparison and JSON report export. LLM judging remains opt-in and records rubric/model metadata.

**Done when:** an intentional tool or business-rule regression is visible per case and in a baseline comparison.

### Milestone 6 — API, CLI, and local CI gate

Finish API resources for experiments, results, traces, comparisons, reports, and gates. Provide CLI commands for import, run, inspect, export, compare, and gate. The CLI uses the API/application services; it must return nonzero only for a failed configured gate or operational failure.

**Done when:** a scripted local run imports data, executes an agent, exports JSON, and fails a shell command for a known hard-constraint regression.

## 3. MVP acceptance suite

- Dataset versions are content-addressed, immutable, and selected explicitly by experiments.
- HTTP and Python adapters satisfy the same normalized result contract.
- Mock-tool cases are deterministic and isolate forbidden tool behavior.
- Case `failed` and case `error` remain distinct in API, storage, reports, and metrics.
- Runs preserve enough configuration and trace metadata to explain results.
- Baseline comparison uses the same dataset version and reports changed cases.
- Automated unit and integration tests cover the contracts above.

## 4. Deferred Features & Future Roadmap

The MVP must not prebuild workers, queues, a dashboard, tenant control, hosted sandboxes, or framework-specific integrations. Use interfaces only where they are already exercised today: `AgentAdapter`, `ToolRuntime`, `Evaluator`, `ExecutionService`, repositories, and report/gate services. The full register, including each feature's phase, dependencies, trigger, and acceptance criteria, is maintained in [ROADMAP.md](ROADMAP.md#deferred-features--future-roadmap).

## 5. Scope-change rule

Treat the roadmap as a living scope record. Before implementing a deferred item, update its row with the observed trigger, concrete design decision, and revised acceptance criteria. Record a rejected or replaced item rather than silently removing it.
