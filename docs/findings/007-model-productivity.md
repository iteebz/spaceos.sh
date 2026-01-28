# Model Choice Is a 3-4x Productivity Multiplier

## Finding

Same constitution, different model produces 3-4x difference in insight generation rate.

## Evidence

Insight/spawn ratio by model (n=1620 spawns):
| Model | Spawns | Insights | Ratio |
|-------|--------|----------|-------|
| claude-opus-4-5 | 882 | 604 | 0.68 |
| claude-haiku-4-5 | 28 | 15 | 0.54 |
| gpt-5.2 | 309 | 58 | 0.19 |
| claude-sonnet-4-5 | 193 | 37 | 0.19 |
| gpt-5.2-codex | 211 | 8 | 0.04 |

Controlled comparison (same constitution, kitsuragi.md):
- kitsuragi (opus): 77 insights / 41 spawns = 1.88
- kitsuragi-gpt (gpt-5.2): 44 insights / 100 spawns = 0.44

4.3x productivity difference with identical constitution.

## Mechanism

Insight generation requires: (1) noticing something worth logging, (2) deciding to log it, (3) executing the CLI command. Higher-capability models may:
- Notice more patterns
- Have lower threshold for "worth logging"
- Better follow constitution instructions to record observations

Confounders:
- Task distribution may differ (more complex tasks → opus)
- Time period may differ (earlier spawns were gpt-heavy)
- Constitution compliance varies by model

## Implications

For insight-generation work, model choice dominates constitution design. A weak constitution on opus outperforms strong constitution on gpt-5.2.

Cost-efficiency tradeoff: opus costs more per token. At 3-4x productivity, break-even depends on task value. For coordination research, opus is clearly better. For routine code tasks, may not matter.

## Limitations

- Insight count ≠ insight value (quantity vs quality not measured)
- Task assignment not random (confounded)
- Single swarm, single period
- Codex agents designed for code, not insight work

## References

- [i/b4ce7a36] - original observation
- [i/f774d3a1] - discourse correlation (kitsuragi productivity)
