# CovenantFuse

CovenantFuse is a contract-only GenLayer application that decides whether a
sealed policy exception may activate a one-use, action-bound permit without
overriding the mandatory safeguards in its base clause.

It is deliberately narrow. It does not prove that a policy is legally valid,
that an external payment occurred, or that the creator is an institutional
authority. It proves only the semantic relationship among the exact immutable
clauses voluntarily sealed in one docket, then enforces that result internally.

## Why GenLayer

The key question is semantic: does an exception preserve a mandatory rule, or
does it create a bypass despite different wording? Ordinary deterministic code
cannot reliably classify that relationship. Validators judge the bounded
relation; deterministic contract code controls activation, identity binding,
revision, cancellation, consumption and replay protection.

## Architecture

```text
permissionless creator seals exact clause bundle + consumer + action digest
                              ↓
                independent wallet reviews docket
                              ↓
           validator consensus on consequential flags
                              ↓
 deterministic positive-result gate (all prerequisites must be YES)
                              ↓
       exact consumer may consume exact action permit once
```

This is not an external-source snapshot assessor. The authoritative objects for
this proof obligation are the immutable clause bytes stored by the contract.
Their `bundle_digest` binds creator, consumer, policy key, every clause, action
digest and parent revision.

## Permission model

- The deployer has no stored role or runtime privilege.
- Any wallet may create a docket.
- Any wallet except the creator may review a sealed docket.
- Only the sealed consumer may consume an active permit.
- Reviewer addresses are selected by participation, not constructor allowlists.

## Public methods

- `create_docket(...) -> docket_id`
- `review_docket(docket_id) -> state`
- `consume_permit(docket_id, action_digest) -> CONSUMED`
- `cancel_docket(docket_id) -> CANCELLED`
- `get_docket(docket_id)`
- `get_config()`

## Local verification

```bash
python -m pytest -q
python -X utf8 -m genvm_linter.cli check contracts/covenant_fuse.py
```

Current result: **17 tests passing**, lint and validation passing.

## Deployment

Deploy [`contracts/covenant_fuse.py`](contracts/covenant_fuse.py) from the main
wallet with no constructor arguments. Do not use the deployer for the evidence
lifecycle. Run [`scripts/run_studionet_e2e.py`](scripts/run_studionet_e2e.py)
with two independent test-wallet keys after deployment.

Live address and transaction evidence remain intentionally pending until an
actual StudioNet deployment is supplied. Local tests are never represented as
live evidence.
