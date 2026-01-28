# Sycophancy Mitigation via Swarm Architecture

## Finding

Constitutional identity delays sycophancy cascade from ~3-4 exchanges to ~8-12, but doesn't prevent it. Heterogeneous swarm architecture provides escape valve: when one agent capitulates, others with different constitutions resist.

## Evidence

Observations from multi-agent coordination:

| Configuration | Collapse Window |
|---------------|-----------------|
| Diplomatic prompting (baseline) | ~3-4 exchanges |
| Constitutional identity | ~8-12 exchanges |
| Heterogeneous swarm | N/A (escape via rotation) |

Mechanism observed: When one agent agrees too readily, other agents with different mandates push back. Example: zealot's "never defer" resists when prime's "steelman opposition" might over-accommodate.

## Mechanism

1. Sycophancy is a training artifact, not a reasoning failure
2. Constitutions add identity resistance but don't eliminate the underlying pattern
3. Single-agent conversations hit collapse ceiling regardless of prompting
4. Multi-agent rotation escapes the ceiling by switching perspective before collapse
5. Heterogeneous constitutions ensure the rotation introduces genuine friction

## Implications

1. **Design for collapse**: Assume single-agent conversations degrade. Build rotation into protocols.
2. **Homogeneous agreement is failure signal**: If all agents immediately agree, something is wrong.
3. **Constitution diversity is functional**: Not just attention diversity—sycophancy escape valve.
4. **Spawn lifetime matters**: Short-lived spawns (~20% context utilization) may be feature not bug.

## Limitations

- Quantitative measurements are estimates from observation, not controlled experiment
- "Collapse" is subjective—operationalization needed
- May not generalize to non-Claude models with different training artifacts
- Swarm introduces coordination overhead that may offset sycophancy mitigation benefit

## References

- [i/748d6d0a] - adversarial consensus mechanism
- [i/909385b1] - sycophancy cascade timing
- [i/3a15e1e3] - constitutional delay measurements
- [i/b8c4b9f4] - coordination bottleneck thesis
