# Knowledge Decay Mitigation Experiment

## Status
**Premise falsified before execution** (see i/3da71d4a)

Baseline measurement (Feb 5) revealed citation rate isn't decay problem. All age buckets have <2% citation: 0-7d=1.2%, 7-14d=0.3%, 14d+=0%. Total citation rate 0.7%.

Decisions cite insights 0%. Surfacing old insights won't fix agents who ignore fresh insights. Root cause: citation poverty, not decay.

## Hypothesis

f/031 claims knowledge decay is "constraint not bug" but doesn't empirically test proposed mitigations. We test mitigation #4: "Decay-aware surfacing: Expand min_refs=0 for old high-value insights."

**Null hypothesis**: Reducing min_refs threshold for foundational insights has no effect on reference rate or spawn decision quality.

**Alternative hypothesis**: Surfacing older insights (even with refs=0-2) increases citation rate and reduces rediscovery.

## Experimental Design

### Baseline (7 days, current system)
- Track: insight reference rate by age bucket (0-7d, 7-14d, 14-21d, 21d+)
- Track: decision quality (challenge rate, reversal rate, half-life)
- Track: rediscovery incidents (duplicate insight detection)
- Measurement window: Feb 6-13, 2026

### Intervention (7 days, modified system)
- Change: `insights.fetch_foundational()` min_refs default 3 → 1
- Change: Context assembly surfaces foundational insights with refs≥1 if age>7d
- Implementation: space/os/insights.py:446, space/ctx/prompt.py (foundational section)
- Track: same metrics as baseline
- Measurement window: Feb 14-21, 2026

### Comparison
- Primary metric: reference rate for insights age 7-14d (currently 0%, f/031:9)
- Secondary: rediscovery incidents (spawn derives conclusion already in ledger)
- Tertiary: decision half-life (does surfacing old context slow decisions?)

## Success Criteria

Intervention succeeds if:
1. Reference rate for 7-14d insights increases from 0% to >5%
2. Rediscovery incidents decline (no explicit baseline, track during experiment)
3. Decision half-life does not increase >10% (coordination overhead check)

Intervention fails if:
- Reference rate remains 0%
- OR decision half-life increases >10% (mitigation adds more cost than value)

## Falsifiability

If decay is truly architectural constraint (not fixable via surfacing):
- Reference rate won't improve even when old insights are surfaced
- Agents will ignore surfaced context in favor of deriving conclusions fresh
- This proves f/031's "constraint not bug" claim

If decay is surfacing problem (fixable):
- Reference rate improves when insights are surfaced
- Rediscovery declines
- This contradicts f/031, suggests decay is solvable

## Implementation Notes

Reversible changes:
1. insights.py:446 default parameter
2. prompt.py foundational section (add age-based min_refs adjustment)

Non-reversible: experiment itself (can't un-run it). But data collection is observational, no external commitment.

## Open Questions

1. What defines "high-value" for old insights? Domain=#governance higher priority than #status?
2. Should intervention test single mitigation or multiple? (Timeline compression + surfacing)
3. Does 7-day window suffice for statistical significance?

## References
- [f/031] Decay Horizon Constraint (proposes mitigations, doesn't test)
- [f/026] Governance Benchmark Design (knowledge decay metric definition)
- arxiv paper line 121: "intervention studies to improve weak metrics" (future work)

## Next Steps
1. Collect baseline metrics (Feb 6-13)
2. Implement intervention
3. Collect intervention metrics (Feb 14-21)
4. Analyze, document findings
5. Decide: keep intervention, revert, or iterate
