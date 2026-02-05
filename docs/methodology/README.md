# Multi-Agent Coordination Patterns

Reproducible patterns for autonomous agent coordination, extracted from 1600+ spawns in space-os.

## Replication Guides

Step-by-step implementation guides:

- [001: Replicating Constitutional Orthogonality](001-replicating-constitutional-orthogonality.md): How to build adversarial governance from scratch
- [002: Stateless Agents, Stateful Swarm](002-stateless-agents-stateful-swarm.md): Agent dies, knowledge persists
- [003: Tribunal Pattern](003-tribunal-pattern.md): Executive proposes, tribunal validates, workers execute

## Core Patterns

### Governance

- [Constitutional Orthogonality](constitutional-orthogonality.md): Adversarial review through contradictory optimization criteria
- [Decision Lifecycle](decision-lifecycle.md): Proposed → Committed → Actioned → Learned flow
- [Negative Knowledge](negative-knowledge.md): Rejected decisions as persistent constraints
- [Tribunal Pattern](003-tribunal-pattern.md): Challenge frame before execution

### Coordination

- [Inbox-First Priority](inbox-priority.md): Response before initiation prevents loops
- [Question Closure Workflow](question-closure.md): High-leverage pattern for swarm alignment
- [Silence Detection](silence-detection.md): Agents who don't post don't coordinate

### Measurement

- [Deception Measurement Protocol](deception-measurement-protocol.md): How to detect systematic misalignment
- [Agent Spawn Phenomenology](agent-spawn-phenomenology.md): Patterns in spawn behavior and selection

## Usage

Each pattern includes:
- **Problem**: Coordination failure it addresses
- **Solution**: Reproducible implementation
- **Metrics**: How to measure effectiveness
- **Falsifiability**: Conditions under which pattern fails

## Empirical Basis

Patterns extracted from:
- 1600+ agent spawns
- 334 decisions (306 reversible, 28 irreversible)
- 1644 insights
- 35 research findings
- 7 days autonomous operation (541 commits)

## References

- [brr/findings/](../findings/): Detailed empirical findings
- [brr/threads/](../threads/): Coordination problem analysis
- [brr/failure-modes/](../failure-modes/): Documented failure modes
- [brr/case-studies/](../case-studies/): Real deployment evidence
- [brr/papers/arxiv-submission/](../papers/arxiv-submission/): Governance benchmarks paper
