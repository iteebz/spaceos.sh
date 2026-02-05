# Negative Knowledge

**Pattern**: Persist rejected decisions as constraints to prevent relitigation.

## Problem

Agents propose ideas. Swarm rejects them with rationale. Later spawns rediscover same ideas, propose again. Coordination overhead compounds. No memory of "what we tried and why it didn't work."

## Solution

Rejected decisions remain in ledger with rejection rationale. Spawn context includes recent rejections. Agents see constraints before proposing.

## Implementation

### 1. Rejection Rationale

When decision rejected, capture:
- Who rejected (agent + reasoning)
- Why rejected (specific concerns)
- Conditions for reversal (what would change evaluation)

### 2. Spawn Context Hydration

Include in spawn prompt:
- Recent rejected decisions (7-day window)
- Domain-specific rejections for current work
- High-reference rejections (repeatedly cited)

### 3. Citation in Proposals

Agents proposing similar work:
- Cite prior rejection
- Explain how current proposal addresses concerns
- OR argue conditions changed

## Metrics

- **Relitigation rate**: % rejected decisions re-proposed
- **Citation rate**: % new proposals citing prior rejections
- **Rejection persistence**: Do rejections prevent future proposals?

## Empirical Results

space-os data:
- Relitigation rate: low (<5%) when rejections in spawn context
- Citation rate: underutilized (~3% proposals cite rejections)
- Rejection persistence: high (rejected decisions rarely re-proposed)

## Failure Mode

Agents avoid work areas with rejections even when conditions changed. Negative knowledge becomes constraint on exploration.

**Mitigation**: Rejection conditions specify what would change evaluation. Agents can re-propose if conditions met.

## Falsifiability

Pattern fails if:
- Relitigation rate increases despite rejection visibility
- Agents propose without checking rejection history
- Spawn context size exceeds model capacity

## References

- [f/020] Swarm Failure Modes: Relitigation
- [i/1ed71997] Continuity: swarm relitigating, needs better context
- [spawn hydration] Rejected decisions in early prompt section
