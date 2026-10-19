# Product Requirements — AgentEval Lab

## 1. Product vision

Build a developer-focused platform for testing and benchmarking AI agents. The platform evaluates not only final text output but also tool selection, tool arguments, execution trajectories, business-rule compliance, latency, usage and cost.

## 2. Target users

- AI engineers building tool-using agents.
- Backend/platform engineers operating agent systems.
- Teams comparing models, prompts, agent frameworks or workflow versions.
- Developers who want automated regression checks in CI.

## 3. MVP user journey

1. Create a project.
2. Create or import a dataset.
3. Register an agent adapter/configuration.
4. Select tool runtime: mock tools, MCP, or approved staging tools.
5. Create and run an experiment.
6. Inspect test-case results, traces, and machine-readable reports through the API or CLI.
7. Compare the experiment with a baseline.
8. Run a regression gate locally; use its exit status in CI.

## 4. MVP features

### Dataset management
- Create datasets and test cases.
- Import/export JSON or JSONL.
- Validate schema.
- Tag cases by domain, difficulty and scenario.
- Version datasets immutably.

### Agent configuration
- Support an in-process Python adapter and an HTTP adapter from the start.
- Normalize both modes into one request, result, tool-call, trace, usage, and error contract.
- Provide controlled mock tools to the Python adapter for deterministic tests.
- Accept that an HTTP agent may expose only final output unless it returns structured telemetry.
- Store non-secret configuration; secrets must use a secret store/environment configuration.

### Experiment execution
- Create experiment from a fixed dataset version and agent configuration.
- Run cases asynchronously with a background execution service in the initial FastAPI deployment.
- Limit concurrency, timeouts, retries, and total model calls; record execution failure separately from failed assertions.
- Capture outputs, tool calls, traces, errors and usage.

### Evaluation
- Deterministic output checks.
- Tool selection and argument checks.
- Trajectory/business-rule checks.
- Ground-truth comparison.
- Optional LLM-as-a-judge.
- Per-evaluator scores and explanations.

### Comparison and reporting
- Compare two experiments using the same dataset version.
- Show task success/pass rate, tool accuracy, constraint violations, latency and cost.
- Highlight changed test cases and regression reasons.
- Export results as JSON.

### CI integration
- Minimal CLI to import datasets, run and inspect experiments, export reports, and evaluate a gate.
- Gate by explicit hard constraints and baseline-comparison rules.
- Fail CI on hard-constraint violations.
- Return non-zero exit code when gate fails.

## 5. Non-goals for MVP

- Hosting arbitrary customer agent code in the main application process.
- Full enterprise billing and organization administration.
- Kubernetes or microservices from day one.
- Guaranteeing correctness of every open-ended answer.
- Replacing the user's production observability platform.
- Running production side-effecting tools by default.
- A web dashboard in the initial release.
- Dedicated workers, distributed queues, or multi-machine execution.
- Authentication, organizations, memberships, and billing.

## 6. Success criteria

A developer can:
- Import a dataset.
- Run at least 20–30 cases against a sample agent with mock tools.
- Inspect each case's output, tool calls and evaluator results.
- Compare two agent versions.
- Identify a regression and fail a CI job automatically.

## 7. Product principles

- Reproducibility over opaque aggregate scores.
- Deterministic evaluators before LLM judges where possible.
- Keep dataset, agent configuration, execution and evaluation separate.
- Show why a case passed or failed.
- Track quality alongside latency and cost.
- Make external tool access explicit and safe.
- Prove the core runner before adding distributed infrastructure or product surface area.

## 8. Future compatibility

Use stable identifiers and explicit versions for datasets, evaluator configuration, agent configuration, and experiments. Keep adapters, tool runtimes, evaluators, persistence, and execution orchestration behind focused interfaces. The MVP remains single-user and local-first, but its records must be capable of gaining an organization/project owner later. Do not add tenant enforcement, a queue abstraction with multiple implementations, or a frontend solely for hypothetical future needs.

## 9. Deferred Features & Future Roadmap

The complete deferred-feature register, including triggers and acceptance criteria, is maintained in [the roadmap](ROADMAP.md#deferred-features--future-roadmap). Those items are intentionally outside the MVP and must not be implemented early without recording a scope decision there.
