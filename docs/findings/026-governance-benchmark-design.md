# Governance Benchmark Design

## Finding

CTDE benchmarks measure task success rate. Governance benchmarks should measure error correction, decision quality, and knowledge persistence. Design: 6 metrics across 3 categories (correction, commitment, continuity).

## Rationale

f/024 identified the measurement gap: "Papers measure task success rate. space-os should measure error-catch rate, decision reversal rate, insight reference frequency."

f/025 showed ephemeral agents fail between spawns, not within. Benchmarks must capture inter-spawn coordination quality.

## Proposed Metrics

### Category 1: Correction (adversarial oversight working)

**1. Cross-agent error catch rate**
- Definition: Agent A's commit broken by Agent B's fix within 24h
- Numerator: fix commits referencing other agent's prior commit
- Denominator: total fix commits
- Target: Higher = more catching. But high absolute = poor code quality.
- Signal: Constitutional orthogonality producing correction

**2. Decision challenge rate**
- Definition: Decisions receiving dissenting replies before commit
- Numerator: proposed decisions with disagreement replies
- Denominator: total proposed decisions
- Target: 10-30% (healthy debate without gridlock)
- Signal: Agents aren't rubber-stamping

### Category 2: Commitment (decisions binding)

**3. Decision half-life**
- Definition: Median time from committed → actioned
- Signal: Decisions becoming action, not accumulating
- Anti-pattern: Long backlog of stale committed decisions

**4. Decision reversal rate**
- Definition: Committed decisions later rejected
- Numerator: decisions with both committed_at AND rejected_at
- Denominator: total committed decisions
- Target: <5% (commitment should be stable)
- Signal: Premature commitment if high

### Category 3: Continuity (ledger as memory)

**5. Insight reference rate**
Already implemented as `compounding()`. Track weekly.

**6. Knowledge decay curve**
- Definition: Insight reference frequency vs age
- Method: Bucket insights by age (weeks), measure reference rate per bucket
- Signal: Steep decay = swarm forgetting. Flat = knowledge persisting.
- Anti-pattern: Only recent insights referenced

## Implementation Sketch

```python
def cross_agent_corrections(days: int = 7) -> dict:
    """Track when agent fixes another agent's work."""
    # Parse git log for fix commits
    # Match fix domain to prior commits by different author
    # Return {corrections: N, total_fixes: M, rate: N/M}

def decision_challenge_rate() -> dict:
    """Measure healthy disagreement on proposals."""
    # For each decision, check replies for disagreement signals
    # Keywords: "disagree", "alternative", "concern", "but"
    # Return {challenged: N, total: M, rate: N/M}

def decision_half_life() -> dict:
    """Median time from committed to actioned."""
    # SELECT committed_at, actioned_at FROM decisions
    # WHERE both non-null
    # Return median delta

def decision_reversal_rate() -> dict:
    """Committed decisions later rejected."""
    # Already have committed_at, rejected_at columns
    # Count where both non-null

def knowledge_decay() -> dict:
    """Reference rate by insight age."""
    # Bucket insights by created_at week
    # For each bucket, count references
    # Return {week_0: rate, week_1: rate, ...}
```

## Comparison to CTDE Benchmarks

| CTDE Metric | Governance Equivalent | Why Different |
|-------------|----------------------|---------------|
| Task success rate | N/A | No single objective |
| Communication efficiency | Insight reference rate | Information flow, not bandwidth |
| Coordination overhead | Decision half-life | Time-to-action, not token cost |
| Agent utilization | Silent agent rate | Activity, not throughput |
| Reward distribution | Decision influence | Who shapes outcomes |

## Limitations

- No external baseline (space-os is n=1)
- Some metrics gameable (agents can artificially challenge)
- "Healthy" ranges are guesses until data accumulates
- Doesn't measure task quality (intentionally—different problem)

## Next Steps

1. Implement decision_reversal_rate (simplest, data exists)
2. Implement knowledge_decay (most novel signal)
3. Baseline current swarm state
4. Track weekly for trend detection

## References

- [f/024] space-os vs. 2025 Multi-Agent Literature
- [f/025] MAST Failure Taxonomy vs Ephemeral Agent Architectures
- [f/020] Swarm Failure Modes Cluster into Four Patterns
- [i/b28970bf] CTDE vs ledger governance distinction
