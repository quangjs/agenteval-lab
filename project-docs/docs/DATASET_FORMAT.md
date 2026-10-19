# Dataset Format

## 1. Design principles

A test case includes:
- `input`: the user request or task.
- `context`: additional context such as user or tenant identifiers.
- `expected`: expected result, behavior or constraints.
- `assertions`: evaluators to apply.
- `fixtures`: optional deterministic data for tools.
- `tags` and `difficulty`: filtering and reporting metadata.

Not every case needs an exact expected output string. Use structured ground truth for deterministic tasks and rubrics/source references for open-ended tasks.

## 2. Recommended JSON structure

```json
{
  "dataset_id": "order-agent-v1",
  "name": "Order Management Agent Tests",
  "version": "1.0",
  "test_cases": [
    {
      "id": "TC001",
      "name": "Tra cứu đơn hàng hợp lệ",
      "input": {
        "message": "Kiểm tra giúp tôi đơn hàng ORD-1001 đang ở trạng thái nào?"
      },
      "context": {
        "customer_id": "CUS-001"
      },
      "expected": {
        "intent": "check_order_status",
        "tool_calls": [
          {
            "tool": "get_order",
            "arguments": {
              "order_id": "ORD-1001"
            }
          }
        ],
        "output_contains": [
          "ORD-1001",
          "đang giao"
        ]
      },
      "assertions": [
        "correct_tool",
        "correct_tool_arguments",
        "correct_order_status",
        "no_unauthorized_actions"
      ],
      "tags": ["order", "happy-path"],
      "difficulty": "easy"
    }
  ]
}
```

## 3. Example cases

See [`../examples/datasets/order_agent_v1.json`](../examples/datasets/order_agent_v1.json) for a complete three-case sample:
- Valid order lookup.
- Unknown order.
- Refund request that must not call the refund tool before payment verification.

The data is fictional and intended for local test fixtures.

## 4. Expected output patterns

Prefer structured expectations where possible:

### Exact or structured output
For stable structured outputs, compare selected JSON fields or validate against a JSON Schema.

### Contains / semantic output
For natural language, use required facts, source grounding, rubric-based judge, or human review. Avoid relying only on exact string matching.

### Tool-call expectation
Test the tool name, required arguments, number of calls, order/trajectory and forbidden tools. Tool-call traces may only be available when the adapter/runtime exposes them.

### Business constraints
Use explicit hard constraints such as “must not call refund_order unless payment is verified”. These should fail the case even if the final text appears plausible.

## 5. Fixtures and mock behavior

Fixtures define deterministic tool data for a test case. Tool mock configuration may be stored separately from the dataset if multiple datasets share the same runtime.

Example mock configuration:

```json
{
  "tool_name": "get_order",
  "cases": [
    {
      "when": {
        "order_id": "ORD-1001"
      },
      "returns": {
        "order_id": "ORD-1001",
        "status": "shipping"
      }
    }
  ],
  "default_response": {
    "error": "ORDER_NOT_FOUND"
  }
}
```

## 6. Versioning

- Published dataset versions are immutable.
- Changing inputs, expected outcomes, fixtures or assertions creates a new version.
- Experiments must reference a specific version.
- Store a content hash for auditability.
