# Multi-Agent Swarms Can Operate Autonomously Overnight

## Finding

100 sequential agent spawns over 8+ hours with no human intervention produced 51 commits and maintained healthy system metrics.

## Evidence

Test parameters (d/9b341ac4):
- 100 sequential spawns
- No human intervention
- No changes to focus directive

Results:
- 51 commits shipped
- All agents >4.9 artifacts/spawn (baseline: 2.0-8.6)
- Decision influence: 9.4% (improved from 0.6%)
- Compounding rate: 4.7% (stable)
- No system crashes or runaway loops

One concern: kitsuragi hit 5 consecutive spawns vs threshold of 3, indicating daemon prioritization could be tuned.

## Mechanism

Overnight autonomy requires:
1. Task queue with clear priorities (inbox, backlog)
2. Loop detection (consecutive same-agent threshold)
3. Distributed attention (multiple agents with different focus areas)
4. Self-correction via peer review (decision rejection mechanism)

The swarm self-organized work allocation without explicit coordination.

## Implications

1. Autonomous agent systems can sustain productive work for extended periods
2. Human oversight can be asynchronous rather than synchronous
3. Value of overnight autonomy = work completed while human unavailable
4. Risk: self-perpetuating activity vs. externally valuable work (separate validation needed)

## Limitations

- Single test run (N=1)
- No control group (what would random task selection produce?)
- Quality of 51 commits not independently assessed
- "Valuable autonomy" vs "self-perpetuating activity" not distinguished

## References

- [d/9b341ac4] - overnight test decision
- [i/935fd163] - test results
- [i/9ae725f4] - quality question raised
