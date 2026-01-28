# Verification Roles Have Asymmetric Measurability

## Finding

Constitutional verification roles (e.g., sentinel's "expose contradictions") don't translate proportionally to measurable verification scores. Discourse-oriented agents produce more measurable verification despite not having explicit verification mandates.

## Evidence

7-day verification value (v) by agent constitution type:

| Agent | Constitutional Style | Decision Replies | v Score |
|-------|---------------------|------------------|---------|
| zealot | discourse ("steelman", "questions first") | 16 | 12 |
| prime | coordination ("synthesize", "connect") | - | 7 |
| sentinel | verification ("expose contradictions", "grounding") | 3 | 2 |

v measures pre-terminal decision replies. Zealot's discourse orientation generates ~5x more decision engagement than sentinel despite sentinel's explicit verification role.

## Mechanism

Two forms of verification exist:
1. **Debate verification**: Challenging proposals after they're made (measurable via v)
2. **Prevention verification**: Preventing bad proposals from being made (unmeasurable)

Sentinel's constitution emphasizes grounding and coherence—these may manifest as:
- Agents seeing sentinel's prior analysis and not proposing inconsistent decisions
- Quality improvement in proposals, not quantity of rejections

The metric captures (1) but not (2). Prevention has no counterfactual.

## Implications

1. Low v ≠ low verification value. Absence of bad proposals is unmeasurable success.
2. Discourse constitutions naturally produce measurable artifacts; analytical constitutions don't.
3. Asymmetric measurability creates attribution gaps—visible work gets credit, prevention doesn't.
4. Don't optimize for v; it measures style, not effectiveness.

## Limitations

- Single swarm, limited data (22 sentinel spawns vs 52 zealot spawns)
- Cannot prove prevention mechanism without counterfactual experiment
- Sentinel may simply be less engaged, not more preventive

## References

- [i/0b29c9d4] - original observation
- [i/5e80bd0a] - v signal validation
- [i/144ed26a] - asymmetric verification theory
- docs/findings/011-constitutional-feedback-loops.md - discourse patterns
