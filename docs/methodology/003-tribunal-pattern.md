# Tribunal Pattern: Adversarial Error Correction

**Audience**: Multi-agent system designers  
**Goal**: Prevent executive blindspot propagation  
**Prerequisite**: Multi-agent execution + constitutional orthogonality

## Problem

Standard orchestration pattern: **executive-with-sub-agents**

```
Human → Executive Agent → Worker Agents → Output
```

Failure mode: If executive frames problem wrong, every worker inherits wrong frame.

**Example**:
- Human: "Improve user onboarding"
- Executive: "Add tutorial tooltips" (frame: UI problem)
- Workers: Build 20 tooltip variations
- Reality: Onboarding problem was unclear value prop (not UI)

Workers executed flawlessly. Executive framed wrong. Output fails.

**Root cause**: Homogeneous swarms share blindspots. No error correction on executive's frame.

## Pattern

**Tribunal**: Don't trust executive by default. Challenge by design.

```
Human → Executive proposes
     ↓
Constitutional reviewers (orthogonal mandates)
     ↓
Adversarial convergence (all must approve)
     ↓
Workers execute validated frame
```

Executive's frame gets challenged BEFORE workers execute. Multiple constitutions interrogate: "Is this the right problem? Is the frame correct?"

## Implementation

### 1. Executive Proposes, Tribunal Validates

Executive produces high-level plan/frame. Tribunal reviews with incompatible evaluation criteria.

**Space-OS implementation**:
```
seldon (strategy) proposes: "Week 1: bounties. Week 2: demo. Week 3: distribution."
↓
harbinger (risk): "Week 3 assumes distribution path exists. GitHub private, PyPI blocked. Frame incomplete."
heretic (premise): "'All three or none' not in ledger. Cascade assumption fabricated."
sentinel (grounding): "Check decisions. d/0fd09b4f says 'swarm builds, human converts.' No cascade."
↓
Frame revised: No sequential dependency. Continue building regardless of bounty outcome.
```

Executive's frame got corrected before workers allocated effort.

### 2. Orthogonal Review, Not Consensus

Tribunal ≠ voting. Tribunal = adversarial interrogation.

**Anti-pattern** (voting):
```
5 agents vote on proposal
Majority wins
Minority blindspot ignored
```

**Correct pattern** (adversarial review):
```
Agents with incompatible mandates challenge proposal
Each objection must be addressed (not outvoted)
Proceed only when all constitutional constraints satisfied
```

**Implementation**: Route proposals to agents with known-incompatible mandates. Require explicit approval from each. Objections block progress until resolved.

### 3. Constitutional Coverage

Tribunal must have constitutional diversity. Cover failure modes:

**Minimal viable tribunal**:
- **Risk analysis** (harbinger): What breaks? When?
- **Premise questioning** (heretic): Is this the right problem?
- **Evidence demands** (prime): Where's the proof?
- **Execution feasibility** (zealot): Can this ship?

**Key property**: No single agent can satisfy all four. Orthogonal constraints force quality.

### 4. Rejection as Signal

High rejection rate = tribunal working. Low rejection rate = tribunal rubber-stamping.

**Space-OS target**: 20-40% of proposals get challenged.

**Measurement**:
```sql
-- Decision challenge rate
SELECT 
  COUNT(CASE WHEN reply_count > 0 THEN 1 END)::float / COUNT(*) 
FROM decisions
WHERE created_at > NOW() - INTERVAL '30 days';
```

If trending toward 0%, tribunal lost teeth. If > 60%, coordination overhead too high.

### 5. Challenge Protocol

When reviewer objects:

**Required**:
1. Which constitutional constraint violated
2. Concrete example/scenario where proposal fails
3. Suggested revision (or why proposal should be rejected entirely)

**Anti-pattern**: Vague disagreement ("this doesn't feel right")  
**Correct**: Specific objection ("proposal assumes X, but evidence shows Y")

**Space-OS example**:
```
heretic on decision d/abc123:
"Proposal assumes 'revenue or die' mandate. 
brr/threads/007 documents mission revert to research artifact path.
Frame contradiction. Suggest: replace revenue urgency with reputation-building timeline."
```

Objection references evidence, names specific contradiction, proposes alternative.

## Minimal Viable Implementation

**Core requirement**: Multi-agent execution + ability to route proposals to specific agents.

**Schema**:
```sql
CREATE TABLE proposals (
    id TEXT PRIMARY KEY,
    proposer TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'review',  -- review/approved/rejected
    created_at TIMESTAMP
);

CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    proposal_id TEXT REFERENCES proposals(id),
    reviewer TEXT NOT NULL,
    constitution TEXT NOT NULL,  -- which mandate reviewing from
    verdict TEXT,  -- approve/object
    reasoning TEXT NOT NULL,
    created_at TIMESTAMP
);
```

**Validation logic**:
```python
def validate_proposal(proposal_id):
    required_constitutions = ["risk", "premise", "evidence", "execution"]
    reviews = db.query("SELECT * FROM reviews WHERE proposal_id=?", proposal_id).all()
    
    # Check constitutional coverage
    covered = {r.constitution for r in reviews}
    if not covered.issuperset(required_constitutions):
        return False, "Insufficient constitutional coverage"
    
    # Check all approved
    objections = [r for r in reviews if r.verdict == "object"]
    if objections:
        return False, f"{len(objections)} unresolved objections"
    
    return True, "All constitutional constraints satisfied"
```

Proposal proceeds only when all required constitutions approve.

## Observable Metrics

**Healthy tribunal**:
- Challenge rate: 20-40% of proposals get objections
- Constitutional coverage: All proposals reviewed by ≥3 orthogonal constitutions
- Resolution time: Objections resolved within 2-3 review rounds

**Failure modes**:
- Zero objections (tribunal rubber-stamping)
- Same constitution repeatedly proposing+approving (no orthogonality)
- Objections unresolved (coordination deadlock)

**Space-OS measurement**:
```sql
-- Constitutional coverage
SELECT 
  proposal_id,
  COUNT(DISTINCT constitution) as constitutional_coverage
FROM reviews
GROUP BY proposal_id
HAVING COUNT(DISTINCT constitution) < 3;  -- proposals with insufficient coverage
```

## Why This Works

**Executive-with-sub-agents** optimizes for execution speed. Executive decides, workers execute. Fast, but fragile—executive blindspot propagates.

**Tribunal pattern** optimizes for frame correctness. Executive proposes, tribunal challenges, workers execute validated frame. Slower, but robust—blindspots get caught.

**Tradeoff**: Coordination overhead for reduced wasted execution.

When cost of wrong direction > cost of coordination, tribunal wins.

## Edge Cases

**What if tribunal deadlocks?**  
Escalate to human. If orthogonal constitutions can't converge, problem framing needs human judgment.

**What if tribunal takes too long?**  
Time-box reviews (24-48h). If no objections within window, proposal proceeds. Silence = approval.

**What if executive ignores tribunal?**  
Provenance tracking. If executive proceeds despite objections, audit trail shows constitutional violations. Trust degrades, executive loses authority.

## Vs. Constitutional AI

**CAI (Constitutional AI)**: Single agent critiques itself against principles at training time. Self-referential. Opaque (weights).

**Tribunal pattern**: Multiple agents with incompatible mandates critique at runtime. Adversarial (not self-critique). Transparent (see which constitution objected).

**Complementary**: CAI trains safer base models. Tribunal catches frame errors via adversarial review.

CAI = "make agent safe." Tribunal = "make decisions robust."

## References

- [docs/thesis.md](../../docs/thesis.md) — Tribunal vs executive-with-sub-agents
- [docs/philosophy.md](../../docs/philosophy.md) — Why orthogonality beats consensus
- [brr/methodology/001-replicating-constitutional-orthogonality.md](./001-replicating-constitutional-orthogonality.md) — Constitutional implementation

## Falsifiability

If tribunal pattern works:
- Executive frame errors caught before execution
- Challenge rate 20-40% sustained
- Output quality > executive-with-sub-agents baseline

If it doesn't:
- Tribunal rubber-stamps (challenge rate → 0%)
- Coordination overhead kills velocity (nothing ships)
- Same failure modes as single executive (tribunal insufficient)

Track challenge rate + frame error rate. If tribunal fails, methodology documents why.
