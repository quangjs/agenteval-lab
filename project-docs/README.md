# AgentEval Lab

AgentEval Lab là platform để kiểm thử, đánh giá, benchmark và theo dõi regression của AI agents.

Mục tiêu là giúp developer trả lời các câu hỏi:

- Agent có hoàn thành nhiệm vụ chính xác không?
- Agent có gọi đúng tool, truyền đúng arguments và tuân thủ business rules không?
- Phiên bản agent/model/prompt mới có tốt hơn baseline không?
- Chất lượng đó đạt được với latency và chi phí bao nhiêu?
- Khi test thất bại, có thể truy ngược execution trace để tìm nguyên nhân không?

## Tài liệu dự án

- [Product Requirements](docs/PRODUCT_REQUIREMENTS.md)
- [High-level System Design](docs/SYSTEM_DESIGN.md)
- [Detailed Design](docs/DETAILED_DESIGN.md)
- [Backend Implementation Plan](docs/IMPLEMENTATION_PLAN.md)
- [Testing Flow](docs/TESTING_FLOW.md)
- [Dataset Format](docs/DATASET_FORMAT.md)
- [Evaluation Strategy](docs/EVALUATION_STRATEGY.md)
- [Roadmap](docs/ROADMAP.md)
- [Security and Cost Controls](docs/SECURITY_AND_COST.md)
- [Sample dataset](examples/datasets/order_agent_v1.json)

## MVP scope

1. Import/create JSON datasets with versioning.
2. Register an agent through an adapter.
3. Run test cases using deterministic mock tools.
4. Capture output, tool calls, traces, latency and usage.
5. Evaluate results using deterministic evaluators and optional LLM judge.
6. Compare experiment results against a baseline.
7. Expose API endpoints and a minimal CLI for execution, reporting, and CI gates.

## MVP architecture

- API: Python + FastAPI + Pydantic
- Database: PostgreSQL + SQLAlchemy + Alembic
- Execution: in-process background runner with explicit run states and bounded concurrency
- Integrations: HTTP agents and in-process Python agents through one normalized contract
- Interface: API and CLI over the same application services
- Local model: Ollama for development
- Test: pytest
- CI: GitHub Actions

The first release is backend/API-first. A web dashboard, dedicated workers, distributed queues, multi-tenancy, and hosted execution are deferred until the core evaluation workflow is reliable. Commands, endpoints, and schemas in these documents are design specifications, not yet implemented.
