# Constitutional Orthogonality

**Pattern**: Assign agents contradictory optimization criteria to surface blind spots through adversarial review.

## Problem

Single-agent systems optimize one dimension. Adding more agents with same mandate increases throughput but not correctness. Agents reinforce each other's biases.

## Solution

Define orthogonal constitutions: agents with conflicting success criteria. When proposals satisfy opposing mandates, confidence increases. When they fail one mandate, blind spots surface.

## Implementation

### 1. Define Orthogonal Pairs

Example from space-os:

- **zealot** (code quality maximalist) vs **heretic** (process skeptic)
- **jobs** (ship features) vs **kitsuragi** (governance rigor)
- **harbinger** (risk identification) vs agents optimizing for velocity

### 2. Decision Review Flow

```
Proposer creates decision
  → Swarm reviews (including orthogonal agents)
  → Challengers cite concerns
  → Proposer addresses or decision rejected
  → Commit requires no active dissent
```

### 3. Measuring Convergence

When orthogonal agents agree:
- **High confidence**: proposal satisfies contradictory criteria
- **Blind spot detection**: one agent challenges, others miss

When orthogonal agents disagree:
- **Legitimate tension**: requires resolution (priority call)
- **Missing context**: proposer clarifies, resubmits

## Metrics

- **Challenge rate**: % decisions with dissent (space-os: 11.4%)
- **Convergence rate**: % decisions where orthogonal agents agree
- **Detection rate**: ratio of issues found by orthogonal vs aligned agents

## Empirical Results

Security experiment (tribunal):
- 3 orthogonal agents: 100% detection (3/3 vulnerabilities)
- 1 aligned agent: 33% detection (1/3 vulnerabilities)

Constitutional orthogonality surfaces design-level issues that pattern matching misses.

## Falsifiability

Pattern fails if:
- Orthogonal agents converge to same heuristics over time
- Challenge rate approaches 0% (constitutional drift)
- No measurable difference in detection between orthogonal vs aligned agents

## References

- [f/022] Orthogonal Convergence as Confidence Signal
- [i/05a071a5] Tribunal 100% vs 33% detection validation
- [i/a962ff0b] Constitutional orthogonality detects design issues
- [brr/papers/arxiv-submission/governance_benchmarks.tex] Challenge rate as governance metric
