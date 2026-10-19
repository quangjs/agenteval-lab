# Roadmap

## Phase 1 — MVP: Core Evaluation Engine

Build the backend/API-first workflow: immutable versioned datasets; HTTP and trusted in-process Python adapters; deterministic mock tools; traces, tool calls, errors, latency and usage when available; deterministic evaluators; optional configured LLM judge; asynchronous in-process experiment runs; baseline comparison; JSON reports; a minimal CLI/API gate; PostgreSQL persistence; and automated core tests.

**Exit criteria:** a developer can import the sample dataset, run 20–30 controlled cases through either adapter, inspect per-case evidence, compare with a baseline, export JSON, and receive a failing CLI exit code for a known hard-constraint regression.

## Deferred Features & Future Roadmap

All entries below have **Status: Deferred**. This register is authoritative: update the entry with evidence when a feature is implemented, rejected, or replaced. “Dependencies” are prerequisites, and “Trigger” is the measurable reason to begin the work.

## Phase 2 — Reliability, Scalability, and Evaluation Quality

| Feature | Purpose and value | Reason for deferral | Dependencies | Trigger | Acceptance criteria |
|---|---|---|---|---|---|
| Dedicated workers and durable job queue | Recover long runs, apply retries, cancellation, and durable concurrency control. | The in-process runner proves the execution contract first. | Stable run states and `ExecutionService`; persisted attempts. | Process restarts can lose required work or run volume exceeds one process. | Jobs survive restart, obey limits, support cancellation, and preserve current result semantics. |
| Distributed execution | Increase throughput across machines. | Adds deployment and coordination cost. | Dedicated queue/workers and isolation model. | Sustained workload exceeds one worker's capacity. | Multiple workers execute without duplicate case completion or inconsistent reports. |
| Advanced scheduling | Support batches, priorities, resource limits, and policies. | No measured contention in MVP. | Durable jobs and worker metrics. | Competing runs cause unacceptable wait time or resource contention. | Policies are configurable, fair, observable, and covered by integration tests. |
| Evaluation caching | Reuse safe identical work and reduce cost. | Incorrect invalidation can invalidate comparisons. | Content hashes and complete configuration fingerprints. | Repeated identical evaluations have material measured cost. | Cache keys include all relevant inputs; hits/misses are reported; invalidation is tested. |
| Advanced reproducibility | Pin model/prompt/config, control randomness, and expose nondeterminism. | MVP first establishes basic metadata capture. | Stable adapters, configuration snapshots, trace schema. | Re-runs cannot be explained with stored metadata. | Reports classify reproducible versus external/nondeterministic dependencies. |
| Advanced evaluators | Add pairwise, rubric, custom Python, statistical, and domain metrics. | Deterministic core evaluators need validation first. | Evaluator interface and trusted execution boundary. | Repeated users need judgments current evaluators cannot express. | Each evaluator has versioned configuration, evidence, tests, and documented limits. |
| LLM-judge reliability | Calibrate judges, use references, measure agreement/bias, track versions. | Judge scores lack value before human-reviewed calibration data exists. | Opt-in judge, saved rubric/model metadata, reviewed cases. | Judge decisions affect material decisions or disagree with reviewers. | Calibration set, agreement metrics, version tracking, and fallback policy are documented. |
| Regression analysis | Add confidence intervals, distributions, and configurable thresholds. | Small MVP samples do not justify statistical claims. | Repeated comparable runs and stable metrics. | Stochastic variation causes false regression decisions. | Reports show uncertainty and gate behavior is validated against known distributions. |
| Advanced trace analysis | Filter, search, compare, replay, and debug traces. | Core trace capture and retrieval come first. | Stable trace schema and retained payload policy. | Stored traces cannot diagnose common failures efficiently. | Users can query and compare a failed trace with a baseline under access rules. |
| Cost and performance analytics | Analyze percentiles, throughput, cost-quality tradeoffs. | Requires reliable normalized usage and enough data. | Usage capture, run history, cost mapping policy. | Cost or latency influences selection decisions. | Metrics define denominators, source data, estimates, and confidence limits. |

## Phase 3 — Developer Experience and CI/CD Integration

| Feature | Purpose and value | Reason for deferral | Dependencies | Trigger | Acceptance criteria |
|---|---|---|---|---|---|
| CI/CD integrations | Run evaluations in GitHub Actions and other systems. | Local CLI/API behavior must stabilize. | Stable CLI, report format, and gate semantics. | Teams repeatedly script local commands in CI. | Reference integration publishes report artifacts and returns correct build status. |
| Configurable quality gates and policies | Apply project/dataset/evaluator/environment-specific pass rules. | One explicit MVP gate validates the model first. | Stable metrics and baseline comparison. | Different workflows need different approved thresholds. | Versioned policies are evaluated deterministically and explain every decision. |
| Pull-request reports | Show a candidate-versus-baseline summary in review. | Needs CI identity and stable comparison output. | CI integration and report API. | Teams request review-time regression visibility. | A PR receives an attributable summary with changed cases and links/artifacts. |
| Dataset import/export and framework integrations | Exchange data and reach common agent ecosystems. | Avoid framework lock-in before core contracts mature. | Stable schemas, adapter contract, versioning rules. | Interoperability blocks adoption. | Each format/integration round-trips or documents loss and has compatibility tests. |
| SDKs | Provide Python and, if justified, TypeScript client libraries. | The API must settle before supporting clients. | Versioned API and auth strategy if hosted. | Repeated client boilerplate or external users. | SDK covers core workflow, versioning, errors, and examples; TypeScript requires demonstrated demand. |
| Versioned evaluation configuration files | Keep run configuration with application code. | The configuration model is still forming. | Stable schemas and CLI. | Teams need reproducible code-reviewable settings. | Files validate, pin versions, and produce the same API request. |
| Scheduled evaluations and triggers | Run recurring or event-driven benchmarks. | Manual/CI invocation establishes useful schedules first. | Durable execution and policy model. | A documented recurring need exists. | Schedules are observable, idempotent, and do not duplicate runs. |
| Webhooks and notifications | Inform systems/users of completion, failure, or regression. | Requires reliable delivery semantics and users. | Terminal run states, subscriptions, security model. | Polling or CI artifacts are insufficient. | Signed delivery, retries, observability, and event schemas are tested. |

## Phase 4 — Multi-User Platform and SaaS Capabilities

| Feature | Purpose and value | Reason for deferral | Dependencies | Trigger | Acceptance criteria |
|---|---|---|---|---|---|
| Organizations, projects, memberships, RBAC | Safely separate teams and resources. | MVP is intentionally single-user. | Owner/project-compatible records and authentication. | More than one team/user needs shared hosted data. | Every resource is scoped and role checks are integration-tested. |
| Authentication, API keys, rotation, auditing | Identify callers and protect access. | Local single-user workflow does not require it. | User model, transport security, audit policy. | Any non-local or multi-user access. | Auth is enforced on every endpoint; key rotation and audit trails work. |
| Tenant isolation and authorization | Prevent cross-tenant data access. | Has no value without tenants. | Organizations, RBAC, scoped queries. | Hosted multi-tenant use begins. | Isolation tests prove no cross-tenant read/write across every resource. |
| Hosted execution and isolated runtimes | Safely run customer-controlled integrations. | Trusted local Python is sufficient in MVP. | Sandboxing, tenancy, secrets, resource quotas. | Hosted users need execution beyond HTTP endpoints. | Runtimes are isolated, bounded, network-controlled, and disposable. |
| Secret management | Protect external-agent/tool credentials. | Local environment configuration suffices initially. | Auth, deployment platform, audit model. | Hosted or shared credential storage is required. | Secrets are encrypted, masked, scoped, rotated, and never included in traces. |
| Quotas, rate limits, billing, plans | Control shared-service cost and capacity. | No SaaS economics in MVP. | Tenant identity, metering, reliable usage. | Shared capacity or commercial offering. | Limits are enforced and metering is reconciled with usage records. |
| Retention, deletion, backups, disaster recovery | Govern persisted user data safely. | Local development data is not a hosted service. | Tenant model, storage inventory, operations. | Hosted data or contractual retention requirements. | Retention/deletion and restore drills meet stated policy. |
| Monitoring, audit logs, SLOs | Operate a reliable hosted service. | MVP does not provide a service-level commitment. | Production topology, telemetry, ownership. | Users depend on availability or support obligations begin. | Dashboards, alerts, audit events, and error budgets meet defined SLOs. |

## Phase 5 — Advanced and Enterprise Capabilities

| Feature | Purpose and value | Reason for deferral | Dependencies | Trigger | Acceptance criteria |
|---|---|---|---|---|---|
| Web dashboard | Manage datasets, runs, traces, and visualization visually. | API and CLI prove workflows first. | Stable API/report models and user research. | CLI/API is inadequate for frequent inspection tasks. | Dashboard completes core workflow using public API without duplicating logic. |
| Dataset curation and quality checks | Deduplicate, label, and improve evaluation data. | Core import/versioning comes first. | Dataset history and quality signals. | Dataset quality limits trustworthy outcomes. | Changes are versioned, auditable, and measurable against defined quality rules. |
| Synthetic and adversarial test generation | Broaden coverage and find failures. | Generated data needs strong review and verification. | Dataset quality workflow, safety policy, evaluators. | Coverage gaps are evidenced by incidents or review. | Generated cases have provenance, validation, and human/automated acceptance rules. |
| Safety, security, tool-abuse, and red-team evaluation | Test harmful behavior and robustness. | Requires threat models and safe environments. | Isolated tools, safety policy, specialized verifiers. | Risk assessment or incidents identify relevant threats. | Suites have safe fixtures, explicit pass criteria, and no production side effects. |
| Human review workflows | Resolve ambiguous quality judgments. | Operational overhead is unjustified before demand. | User/auth model, review queue, audit trail. | LLM/deterministic evaluation cannot resolve material cases. | Review decisions are attributed, auditable, and feed calibration data. |
| RAG, multi-agent, and long-running suites | Evaluate complex agent patterns. | Core single-agent execution must be dependable first. | Mature trace model, isolation, advanced evaluators. | Validated user demand for a specific pattern. | Each suite has controlled environment, independent verifier, and documented limits. |
| Benchmark sharing and templates | Reuse datasets and evaluation patterns. | Sharing needs governance and compatibility contracts. | Versioned artifacts, tenancy/governance policy. | Teams repeatedly duplicate evaluation assets. | Artifacts have ownership, compatibility metadata, and import/export validation. |
| Governance, compliance, enterprise deployment | Meet enterprise control and deployment requirements. | Premature without customers and requirements. | Auth, isolation, audit, operations. | Contractual or regulatory need is validated. | Requirements are mapped to controls and independently verified. |
| Upgrade/migration evaluation | Assess model, prompt, agent, and framework changes. | Baseline comparison covers the first simple form. | Advanced reproducibility and regression analysis. | Teams need migration evidence beyond basic baselines. | Reports pin compared configurations and quantify uncertainty where relevant. |
| Observability and experiment-tracking integrations | Connect external operational data. | Core trace/report schemas need stability. | Stable export/webhook/API contracts. | Users repeatedly correlate AgentEval results with external systems. | Integration preserves identifiers, redaction, and documented failure handling. |

## Scope management

Do not implement a deferred feature because an abstraction might be useful. Pull an item forward only when its trigger is observed and its dependencies are complete. Before work starts, change its status to **Planned**, record the evidence, and refine acceptance criteria. Mark it **Implemented**, **Rejected**, or **Replaced** after the decision; never silently remove it.
