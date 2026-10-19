# Detailed Design

## 1. Proposed repository structure

```text
agenteval-lab/
  apps/
    api/
      app/
        api/v1/          # HTTP routes and CLI-facing application services
        datasets/
        agents/
        experiments/
        reports/
        execution/       # in-process background runner
  packages/
    agenteval/
      schemas/
      adapters/          # http and python adapters
      tool_runtimes/     # deterministic mock tools
      evaluators/
      tracing/
      metrics/
      storage/
  tests/
    unit/
    integration/
  examples/
    datasets/
  docs/
```

The API and core package may share one repository and deployment initially. The CLI is a thin client of the same application services or API contract; it must not contain a second execution engine.

## 2. Domain model

MVP records: `Dataset`, immutable `DatasetVersion`, `DatasetItem`, `AgentConfig`, immutable `AgentConfigSnapshot`, `Experiment`, `TestCaseRun`, `TraceSpan`, `EvaluationResult`, `ExperimentMetric`, and `BaselineComparison`.

Every durable record has a stable ID and timestamps. A dataset version stores a content hash. An experiment stores the selected dataset version, agent snapshot, tool-runtime and evaluator configuration, limits, baseline reference when used, and terminal status. A case run stores attempt count, final output, structured error, latency, raw usage, and normalized usage. Trace spans include sequence number, parent reference, kind (`agent`, `model`, `tool`, `evaluator`), timestamps, duration, redacted payload references, and attributes.

MVP records do not require organizations or authentication. Keep project/owner references nullable or encapsulate access through repositories so tenancy can be added by migration and authorization middleware later.

## 3. Shared adapter contract

Both adapter types implement a single asynchronous interface. The schema is deliberately small:

```python
class AgentAdapter(Protocol):
    async def run(self, request: AgentRequest, runtime: ToolRuntime) -> AgentResult: ...
```

`AgentRequest` contains input, context, execution identifiers, deadline, and approved configuration. `AgentResult` contains output, ordered `ToolCall` records, trace spans, usage, latency, and an optional structured error. The Python adapter invokes a trusted registered callable and supplies controlled mock tools. The HTTP adapter sends a versioned request to a configured endpoint and normalizes returned telemetry. If an HTTP agent returns only output, tool calls and traces are empty with an explicit telemetry-capability marker.

The MVP does not run user-uploaded Python. Cancellation, retries, and timeout behavior belong to the execution service rather than individual adapters.

## 4. Execution and evaluation

`ExecutionService` owns state transitions and accepts an experiment ID. Its first implementation schedules bounded asynchronous work inside the FastAPI deployment. It validates pinned configuration, creates case runs, applies per-case deadlines and concurrency limits, records attempts, invokes adapters, runs evaluators, and finalizes the experiment idempotently. It must be replaceable by a worker/queue-backed implementation without changing its public contract.

Evaluator results are stored independently. The aggregate case decision requires every configured hard constraint to pass and any configured quality threshold to be met. Deterministic schema, output, tool, trajectory, and business-rule evaluators are MVP requirements. LLM judging is optional, explicitly configured, and stores its model, prompt/rubric, and usage metadata.

## 5. API and CLI surface

| Operation | API | CLI |
|---|---|---|
| Import/publish dataset version | `POST /v1/datasets`, `POST /v1/datasets/{id}/versions` | `dataset import` |
| Register agent configuration | `POST /v1/agents` | `agent register` |
| Start or inspect experiment | `POST /v1/experiments`, `GET /v1/experiments/{id}` | `experiment run`, `experiment get` |
| Read results and traces | `GET /v1/experiments/{id}/results`, `/traces` | `experiment results` |
| Compare and export | `POST /v1/experiments/{id}/compare`, `GET /reports/...` | `compare`, `report export` |
| Apply CI gate | `POST /v1/experiments/{id}/gate` | `gate` |

Experiment creation returns `202 Accepted`. Initial progress delivery is polling. Reports use JSON first; stable schemas and exit codes are part of the CLI contract.

## 6. Deferred Features & Future Roadmap

The MVP intentionally has one execution implementation, no dashboard, and no tenant control plane. Future worker/queue, scheduler, cache, framework adapter, observability, SaaS, and dashboard work must preserve these contracts rather than expand them preemptively. The feature-by-feature ownership, dependencies, measurable triggers, and acceptance criteria are in [ROADMAP.md](ROADMAP.md#deferred-features--future-roadmap).
