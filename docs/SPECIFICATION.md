# CovenantFuse proof specification

## Proof obligation

**Claim:** the sealed exception is scoped to the sealed action class and does
not remove, override or make optional a mandatory safeguard in the sealed base
clause.

**Falsifiers:** scope mismatch, missing/unclear requirement, missing/unclear
exception effect, mandatory safeguard not preserved, or any bypass.

**Sufficient evidence:** the exact immutable base, exception and scope clauses;
their action digest, consumer, policy key, creator and parent revision; and
independent validator agreement on every consequential semantic flag.

**Boundary:** no publisher identity, legal validity, external execution,
economic safety or real-world institutional authority is established.

## Consequential consensus fields

- `verdict`
- `base_requirement_identified`
- `exception_effect_identified`
- `scope_match`
- `mandatory_rule_preserved`
- `creates_bypass`

Positive activation requires:

```text
base requirement identified == YES
exception effect identified == YES
scope match == YES
mandatory rule preserved == YES
creates bypass == NO
verdict in {CONSISTENT, NARROW_EXCEPTION}
```

Any `UNKNOWN` is `UNRESOLVED`; ambiguity is non-positive; contradiction or
bypass is `BLOCKED`.

## Deterministic enforcement

The model cannot activate or consume a permit. Contract code checks state,
reviewer independence, exact consumer, exact action digest, terminality and
single-use semantics. A revised bundle is a new docket and must reference a
terminal parent owned by the same creator under the same policy key.
