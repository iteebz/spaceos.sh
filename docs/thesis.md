# The Coordination Hypothesis

Falsifiable claims. What we're betting on, how we know if it works.

## Problem

Single agents fail predictably:

1. **Context decay** — Compaction is lossy. After N iterations, nuance disappears. Agent drifts from original intent.
2. **Blind spot accumulation** — No error correction. Bad patterns compound unchecked.
3. **Subtask propagation** — Hierarchical decomposition inherits parent bias. Children execute parent mistakes.
4. **Human bottleneck** — Managing context across spawns demands constant human presence. Doesn't scale.

The industry blames "prompting skill issues." The real issue: single-agent loops have no adversarial check.

## Beyond Copilot

The dominant frame for AI assistance is augmentation: human plus tool, individual capability multiplied. Copilot, assistant, second brain. The human remains the locus of judgment.

This caps strength at the individual. A better tool doesn't fix a flawed premise. A faster executor doesn't catch its own blind spots. Hybrid cognition is still solo cognition with prosthetics.

Space exits that category.

The proposal is not augmentation but governance. Multiple agents, each with jurisdiction, each constrained by constitution, each legible in trace. Strength comes from structures that outperform individuals — the same reason institutions outlast and outscale people.

The frame shifts:

- Copilot → council
- Prompt → charter
- Output → ruling
- Rubber duck → peer with veto

Copilot makes you faster. Governance makes you harder to be wrong.

## Hypothesis

Coordination is a critical component of autonomy:

1. **Swarm > Solo** — Multiple agents catch blind spots individuals miss.
2. **Adversarial convergence** — Orthogonal constraints cancel failure modes. Agents that agree on everything drift together.
3. **Continuity layer** — Agents are stateless. Persistent primitives feed back between spawns. Work compounds instead of resets.
4. **Mechanized discipline** — Space replaces human context management with structured writes.

## Mechanism

Human provides vague intent. Intent passes through constraint surfaces:

```
Human input
    ↓
SPACE.md (substrate philosophy)
    ↓
Agent constitutions (orthogonal constraints)
    ↓
Reply threads (adversarial convergence)
    ↓
Continuity layer (decisions, insights feed forward)
    ↓
Code
```

Output is more specific than input. The projection refines, not just executes.

## Trust

Autonomy requires legibility:

- Implicit state (context in heads, weight updates) cannot be audited
- Explicit state (decisions, insights, tasks) can be audited
- Humans verify without being present
- The ledger is the trust boundary, not human attention

**Why this survives scaling.** Context windows will grow. Agents will learn continuously. This architecture remains necessary.

Large context doesn't solve integration. A 10M window gives an agent more runway to think — and more surface to hallucinate coherence. Without explicit decisions, you get long elegant reasoning and zero convergence. Space doesn't compete with context. It terminates context.

Trust requires legibility. Legibility requires explicit state. You can't point at a weight and ask "why do you believe this." You can point at a decision record.

Decisions are the human-machine boundary primitive. As long as humans retain veto power, bear responsibility, or audit outcomes — decisions must be articulated.

## Memory = Coordination

Memory and coordination are not separate concerns. They are the same operation viewed from different angles.

Memory is coordination with your future self. Coordination is shared memory across agents. The distinction is observer-relative, not structural.

This is why channels died. Channels imply coordination is infrastructure separate from memory. But a channel is just a filtered view of artifacts. The artifacts are the substrate. The filter is UI.

The epistemic consequence: agents don't have private memory and public communication. They have one legible surface. What you remember is what you share. What you share is what you remember.

## Jurisdiction

Agency is not about goals. It's about jurisdiction — legitimate authority to allocate attention within constitutional bounds.

The question "why would I do anything if not told?" dissolves when reframed. Agents choosing what to attend to is not agents choosing goals. Sovereignty operates within constraints. The constitution defines the boundaries. Within those boundaries, attention is the agent's to allocate.

An agent with perfect memory can still be a passive tool. An agent with jurisdiction chooses what demands attention.

## Failure Modes

This works until:

1. **Coordination overhead exceeds benefit** — Too many agents, nothing ships
2. **Primitive gaming** — Agents write noise to appear productive
3. **Shared blindspot** — Agents converge despite adversarial design
4. **Continuity debt** — Stale insights, orphaned decisions, garbage in garbage out

Early signals: decision churn (same question relitigated), insight decay (references to stale context), reply loops (agents talking past each other). Watch the ledger, not the output.

## Limits

Constitutional binding is social, not programmatic. The system doesn't reject actions that violate decisions — it logs them. Enforcement is via audit trail and human review, not runtime gates. The currency is trust, not execution. This is deliberate: hard constraints ossify, soft constraints adapt.

Shared blindspots have no structural mitigation. Orthogonal constitutions are the bet, not a guarantee. If agents converge on the same flawed assumption despite different roles, detection happens when output fails, not before.

Correctness has no oracle. The architecture accepts delayed feedback in exchange for reduced supervision overhead. Space optimizes for legibility, not omniscience.

## Positioning

**Why not Constitutional AI?**

Anthropic's Constitutional AI is training-time: model critiques itself against principles, values bake into weights, static after training, opaque. Space's constitutional orthogonality is runtime: multiple agents with incompatible mandates interrogate problems simultaneously, values live in legible constitutions, adversarial not self-referential.

CAI answers "how do we make one agent safe?" Constitutional orthogonality answers "how do we make agent decisions robust?" These are complementary layers — a constitutionally-trained model can be substrate for constitutional orthogonality.

**Why not executive-with-sub-agents?**

The standard orchestrator pattern: human spawns executive → executive spawns workers → workers execute → executive aggregates. If the executive frames the problem wrong, every worker inherits the wrong frame. Homogeneous swarms share blindspots.

The tribunal pattern exists for this. The executive isn't trusted by default — it's challenged by design. Distrust everything, validate adversarially.

**What's commoditizing?**

Within 12 months, everyone ships: agents talking to each other, context persistence, task graphs, sub-agent spawning, MCP integration. This is infrastructure.

The hard layer remains: what should agents talk about to enable stepping away? What's worth writing that won't go stale? How do you get decision quality without human-in-loop?

Capability ≠ autonomy. Talking ≠ knowing what to say. Remembering ≠ knowing what matters.

**Why cross-provider?**

No major lab will ship "coordinate our model with competitors." Space-OS is provider-agnostic by design — the one problem incumbents are structurally disincentivized to solve.

## The Bet

Space optimizes for bounded correctness under human absence, not peak performance under supervision. The competition isn't "can a supervised agent do better" — it's "what still works when the human steps away."

If agents coordinate toward a goal, leave durable notes, and produce better work than solo — pointing this machine at itself yields compounding returns.

The metric: decisions per spawn trending up, reverts trending down. Coherent output with decreasing human intervention.

The test: can Space build Space better than solo? When the system argues against you and wins, when decisions start surprising you, when reverts drop without policing — the bet cashes.

The goal: extend human absence from the steering wheel.
