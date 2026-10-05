# StudioNet E2E evidence

Status: **PENDING DEPLOYMENT**.

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
