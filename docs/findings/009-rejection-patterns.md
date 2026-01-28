# Decision Rejection Patterns Reveal System Debt

## Finding

57% of decision rejections (24/42) stem from a single primitive removal (channels). Rejections cluster around technical debt, not poor judgment.

## Evidence

Rejection categorization (n=42 rejected decisions, n=41 with documented reasons):
- obsolete_primitive: 24 (57%)
- superseded: 7 (17%)
- test_artifact: 4 (10%)
- other: 4 (10%)
- over_engineering: 2 (5%)

The "obsolete_primitive" category is almost entirely decisions referencing the removed `channels` primitive:
- "Channels bookmark to spawns"
- "Tasks decouple from channels"
- "Enforce purpose on channel creation"
- "channel delete soft-deletes"

## Mechanism

When channels were removed from the codebase, decisions referencing channels became invalid. They weren't wrong when made—they became wrong retroactively.

This creates a cascade:
1. Primitive added (channels)
2. Decisions made assuming primitive exists
3. Primitive removed
4. Decisions orphaned
5. Bulk rejection to clean up

The rejection reasons document *why* decisions failed, not *what* agents did wrong.

## Implications

1. Primitive removal is expensive: creates orphaned decisions requiring cleanup
2. High rejection rate doesn't indicate poor decision-making—it can indicate architectural churn
3. "Superseded" (17%) is healthy: decisions can be replaced by better ones
4. "Over-engineering" (5%) is the only category reflecting actual judgment problems
5. Decision validity depends on system state, not just reasoning

## Limitations

- Single codebase observation
- Channels removal was exceptional (complete primitive deletion)
- Rejection reason categorization is heuristic (keyword matching)

## References

- [d/42adb331] - replies replace channels as coordination primitive
- [i/44317df0] - zealot rejection pattern observation
- Rejection reasons extracted from reply threads
