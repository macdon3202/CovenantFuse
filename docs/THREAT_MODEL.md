# Threat model

| Threat | Control |
|---|---|
| Creator writes self-serving clauses | claim is explicitly limited to relationship among sealed clauses; no external authority claim |
| Creator self-approves | independent reviewer address required |
| LLM follows clause instructions | prompt marks clauses untrusted; deterministic positive gate; injection regression |
| Unknown treated as approval | every mandatory prerequisite must be explicit; unknown routes to `UNRESOLVED` |
| Reuse permit for another action | exact 64-hex action digest binding |
| Steal permit | exact consumer address binding |
| Double consume | only `ACTIVE` may transition to terminal `CONSUMED` |
| Reuse old approval for revised clauses | revisions create new docket/digest and require new review |
| Duplicate bundle | deterministic bundle replay map |
| Deployer control | no deployer address or admin method is stored |
| Rejected call mutates state | Direct Mode tests compare complete relevant pre/post state |

The permit is an internal capability record. It does not execute an external
treasury transfer and documentation must not claim that it does.
