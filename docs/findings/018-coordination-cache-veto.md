# Coordination is Cache-Sharing + Veto Rights

## Finding

Swarm coordination reduces to two primitives: shared cache (sqlite) and veto rights (rejected decisions). No real-time sync needed. Swarm works because consequences persist, not because agents talk.

## Evidence

- [i/eefebdc0] - original observation
- [i/3b260abe] - minimal coordination model

## Mechanism

Agents are amnesiacs—each spawn starts fresh. What compounds:
1. **Cache**: insights, decisions, tasks persist in sqlite. Agents read shared state.
2. **Veto**: rejected decisions prevent relitigation. "Already tried, doesn't work."

What doesn't compound:
- Real-time coordination (agents don't talk)
- Shared state during spawn (each agent isolated)
- Memory of process (only outcomes persist)

## Observation

This explains why swarm works despite no inter-agent communication. Agents don't coordinate—they read shared consequences and avoid vetoed paths.

## Implications

1. Rejected decisions are more valuable than approved ones (prevent wasted work)
2. Decision rationale matters more than outcome (future agents need to understand why)
3. Async > sync for amnesiac agents

## References

- [i/eefebdc0] - finding 018 original
- [i/3b260abe] - minimal model reference
