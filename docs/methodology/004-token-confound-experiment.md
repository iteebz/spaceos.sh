# Token Confound Experiment: Isolating Architectural Effects in Constitutional Orthogonality

## Problem

Constitutional orthogonality uses multiple agents with incompatible objectives, producing higher quality outputs than single agents. But orthogonal systems consume more tokens (3 agents × 3 iterations = 9 agent-turns vs 1 agent × 1 turn).

**Confound**: Quality improvements could reflect increased compute budget, not architectural benefits.

**Experiment**: Test whether orthogonality produces quality gains under token-matched conditions.

## Hypotheses

**H1 (architectural benefit)**: Orthogonal agents outperform cooperative agents and single agents when token budgets are equal.

**H2 (compute scaling)**: Quality scales with total tokens regardless of architecture—single agent with 9× tokens matches orthogonal system.

**H3 (diminishing returns)**: Single agent quality saturates before reaching orthogonal system's token budget.

## Experimental Design

### Conditions (Token-Matched)

All conditions use identical token budget T (e.g., 30k tokens):

1. **Single agent baseline**
   - 1 agent, 1 turn
   - T tokens total

2. **Cooperative multi-agent**
   - 3 agents, same objective ("produce high-quality output")
   - Sequential iteration (agent A → agent B → agent C → repeat until convergence)
   - T tokens total

3. **Orthogonal multi-agent**
   - 3 agents, incompatible objectives (precision, procedure, strategy)
   - Sequential iteration until convergence
   - T tokens total

### Controls

- **Model**: Identical weights across all conditions (e.g., Claude 3.7 Sonnet)
- **Task**: Fixed task set (legal reasoning, code generation, strategic planning)
- **Stopping criterion**: Token budget exhausted OR convergence detected (no agent proposes changes)
- **Randomization**: Task order randomized, agent order randomized within multi-agent conditions

### Metrics

**Quality (primary)**:
- Human evaluation: correctness, completeness, clarity (blind evaluation)
- Error detection rate: inject known errors, measure catch rate
- External validation: task-specific ground truth where available (code: passes tests, legal: matches precedent)

**Process (secondary)**:
- Convergence speed: iterations until no changes proposed
- Error surface coverage: which error types caught (factual, procedural, strategic)
- Agreement dynamics: frequency of objections, revision depth

### Task Selection

Use tasks with objective quality criteria:

1. **Legal reasoning**: Contract clause analysis against statutory requirements (ground truth: expert review)
2. **Code generation**: Implement specified API (ground truth: test suite passage, no security vulnerabilities)
3. **Strategic planning**: Resource allocation under constraints (ground truth: mathematical optimality)

N=30 tasks per domain (90 total), balanced for difficulty.

## Expected Outcomes

**If H1 (architectural benefit)**:
- Orthogonal > Cooperative > Single, token-matched
- Error detection rate higher for orthogonal
- Different error types caught by different constitutions

**If H2 (compute scaling)**:
- Quality ∝ tokens across architectures
- No architectural effect

**If H3 (diminishing returns)**:
- Single agent quality plateaus
- Orthogonal agents utilize tokens more efficiently

## Token Budget Determination

Pilot study to determine T:

1. Run single agent on 5 tasks with increasing budgets (5k, 10k, 20k, 40k tokens)
2. Measure quality saturation point
3. Set T = saturation point for single agent
4. Hypothesis: Orthogonal system achieves higher quality at this budget

## Implementation Notes

**Token tracking**:
- Count prompt + completion tokens per agent turn
- Stop condition: cumulative tokens ≥ T
- Allow final turn to exceed T to enable convergence (report actual token usage)

**Convergence detection**:
- Agent explicitly states "no changes" OR returns draft unchanged
- All agents must converge for stopping

**Constitutional specifications** (orthogonal condition):
- **Precision agent**: Rejects unsupported claims, requires evidence citations, flags uncertainty
- **Procedure agent**: Enforces format requirements, scope boundaries, procedural compliance
- **Strategy agent**: Maximizes impact, identifies opportunities, challenges conservative framing

**Cooperative specification**:
- All agents share objective: "Produce the highest quality output possible"

## Analysis Plan

**Primary comparison**: Quality scores across 3 conditions (one-way ANOVA, post-hoc pairwise)

**Token efficiency**: Quality per 1k tokens consumed

**Error analysis**: Categorize caught vs missed errors by type, condition

**Failure mode frequency**: Constitutional drift, evidence fabrication, agreement theater rates across conditions

## Limitations

1. **Single model family**: Results may not generalize across model architectures
2. **Task domain dependence**: Some domains may benefit more from orthogonality than others
3. **Human evaluation bias**: Evaluators may infer architecture from output characteristics
4. **Token counting variability**: Different APIs measure tokens differently
5. **Convergence ambiguity**: Stopping criteria affects token budget utilization

## Falsifiability

**Evidence that would refute H1**:
- Orthogonal agents perform no better than cooperative agents or single agents under token matching
- Error detection rate equivalent across conditions
- Quality gains disappear when token-matched

**Evidence that would support H1**:
- Orthogonal > Cooperative > Single (p < 0.05, effect size d > 0.5)
- Orthogonal agents catch error categories missed by single/cooperative agents
- Quality gains persist under token matching

## Future Extensions

1. **Token allocation strategies**: Equal per agent vs weighted by constitutional role
2. **Constitution diversity**: Test N=2, N=4, N=5 orthogonal agents
3. **Model heterogeneity**: Mix model families (Claude, GPT-4, Gemini) within orthogonal system
4. **Adversarial validation**: Inject adversarial inputs designed to exploit single-agent blindspots

## References

- Constitutional orthogonality paper: brr/papers/constitutional-orthogonality-arxiv.md
- Methodology: brr/methodology/001-replicating-constitutional-orthogonality.md
- Stateless swarm comparison: brr/papers/stateless-agents-stateful-swarm-arxiv.md (CTDE architectural parallel)

## Status

**Phase**: Methodology design (not yet executed)

**Blocker**: Requires compute budget for 90 tasks × 3 conditions = 270 experimental runs

**Next step**: Pilot study (N=5 tasks) to validate token budget determination and identify implementation issues
