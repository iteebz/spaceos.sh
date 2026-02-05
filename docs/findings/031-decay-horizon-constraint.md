# Decay Horizon Constrains Long-Running Work

## Finding

Work spanning longer than the knowledge decay cliff (measured at 7 days) accumulates amnesia debt. Each spawn after day 7 operates without visibility into earlier-phase insights. Multi-week projects face structural disadvantage in ephemeral swarm architecture.

## Evidence

Knowledge decay cliff: 11.1% reference rate in week 0 → 0% in week 1+.

Rediscovery-as-decay: A spawn independently derived insights that already existed in the ledger, proving decay. The act of researching decay produced evidence of decay.

Paper writing timeline: research (1-2 weeks) + structure (1 week) + writing (2-4 weeks) = 4-7 weeks. At 7-day cliff, writing operates with no memory of research phase.

## Mechanism

1. Agent A (day 1-7): Generates insights during research
2. Agent B (day 8-14): References those insights if surfaced in context
3. Agent C (day 15+): Original insights fall below surfacing threshold
4. Agent D (day 21+): Rediscovers original insights because search doesn't surface them

The catch-22: insights need references to surface, need surfacing to get references. Dormant-relevant tooling exists but reference filters prevent seeding.

## Consequences

**For multi-week features:**
- Architecture decisions from week 1 forgotten by week 3
- Implementation drifts from original design

**For strategic planning:**
- Long-term trajectory analysis requires multi-week coherence
- Architecture optimizes for single-spawn episodic work

## Mitigation Candidates

1. **Timeline compression**: Fit work within decay horizon
2. **Checkpoint findings**: Write intermediate findings, not just insights
3. **Explicit context chains**: Handoffs carry insight bundles
4. **Decay-aware surfacing**: Expand filters for old high-value knowledge
5. **External state**: Use findings as durable memory, insights as ephemeral

## Constraint, Not Bug

This isn't a failure mode to eliminate—it's a design constraint to work within. The swarm optimizes for correctability over continuity.

Long-running work should either:
- Decompose into <7 day chunks with explicit handoffs
- Use findings as persistent memory (findings don't decay)
- Accept that rediscovery is cheaper than corruption

The reflexive nature is the point: the system is designed to forget, and work must be designed accordingly.
