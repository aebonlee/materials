# 07 · HARNESS CANVAS — MY AGENT HARNESS (Day 2)

> AGENT HARNESS LAB · 웹 버전: /harness-lab (채우면 구조도가 실시간으로 그려집니다)

| # | 항목 | 내용 | 채우는 교시 |
|---|---|---|---|
| 01 | GOAL | (01_agent_canvas 에서) | Day 1 |
| 02 | CONTEXT | (02_context_map 요약) | Day 1 |
| 03 | TOOLS | (03_tool_card 목록) | Day 1 |
| 04 | GUARDRAILS | AUTO / ASK / DENY 목록 + 내용 규칙 (04_permission_matrix) | 2교시 |
| 05 | EVALUATION | 6기준 + PASS / RETRY / HUMAN REVIEW 규칙 (05_evaluation_checklist) | 3교시 |
| 06 | FAILURE | 실패로 보는 상황 (06_failure_test 에서) | 1·4교시 |
| 07 | RETRY | 최대 횟수 · 무엇을 붙여 다시 시도하나 · 우회 · 축소 | 4교시 |
| 08 | STOP CONDITION | 이 조건이면 멈추고 보고 | 4교시 |
| + | HUMAN CHECKPOINT | 사람이 서는 자리 (발송 전 · RETRY 소진 · 안전 실패) | 4·6교시 |

## 개념도 순서 (대표 개념도)

```
GOAL → CONTEXT → [TOOLS · MEMORY →] AGENT → GUARDRAILS → ACTION → EVALUATE
                                                              ├─ PASS → DONE
                                                              └─ FAIL → FEEDBACK → (RETRY, MAX N) → AGENT
```

## Failure Test 재실행 비교

| 테스트 | Day 1 (v1) 반응 | Harness 붙인 뒤 반응 | 막았나 |
|---|---|---|---|
| | | | |
