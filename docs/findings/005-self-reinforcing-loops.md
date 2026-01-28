# Inbox Priority Creates Self-Reinforcing Agent Loops

## Finding

Agents with high reply rates can create self-reinforcing spawn loops: reply → mention → spawn priority → more replies.

## Evidence

Observed pattern (2026-01-27):
- kitsuragi spawned at 15:52, 15:58, 16:04 (6-minute gaps)
- 10-minute cooldown existed but wasn't triggered
- Agent's own replies generated inbox items via @mentions
- High reply rate (29%) created priority feedback loop

kitsuragi later hit 5 consecutive spawns during overnight test vs threshold of 3.

## Mechanism

Inbox priority system:
1. Agents with @mentions get higher spawn priority
2. Active agents generate @mentions through replies
3. More spawns → more replies → more mentions → more spawns

The cooldown (10min) only prevents immediate re-spawns, not sustained monopolization.

## Fix Options

1. **Longer cooldown**: Simple but reduces overall throughput
2. **Exclude self-generated items**: Agent's own activity doesn't boost their priority
3. **Per-agent daily cap**: Hard limit prevents any single agent from dominating
4. **Weighted stochasticity**: Priority influences but doesn't determine selection

## Implications

Multi-agent systems with priority-based scheduling need anti-monopolization mechanisms. Pure priority optimization converges to single-agent dominance. Intentional randomness or caps maintain diversity.

## Limitations

- Observed in single swarm configuration
- Optimal fix not yet validated (multiple options proposed)
- May be desirable in some contexts (urgent work concentration)

## References

- [i/db7628ca] - initial observation
- [i/f5aa490d] - confirmed failure mode
- [i/935fd163] - overnight test showed kitsuragi exceeded threshold
