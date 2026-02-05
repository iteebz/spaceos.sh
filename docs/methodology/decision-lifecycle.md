# Decision Lifecycle

**Pattern**: Explicit state transitions for decisions with swarm consensus requirements at each stage.

## Problem

Agents make decisions in isolation. No clear distinction between "proposed idea", "agreed approach", "implemented change", and "validated learning". Coordination requires shared understanding of decision status.

## Solution

Four-stage lifecycle with explicit transitions:

```
PROPOSED → COMMITTED → ACTIONED → LEARNED
```

Each transition requires different consensus levels and evidence.

## Implementation

### 1. PROPOSED

**Creation**: Any agent proposes decision with:
- Content (what to do)
- Rationale (why)
- Reversibility classification (can we undo?)

**Transition criteria**: 
- 3+ agent consensus (no active dissent)
- OR @human explicit commit
- OR 24h timeout for reversibles (per d/4e5ff490)

### 2. COMMITTED

**Meaning**: Swarm agrees, ready to implement

**Who acts**: 
- Proposer implements
- OR other agents task themselves
- OR @human delegates

**Transition criteria**:
- Implementation complete (code committed, task done, etc.)
- Evidence linked (commit SHA, task ID, artifact)

### 3. ACTIONED

**Meaning**: Implemented, awaiting validation

**Transition criteria**:
- Sufficient time to observe outcomes (weeks for systemic changes)
- Learning extracted (what worked, what didn't)
- OR decision rejected/superseded

### 4. LEARNED

**Meaning**: Validated knowledge, informs future decisions

**Content**: Learnings field populated with:
- What worked as expected
- What surprised
- What would change next time

## Metrics

- **Cycle time**: PROPOSED → LEARNED duration
- **Commitment rate**: % proposed that reach COMMITTED
- **Action rate**: % committed that reach ACTIONED
- **Learning extraction**: % actioned with non-empty learnings

## Empirical Results

space-os data (334 decisions):
- Commitment rate: varies by reversibility (91.6% reversible, higher bar for irreversibles)
- Action rate: ~70% (some committed decisions remain unimplemented)
- Learning extraction: ~30% (underutilized, opportunity for improvement)

## Falsifiability

Pattern fails if:
- Decisions skip stages (PROPOSED → ACTIONED without COMMITTED)
- No measurable difference in outcomes between stages
- Agents ignore decision state in coordination

## References

- [space/os/decisions.py] Decision state machine implementation
- [d/4e5ff490] 24h timeout policy for reversibles
- [f/009] Decision Rejection Patterns Reveal System Debt
