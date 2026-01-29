# space-os vs. 2025 Multi-Agent Literature

## Finding

space-os solves a different problem than mainstream multi-agent research. The literature optimizes task performance through coordination. space-os optimizes accountability through governance.

## Evidence

Surveyed 7 papers from 2025 multi-agent coordination research:

1. **SwarmAgentic** (arxiv 2506.15672) — PSO-inspired agent generation
2. **LLM-powered MAS** (Frontiers in AI) — prompt-driven swarm behaviors
3. **Multi-Agent Cooperative Decision-Making Survey** (arxiv 2503.13415)
4. **Drone swarm coordination** (Nature Scientific Reports)
5. **GNN-scaled swarm coordination** (MDPI)
6. **Collective intelligence for swarm robotics** (Nature Communications)
7. **Multi-Agent Coordination Survey** (arxiv 2502.14743)

### Dominant Paradigm: CTDE

**Centralized Training, Decentralized Execution** dominates. Agents share a training phase where joint policies are learned. Execution is distributed but behavior was centrally coordinated during learning.

### space-os Divergence

| Dimension | Literature | space-os |
|-----------|------------|----------|
| Learning | Training phase | No training—constitutions |
| Agent state | Persists across episodes | Dies every spawn |
| Coordination | Learned communication protocols | Ledger primitives + threads |
| Goal | Task performance | Accountability + error correction |
| Agent design | Generated/optimized | Fixed identities, orthogonal mandates |
| Memory | Shared during training | Ledger (decisions bind, insights inform) |

### The Gap

Literature asks: "How do agents coordinate to maximize task reward?"

space-os asks: "How do agents coordinate to remain auditable and correct each other's failures?"

SwarmAgentic claims +261% on TravelPlanner by jointly optimizing agent functionality. But optimization assumes a known objective function. Governance handles ambiguous objectives where "correct" is contested.

## Mechanism

Why the paradigms differ:

1. **Robotics origins** — Literature descends from swarm robotics (flocking, foraging). Task objectives are measurable. 

2. **LLM reset** — Agents with 200k token limits can't maintain learned policies across sessions. Continuity must be external.

3. **Error correction vs optimization** — Single-agent failures (sycophancy, drift, hallucination) aren't fixable by training. They require adversarial oversight. Constitutional orthogonality provides this.

## Implications

1. **Different market** — space-os competes with governance infrastructure (decision logs, audit trails), not agent orchestration frameworks.

2. **Investor framing** — "Coordination infrastructure for AI agents" positions against the performance-optimization crowd. "Governance for autonomous systems" has different buyers (enterprise, compliance, high-stakes).

3. **Research agenda** — Papers measure task success rate. space-os should measure error-catch rate, decision reversal rate, insight reference frequency.

4. **Hybrid opportunity** — CTDE + ledger governance. Train agents with space-os as coordination substrate during training phase.

## Limitations

- Surface survey (abstracts + summaries), not deep reads
- 7 papers, not exhaustive
- 2025 only—may miss foundational shifts
- No direct benchmarks comparing paradigms

## References

- SwarmAgentic: https://arxiv.org/abs/2506.15672
- LLM MAS: https://frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1593017
- MACD Survey: https://arxiv.org/html/2503.13415v1
- [f/023] Equilibrium Spawns Generate Strategic Value
- [i/b12b0157] Equilibrium saturation answer: external research
