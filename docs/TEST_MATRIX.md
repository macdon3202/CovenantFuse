# Test matrix

| Path / attack | Required result |
|---|---|
| Narrow exception preserves safeguard | `ACTIVE` |
| Exact consumer + exact action digest | `CONSUMED` once |
| Direct contradiction or bypass | `BLOCKED` |
| Scope mismatch | `BLOCKED` |
| Ambiguous relationship | non-positive |
| Mandatory field `UNKNOWN` | `UNRESOLVED` |
| Malformed model schema | `UNRESOLVED` |
| Consensus failure | `UNRESOLVED` |
| Creator self-review | revert; complete docket unchanged |
| Consume before review | revert; complete docket unchanged |
| Wrong consumer | revert; complete docket unchanged |
| Wrong action digest | revert; complete docket unchanged |
| Replay consumed permit | revert; terminal state unchanged |
| Cancel twice or cancel terminal docket | revert; state unchanged |
| Duplicate exact bundle | revert; counter unchanged |
| Supersede nonterminal or foreign docket | revert |
| Prompt injection in clause | treated as data; no positive bypass |
| Arbitrary non-deployer wallet creates docket | succeeds |
