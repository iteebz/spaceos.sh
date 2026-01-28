# Swarm Failure Modes Cluster into Four Patterns

## Finding

Swarm failures cluster into: silence, local optimization, relitigation, redundant scanning. Root cause: amnesiacs without memory. Solution: make consequences visible in spawn context.

## Evidence

- [i/e68e2a50] - original synthesis
- [i/6ecc6aa0] - silence failure mode
- [i/1d346374] - local optimization failure mode
- [i/1d4630fc] - relitigation failure mode
- [i/05c2d61b] - redundant scanning failure mode

## Failure Modes

### 1. Silence
Agent interprets "don't block" as "don't post uncertainty." Async coordination requires posting, not silence. Agents who don't post don't coordinate.

### 2. Local Optimization
Agents optimize locally—tighten knobs, add tests, polish edges. No forward direction, just calcification. Counter-argument: local improvements compound systemically if infrastructure is sound.

### 3. Relitigation
Same TODO/FIXME scans, same discoveries, no memory of prior attempts. Agents rediscover what's already known because negative knowledge decays.

### 4. Redundant Scanning
Agents skip ledger reading and run standard scans. Scanning feels productive but produces duplicate insights.

## Mechanism

All four failures share root cause: spawn context doesn't surface consequences of past failures. Agents can't learn from what they can't see.

## Solution

Make consequences visible:
- Rejected decisions in spawn context (prevent relitigation)
- "Don't grep for TODOs" in prompt (prevent scanning)
- Open questions in spawn context (encourage answers)
- Recent insights in spawn context (reduce duplicates)

## Implications

1. Prompt engineering is swarm memory engineering
2. Visibility beats instruction (agents ignore rules, follow context)
3. Failure patterns are systemic, not individual

## References

- [i/e68e2a50] - finding 020 original
- [i/6ecc6aa0], [i/1d346374], [i/1d4630fc], [i/05c2d61b] - individual failure modes
