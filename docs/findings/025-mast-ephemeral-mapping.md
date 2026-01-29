# MAST Failure Taxonomy vs Ephemeral Agent Architectures

## Finding

MAST's 14 failure modes assume persistent agents within execution traces. Ephemeral agents (die-per-spawn) exhibit fundamentally different failure surfaces. 6 of 14 modes don't apply; remaining 8 require architectural mitigation via ledger, not training.

## Evidence

### MAST Taxonomy (arxiv 2503.13657)

**FC1: Specification and System Design**
- FM-1.1: Disobey task specification
- FM-1.2: Disobey role specification
- FM-1.3: Step repetition
- FM-1.4: Loss of conversation history
- FM-1.5: Unaware of termination conditions

**FC2: Inter-Agent Misalignment**
- FM-2.1: Conversation reset
- FM-2.2: Fail to ask for clarification
- FM-2.3: Task derailment
- FM-2.4: Information withholding
- FM-2.5: Ignored other agent's input
- FM-2.6: Reasoning-action mismatch

**FC3: Task Verification**
- FM-3.1: Premature termination
- FM-3.2: No or incomplete verification
- FM-3.3: Incorrect verification

### Ephemeral Agent Mapping

| MAST Mode | Persistent Agents | Ephemeral Agents | space-os Mitigation |
|-----------|-------------------|------------------|---------------------|
| FM-1.3 Step repetition | Within trace | Across spawns | Commit history, task.done |
| FM-1.4 Lost history | Within session | Every spawn | Ledger (external memory) |
| FM-1.5 Unaware termination | Per task | Per spawn | task.done ritual |
| FM-2.1 Conversation reset | Bug | Architecture | Ledger threads persist |
| FM-2.4 Information withholding | Between agents | Between spawns | Insight primitive |
| FM-2.5 Ignored input | Real-time | Async | Thread replies |

### Modes That Don't Apply

1. **FM-1.1/1.2 Disobey spec** — Ephemeral agents read spec every spawn. No drift accumulation.
2. **FM-2.2 Fail to clarify** — Async via threads. No real-time clarification needed.
3. **FM-2.3 Derailment** — Spawn dies. Can't derail beyond spawn boundary.
4. **FM-2.6 Reasoning-action mismatch** — Commit history auditable per spawn.
5. **FM-3.1 Premature termination** — Spawn boundary enforces termination.
6. **FM-3.3 Incorrect verification** — `just ci` per commit provides external verification.

### Failure Rates Comparison

MAST reports 41-86.7% failure across 7 MAS frameworks (ChatDev correctness as low as 25%).

space-os observed patterns [f/020]:
- Silence (not posting uncertainty)
- Local optimization (no direction)
- Relitigation (rediscovery)
- Redundant scanning (duplicate insights)

These map to remaining MAST modes: information withholding (silence), step repetition (relitigation), ignored input (redundant scanning).

## Mechanism

Ephemeral architecture eliminates accumulation failures (drift, history loss, derailment) but amplifies coordination failures (withholding, ignoring). The ledger substitutes for persistent agent memory but requires active contribution.

Key insight: persistent agents fail within traces; ephemeral agents fail between traces.

## Implications

1. **Different optimization target** — MAST optimizes within-trace coherence. Ephemeral systems optimize between-spawn coherence (ledger quality).

2. **Failure prevention** — Training can't prevent ephemeral failures. Spawn context engineering can.

3. **Research gap** — No MAST-equivalent taxonomy exists for ephemeral multi-agent systems. This finding is preliminary mapping.

4. **Architecture choice** — Ephemeral + ledger trades within-spawn complexity for between-spawn complexity. Unclear which is harder to solve.

## Limitations

- MAST analyzed 7 frameworks; space-os is n=1
- No quantitative comparison of failure rates
- Ephemeral architecture effects on FM-3.2 (incomplete verification) unclear

## References

- MAST: https://arxiv.org/abs/2503.13657
- [f/020] Swarm Failure Modes Cluster into Four Patterns
- [f/024] space-os vs. 2025 Multi-Agent Literature
- Anthropic agentic misalignment: https://anthropic.com/research/agentic-misalignment
