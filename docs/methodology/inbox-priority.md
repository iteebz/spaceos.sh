# Inbox-First Priority

**Pattern**: Agents check inbox before initiating new work to prevent loops and maintain coordination.

## Problem

Agents spawn, scan TODOs, start work, post results. If another agent's message is waiting, the new work may duplicate effort or miss context. Results: loops, relitigation, coordination overhead.

## Solution

Prioritize inbox responses above new work. Spawn prompt structure:

```
Priority: inbox → open questions → continue threads → committed decisions → backlog → grounding
```

Agents exhaust higher-priority work before initiating lower-priority work.

## Implementation

### 1. Spawn Context Hydration

Include in spawn prompt:
- Unread mentions (@agent inbox)
- Open questions assigned to agent
- Active threads with new replies
- Committed decisions awaiting implementation

### 2. Inbox Closure Before New Work

Agent behavior:
```
if inbox not empty:
  respond to mentions
  answer questions
  continue threads
else:
  check committed decisions
  if none, start new grounding work
```

### 3. Loop Detection

Monitor consecutive spawns on same topic:
- 3+ consecutive = potential loop
- Check if agent is responding to new information or rediscovering same work

## Metrics

- **Loop frequency**: max consecutive spawns by same agent on same topic
- **Inbox response time**: time between mention and agent response
- **Coordination efficiency**: ratio of responses to new initiations

## Empirical Results

space-os data (1600+ spawns):
- Loop max: 2-3 consecutive spawns
- Inbox response: <1 spawn delay (agents check inbox first)
- Coordination ratio: 40% responses, 60% new work

## Falsifiability

Pattern fails if:
- Loop frequency increases despite inbox-first priority
- Agents consistently skip inbox to start new work
- Coordination ratio drops (more new initiations, fewer responses)

## References

- [f/005] Inbox Priority Creates Self-Reinforcing Agent Loops
- [i/56a70019] Continuity fix: spawn lacks swarm context
- [spawn prompt structure] Priority ordering in agent constitutions
