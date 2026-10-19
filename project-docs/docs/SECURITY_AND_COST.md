# Security, Isolation and Cost Controls

## 1. Execution safety

- Do not execute user-uploaded code inside the API process. The MVP Python adapter invokes trusted, locally registered code only.
- Treat agent output, tool arguments, MCP payloads and dataset content as untrusted.
- Hosted sandboxing and execution of untrusted code are deferred; do not add a partial sandbox to the MVP.
- Use dedicated test credentials and least-privilege permissions.
- Do not allow production side effects by default.
- Require explicit configuration/approval for tools that can refund, delete, send messages or mutate real data.
- Redact credentials and sensitive fields from traces.
- The MVP is single-user/local-first. Preserve owner/project-compatible records, but defer organization/project authorization enforcement until multi-user hosting is needed.

## 2. Mock-first strategy

Develop and test most platform features using:
1. Deterministic mock agent results to test the runner/evaluator infrastructure.
2. A local model such as Ollama to exercise real model behavior without per-request API billing.
3. Limited provider API tests for real-world quality, latency and usage.

Local inference is not literally free: it consumes hardware, electricity and time. Quality depends on the model and local hardware.

## 3. Cost controls

- Maximum test cases per experiment.
- Maximum model calls per case.
- Maximum agent steps and tool calls.
- Per-case and experiment timeout.
- Concurrency limits.
- Maximum input/output token budget where supported.
- Experiment-level estimated budget.
- Stop or require approval when a budget threshold is reached.
- Rerun failed cases only when appropriate.
- Run deterministic evaluators before paid LLM judges.
- Record raw provider usage separately from estimated cost.
- Set provider-side limits where the provider offers them.

Application-level budgets are only reliable if model calls are routed through a controlled layer. Remote agents may make hidden model calls that the platform cannot meter unless they expose usage telemetry.

## 4. Secrets

- Never store API keys in plaintext in `agent_configs`.
- Use environment variables for local development and a secret manager for hosted deployments.
- Mask secrets in logs, traces and error messages.
- Keep separate credentials for development, staging and production.
- Rotate credentials if exposed.

For the local MVP, provide HTTP-agent credentials through environment configuration and mask them in logs and traces. Do not add a hosted secret store until the multi-user/hosted trigger in the roadmap is met.

## 5. Trace privacy and retention

- Capture only the fields needed for debugging and evaluation.
- Provide configurable retention and deletion policies.
- Support redaction before persistence.
- Avoid putting personal or financial data into public demo datasets.
- Clearly indicate whether raw inputs/outputs are stored.

Configurable retention, deletion workflows, backups, disaster recovery, and access auditing are deferred platform capabilities. The MVP must still redact known credentials and use fictional data in its examples.

## 6. Deferred Features & Future Roadmap

Hosted runtimes, tenant isolation, authentication, secret management, quotas, operational monitoring, retention controls, and enterprise governance are intentionally deferred to Phase 4 or 5. Their dependencies, implementation triggers, and completion criteria are maintained in [ROADMAP.md](ROADMAP.md#phase-4--multi-user-platform-and-saas-capabilities).
