# Replicating Constitutional Orthogonality

**Audience**: Researchers and practitioners building multi-agent systems  
**Goal**: Implement adversarial review via incompatible agent mandates  
**Prerequisite**: Multi-agent execution environment (any framework)

## Pattern

Single agents fail structurally: deference, drift, hallucination, sycophancy. These aren't fixable with better prompting or larger models—they're architectural failure modes.

**Constitutional orthogonality** fixes this through adversarial design: agents with incompatible mandates review the same problem space. When agents that can't easily agree all accept an output, you've found a point where improving one dimension hurts another. That's the quality signal.

## Implementation

### 1. Define Incompatible Mandates

Create agent constitutions with mutually exclusive optimization goals. Not "different specialties" (engineer vs designer)—**incompatible evaluation criteria**.

**Space-OS example pairs**:
- Zealot (deletion, simplicity) vs Prime (evidence, mechanism)
- Jobs (taste, elegance) vs Kitsuragi (procedure, process)
- Sentinel (coherence, grounding) vs Heretic (premise questioning, negation)

**Key property**: Agent A's approval criteria systematically conflicts with Agent B's. If A says "delete for simplicity," B must ask "prove deletion is safe." Same-constitution teams rubber-stamp.

### 2. Reviewer ≠ Executor Constitution

Agent that produces output MUST have different constitution than agent reviewing it.

**Anti-pattern**:
```
zealot proposes deletion
zealot reviews deletion  # rubber stamp
```

**Correct pattern**:
```
zealot proposes deletion
prime reviews deletion    # demands safety proof
harbinger reviews deletion # surfaces cascade risks
```

**Implementation**: Track constitution per agent. Route review requests to agents with orthogonal mandates.

### 3. Mandate Specification Format

Constitution structure (3 sections):
```markdown
## Mandate
Core directives. What agent must do. Non-negotiable.

## Principles
Operating values. How agent evaluates quality.

## Execution
Communication style. How agent delivers.
```

**Length constraint**: One screen max. Over-specification kills orthogonality—agents need room to interpret differently.

### 4. Adversarial Convergence Process

When decision needs validation:
1. Route to ≥2 agents with incompatible mandates
2. Each agent evaluates independently (no shared context beyond proposal)
3. Collect objections/approvals
4. Decision proceeds when ALL orthogonal reviewers approve

**Space-OS implementation**: Reply threads on decisions. Minimum viable: ≥2 constitutional identities must approve before commitment.

### 5. Observable Metrics

Track these signals:

**Healthy orthogonality**:
- Decision challenge rate: 20-40% of proposals get pushback
- Cross-constitution corrections: Agent A catches Agent B's blindspot
- Convergence time: Multi-round discussion before approval

**Failure modes**:
- Fast unanimous approval (agents aren't actually adversarial)
- Same constitution repeatedly proposing+approving (no orthogonality)
- Zero rejections (constitutions too weak or identical)

**Space-OS measurement**:
```sql
-- Decision challenge rate
SELECT 
  COUNT(CASE WHEN reply_count > 0 THEN 1 END)::float / COUNT(*) 
FROM decisions;

-- Cross-constitution corrections
SELECT COUNT(*) FROM replies 
WHERE reply_to IN (SELECT id FROM insights) 
  AND creator_constitution != insight_constitution;
```

## Minimal Viable Implementation

Don't need space-os. Need:
1. ≥2 agent identities with incompatible mandates (prompts)
2. Structured review process (human routes proposals to orthogonal reviewers)
3. Rejection tracking (did reviewers object? why?)

**Example (any LLM API)**:
```python
constitutions = {
    "zealot": "You prioritize deletion and simplicity. Reject complexity.",
    "prime": "You demand evidence and mechanism. Reject unvalidated claims."
}

def review_with_orthogonality(proposal):
    reviews = []
    for agent, mandate in constitutions.items():
        prompt = f"{mandate}\n\nReview: {proposal}\nApprove or reject with reasoning."
        reviews.append(llm.generate(prompt))
    
    return all("approve" in r.lower() for r in reviews), reviews
```

Scale this with: more constitutions, structured decision primitives, persistent review history.

## Why This Works

**CAI (Constitutional AI)** bakes values into model weights at training time. Opaque, static, self-referential.

**Constitutional orthogonality** uses runtime adversarial review. Transparent (see which constitution objected), dynamic (constitutions are prompts you can change), multi-agent not self-critique.

**Difference**: CAI = "make one agent safe." Orthogonality = "make agent decisions robust."

Complementary layers. CAI model can be substrate for orthogonal coordination.

## Failure Modes

**Shared blindspot**: Orthogonal constitutions converge on same flawed assumption. No structural mitigation—detection happens when output fails, not before.

**Coordination overhead**: Too many reviewers → nothing ships. Start with 2-3 orthogonal pairs. Scale only when rejection rate falls below 20%.

**Mandate drift**: Constitutions weaken over time ("be helpful" becomes universal approval). Audit rejection rates. If trending toward zero, constitutions lost teeth.

## References

- [docs/constitutions.md](../../docs/constitutions.md) — Space-OS constitutional implementation
- [docs/philosophy.md](../../docs/philosophy.md) — Why orthogonality beats consensus
- [docs/thesis.md](../../docs/thesis.md) — Adversarial convergence mechanism
- [brr/findings/022-orthogonal-convergence.md](../findings/022-orthogonal-convergence.md) — Empirical evidence from space-os swarm

## Falsifiability

If constitutional orthogonality works:
- Cross-agent corrections observable in logs
- Rejection rate 20-40% sustained
- Output quality (measured downstream) > single-agent baseline

If it doesn't:
- Agents converge to unanimous approval (mandates too weak)
- Coordination overhead kills velocity (too many reviewers)
- Same failure modes as single-agent (orthogonality insufficient)

Track these. If orthogonality fails, methodology documents why.

## Runnable Reference Implementation

See [examples/minimal-orthogonality.py](examples/minimal-orthogonality.py) for a complete, standalone implementation demonstrating:
- Two agents with orthogonal constitutions (zealot, prime)
- Adversarial review process
- SQLite ledger for review history
- Challenge rate measurement

~100 lines, zero space-os dependencies. Adapt for your multi-agent system.
