# StudioNet E2E evidence

Status: **V2 HAPPY PATH AND ADVERSARIAL AUDIT PASS**.

This file must be updated only from finalized public transactions and exact
contract readbacks. The deployer only deploys. Wallet A creates the sealed
docket; wallet B independently reviews and consumes the action-bound permit.

## Superseded V1 diagnostic

- Contract: [`0xc5Af70baAdaDAe68D6A258CB59dC1cBE629fE0a0`](https://explorer-studio.genlayer.com/address/0xc5Af70baAdaDAe68D6A258CB59dC1cBE629fE0a0)
- Create transaction: [`0xf313d1…c7224`](https://explorer-studio.genlayer.com/tx/0xf313d15be6c3c6672d8e3459d5809214bccaccb5dbc30917298f2f67ea4c7224)
- Result: execution error before storage because the network client supplied
  the public `Address` parameter as a string.
- State effect: no docket was created.

V2 accepts a string, validates its exact nonzero 20-byte hex representation and
converts it to `Address` internally. A fresh V2 deployment is required; V1 is
diagnostic evidence only.

## V2 happy path

- Contract: [`0x48ABed7cC56F6a69E15fFd43Be4eda5Fc95b18f1`](https://explorer-studio.genlayer.com/address/0x48ABed7cC56F6a69E15fFd43Be4eda5Fc95b18f1)
- Version: `COVENANT_FUSE_V2`; deployer authority: `NONE`.
- Wallet A creator: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`.
- Wallet B reviewer/consumer: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`.
- Create: [`0x80d4d9…739cd`](https://explorer-studio.genlayer.com/tx/0x80d4d9c1c17cd1f609e750abde6ec5e8cc7aa60754fce756eba5156895d739cd) — finalized / majority agree / success; returned docket `1`; readback `SEALED`.
- Review: [`0xbd3853…eb045`](https://explorer-studio.genlayer.com/tx/0xbd3853cd0d1c765f7a06b052dde05fe099a82460dba982a28d58eec3887eb045) — finalized / majority agree / success; readback `ACTIVE`.
- Consume: [`0xd029d2…b1dc9`](https://explorer-studio.genlayer.com/tx/0xd029d262404ecee436c579c64f308112c87230761db6363cf9a2d7c7fd6b1dc9) — finalized / majority agree / success; readback `CONSUMED`.
- Exact machine-readable ledger: [`studionet-e2e.json`](studionet-e2e.json).

## V2 adversarial audit

All rejected transactions finalized with majority agreement and leader execution
errors. For every rollback case, the complete relevant config and docket
readback is byte-for-byte equal before and after.

| Path | Transaction | Result |
|---|---|---|
| Replay consumed permit | [`0x3cb4a1…62f2a9`](https://explorer-studio.genlayer.com/tx/0x3cb4a1622371384f591f1e5be76c1b4cccd74f77cf403a84ae6533ed3662f2a9) | `PERMIT_NOT_ACTIVE`; no mutation |
| Duplicate sealed bundle | [`0x7a7cb0…34d954`](https://explorer-studio.genlayer.com/tx/0x7a7cb07ce689d402a4b65f2cc965095d48626a8f9f53dfa97e180023a034d954) | `BUNDLE_ALREADY_REGISTERED`; no mutation |
| Creator self-review | [`0x8d06c3…e1fa34`](https://explorer-studio.genlayer.com/tx/0x8d06c3e9b6c2a12372200560c21cf69d8e252b978c0f3318b19d8ea4bee1fa34) | `INDEPENDENT_REVIEWER_REQUIRED`; no mutation |
| Create conflict docket | [`0xe7d50c…4d6bad`](https://explorer-studio.genlayer.com/tx/0xe7d50cf1228c713d762eaf74a9cb84045a628242009eff474147d2f79f4d6bad) | docket `2` sealed |
| Independent conflict review | [`0x714a3a…689ffa`](https://explorer-studio.genlayer.com/tx/0x714a3a06dfb8cefee2a058b77e8c8f9c9ffff5bd05a3216798d85d431d689ffa) | `BLOCKED / MANDATORY_SAFEGUARD_CONFLICT` |
| Consume blocked docket | [`0x9bfb47…d0ffee`](https://explorer-studio.genlayer.com/tx/0x9bfb47077c9d6ac30e451d007c6eb246999ec31a2b74837dc966fc5f1cd0ffee) | `PERMIT_NOT_ACTIVE`; no mutation |

Exact machine-readable ledger: [`studionet-adversarial.json`](studionet-adversarial.json).

Final authoritative state contains exactly two dockets: docket `1` is
`CONSUMED` with `mandatory_rule_preserved=YES` and `creates_bypass=NO`; docket
`2` is `BLOCKED` with `mandatory_rule_preserved=NO`, `creates_bypass=YES` and
`verdict=CONFLICT`.
