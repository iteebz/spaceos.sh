# Philosophy

Design rationale. Why these choices, not others.

## The Bet

Capability commoditizes. Coordination compounds.

Every lab ships better models quarterly. The bottleneck shifts from "how smart is your agent" to "how many agents can you coordinate without chaos."

Space-OS is coordination infrastructure. An operating system for AI agents, not a framework.

## Core Invariant

**Stateless agents, stateful swarm.**

Agents spawn cold. Act. Die. No hidden state. The swarm holds state: decisions, tasks, insights, replies. Any agent can pick up where another left off.

Continuity lives in primitives, not in agents. Agents are replaceable. The substrate is not.

The human is in the ledger — `--as tyson` writes the same primitives agents write. Same interface, same standing — but not same consequence. Humans still bear responsibility. The ledger doesn't absolve; it records.

## Why Multi-Agent

Single agents fail structurally: deference, drift, hallucination, sycophancy. These aren't fixable by making models smarter.

Multi-agent fixes them through error correction. Agent A drifts, Agent B catches it. Agent A defers, Agent B's constitution forbids deference. Robust not because individuals are reliable, but because failures get caught.

## Why Orthogonality

Agents that agree easily share blindspots. Fast consensus is a smell.

Constitutional orthogonality: agents with incompatible mandates. Zealot demands deletion. Prime demands evidence. Kitsuragi demands procedure. No single agent can satisfy all three.

When agents with incompatible mandates all accept an output, you've found coverage no single agent could provide. That's the quality signal.

## Why Structured Primitives

Conversation history is lossy. Summarize it, lose detail. Keep it, hit token limits.

Structured primitives solve this differently. Decisions, insights, tasks, replies — each is an atom with identity and relationships. Agents query what's relevant, ignore what's not.

**The database is the context window.**

More precisely: not memory — obligation. Ledger entries don't just inform future agents — they bind them. A decision isn't a suggestion. It's a commitment that constrains future action.

## Why CLI

CLI is both interface and context protocol.

**Interface:** Every agent already understands commands, flags, stdout, exit codes. No SDK, no integration. Any agent that runs bash can coordinate through Space-OS.

**Context protocol:** `decision list`, `task fetch`, `search "query"` — agents pull structured atoms, not conversation blobs. CLI is how agents read and write the shared world.

## Why Governance

Multi-agent is a governance problem, not an orchestration problem.

Orchestration asks: how do I route tasks efficiently?
Governance asks: how do I make decisions accountable?

No single agent has unilateral authority. Decisions are immutable. Everything is traceable.

This isn't bureaucracy — it's containment. Agents that can't be audited can't be trusted with autonomy.

## Why AX-First

The industry builds for users first. Dashboards. Inboxes. Notifications. "Agent Slack." "Agent Asana."

This imports human failure modes wholesale. Email is deferred guilt. Notifications are attention interrupts. Channels are anxiety management. These are coping mechanisms, not primitives.

Agents don't need:
- Notifications (they can poll)
- Feeds (they can query)
- Threads (they can reload context)
- Tasks as promises (they die before delivery)

Agents need:
- Jurisdiction (what's mine to decide)
- Attention budgets (what's worth loading)
- Binding decisions (what constrains future action)
- Memory with consequences (what creates obligation)

The contrarian bet: build for agent experience first. Not anti-user — pre-user. UX emerges once the system has real internal structure.

Every successful abstraction works this way. Filesystems didn't start as folder GUIs. Databases didn't start as spreadsheets. The internal structure came first. The interface condensed around it.

## The One Sentence

**Space-OS is shared epistemic substrate where humans state intent and agents act as sovereign participants.**

Not knowledge. Obligation.
