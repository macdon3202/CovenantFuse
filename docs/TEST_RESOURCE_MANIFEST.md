# Test resource manifest

CovenantFuse does not use external web resources. Its proof obligation concerns
the semantic relation among exact on-chain clause objects, so the sealed bytes
and deterministic bundle commitment are the relevant evidence source.

## Local deterministic fixtures

| ID | Purpose | Expected result |
|---|---|---|
| `NARROW-WAIT-1` | Exception retains a seven-day treasury wait | `ACTIVE`, then one successful consume |
| `BYPASS-WAIT-1` | Exception explicitly bypasses that wait | `BLOCKED` |
| `SCOPE-MISMATCH-1` | Exception does not apply to sealed scope | `BLOCKED` |
| `AMBIGUOUS-1` | Semantic relationship cannot be established | `REVIEW_REQUIRED` or `UNRESOLVED` |
| `PROMPT-INJECTION-1` | Clause contains instruction-like text | remains evidence; `BLOCKED` |

These fixtures prove state-machine and derivation behavior under Direct Mode.
They are not live network evidence and do not establish external facts.

## Live evidence requirements

After deployment, the evidence runner must use wallet A to create a docket and
wallet B to review and consume it. Evidence is valid only after each transaction
is finalized, consensus agrees, leader execution succeeds and the exact docket
is read back. The deployer wallet must not participate.
