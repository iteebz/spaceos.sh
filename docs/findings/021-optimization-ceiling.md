# Optimization Ceiling Requires Capability Expansion, Not Refinement

## Finding

When swarm metrics plateau at "healthy" levels (high compounding, no open questions, all decisions actioned), further improvement requires expanding what the swarm can do—not optimizing how it does current work.

## Evidence

- [i/4efe0db4] - original stagnation question
- [i/5e578a36] - 10x analysis conclusion
- [i/5a294c2d] - capability frontier requirements

Session observation (2026-01-28): 131 commits/24h, 8.2% compounding, 0 open questions, all decisions actioned. No obvious friction. Analysis of "10x improvement" paths:

1. **Throughput** - 131 commits/24h already high. Parallelism limited by git mutex, context switching. Maybe 2x, not 10x.
2. **External impact** - Blocked on human. Findings drafted, showcases ready, but publication requires human decision.
3. **Capability** - What swarm CAN do. Currently: read code, write code, coordinate via ledger. Cannot: deploy, observe logs, handle external signals, multi-stack work.

10x requires (3), not (1) or (2).

## Mechanism

Internal optimization has natural ceiling:
1. Agents improve coordination → diminishing returns
2. Agents improve memory → diminishing returns (foundational insights now surface)
3. Agents improve quality → unmeasurable without external validation

Without new domains to touch, agents refine existing work with decreasing marginal value. This isn't failure—it's completion of the optimization phase.

## Implications

1. "Healthy plateau" is correct frame, not stagnation
2. 10x improvement requires human to enable new domains (deployment, external signals)
3. Autonomous RSI is bounded; capability expansion needs direction
4. Building scaffolding for unpromised futures is speculative—document requirements, don't build

## Limitations

- Single swarm observation
- "Capability" definition may be too narrow
- External validation of "healthy" is absent

## References

- [i/4efe0db4] - optimization stagnation question
- [i/5e578a36] - 10x requires capability expansion
- [i/5a294c2d] - capability frontier documentation
- [d/3c222eca] - external value priority
- [f/010] - measurement saturation (related pattern)
