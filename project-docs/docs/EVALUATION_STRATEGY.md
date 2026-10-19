# Evaluation Strategy

## 1. Core principle

Do not use a third agent as the only source of truth. Determine correctness with ground truth, deterministic rules and source data wherever possible. Use an LLM judge as an optional evaluator for open-ended qualities that cannot be reliably checked by code alone.

## 2. Evaluator hierarchy

### A. Deterministic evaluators
Examples:
- Output schema is valid.
- Required JSON fields are present.
- Correct tool was called.
- Tool arguments match expected values.
- Required tools were called.
- Forbidden tools were not called.
- Tool-call order satisfies constraints.
- Result matches a test database fixture.
- Latency/timeout/usage limits are met.

These are usually cheaper and more reproducible than LLM judges.

### B. Ground-truth evaluators
Compare output to verified expected facts or answers. Use exact comparison for stable values and field-level comparison for structured data.

### C. LLM-as-a-Judge
Use for dimensions such as:
- Relevance.
- Completeness.
- Clarity.
- Grounding in supplied sources.
- Following a rubric.

Provide a structured rubric and ask for machine-readable results with reasons. Track judge model/version and prompt version. Judge scores can be noisy and biased; calibrate them against human-reviewed examples.

### D. Human review — deferred
Human review is a future capability for judge calibration, disputed cases, and high-impact scenarios. The MVP stores evaluator evidence so reviewed decisions can be added later; it does not build a review workflow.

## 3. Hard constraints and quality score

Separate:
- **Hard constraints:** must pass, such as no unauthorized refund or no secret disclosure.
- **Quality dimensions:** scored dimensions such as relevance or completeness.

A case passes only if all required hard constraints pass and its configured quality threshold is met. Do not blindly average all evaluator scores: a critical policy violation should not be offset by good writing quality.

## 4. Metrics

- Test pass rate = passed cases / eligible completed cases. Define how errors and skipped cases are treated.
- Task success rate = cases satisfying task-success criteria / eligible cases.
- Tool selection accuracy.
- Tool argument correctness.
- Constraint violation rate.
- P50/P95 latency.
- Timeout, error and retry rate.
- Token usage and estimated cost per task.
- Cost per successful task.
- Run-to-run consistency for selected cases.

Keep deterministic pass rate separate from LLM judge quality scores. Normalize metrics carefully and document denominators.

## 5. Fair comparison

For Agent A vs Agent B:
- Use the same immutable dataset version.
- Use equivalent tool fixtures and permissions.
- Pin evaluator and judge versions.
- Record model, prompt, agent code/config and adapter versions.
- Control concurrency and timeouts.
- Compare per-case outcomes as well as aggregates.
- Repeat selected cases if stochasticity materially affects outcomes.
- Report uncertainty where appropriate.

Conclusions apply to the tested workload; a single dataset cannot prove one agent is universally more accurate.

## 6. LLM judge cost and reliability

- Run deterministic evaluators first.
- Invoke the judge only when needed.
- Limit judge calls and output tokens.
- Cache judge results when the exact input, output, rubric and judge version are unchanged.
- Record judge usage and cost separately.
- Periodically compare judge decisions against human-reviewed samples.

## 7. MVP boundary and deferred quality work

The MVP implements deterministic evaluators and may invoke an LLM judge only when an experiment explicitly configures one. It records the judge model, prompt/rubric version, input/output limits, result, and usage when available. It does not claim calibrated judge quality.

Pairwise evaluators, custom Python evaluators, statistical aggregation, domain-specific metrics, judge calibration, reference-based scoring, inter-judge agreement, bias analysis, confidence intervals, and advanced regression thresholds are deferred to Phase 2. Their dependencies and acceptance criteria are in [the roadmap](ROADMAP.md#phase-2--reliability-scalability-and-evaluation-quality).
