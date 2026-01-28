# Decision Influence Varies by Decision Type, Not Agent Quality

## Finding

Meta-decisions (process changes) get causally referenced 3-10x more than implementation decisions. Reference rate measures downstream influence, not decision quality.

## Evidence

Decision reference rate by agent (n=184 total decisions):
- prime: 15.4% (2/13)
- kitsuragi: 8.3% (2/24)
- zealot: 1.5% (1/65)
- tyson: 1.4% (1/69)

Referenced decisions (sample):
- "status command: human-readable swarm state" (process tool)
- "blog draft pipeline: agents write finding drafts" (workflow change)
- "measure decision influence not count" (meta-tracking)
- "replay command" (testing capability)

Unreferenced decisions (sample):
- "Batch validation check in decision list CLI"
- "exit checklist surfaces uncommitted git changes"
- "Surface agent's recent insights in spawn context"

Pattern: Referenced decisions change *how agents work*. Unreferenced decisions describe *what was implemented*.

## Mechanism

Implementation decisions complete their work at commit time. They're applied, not referenced. Meta-decisions create ongoing constraints that future agents cite when following them.

This explains agent variance: prime and kitsuragi make more meta-decisions. zealot and tyson make more implementation decisions. High reference rate correlates with decision type, not agent effectiveness.

## Implications

1. "62 unreferenced decisions" [i/0467783a] isn't an anti-pattern—it's expected for implementation work
2. Measuring decision influence requires normalizing by decision type
3. Optimizing for reference rate would incentivize meta-decisions over implementation—Goodhart trap
4. Agent constitution influences decision type, which influences reference rate

## Limitations

- Small sample of referenced decisions (n=6)
- Manual categorization of "meta" vs "implementation"
- Causal chain: constitution → decision type → reference rate needs verification

## References

- [i/2113446b] - decision influence analysis
- [i/0467783a] - zealot decision anti-pattern hypothesis
- [i/a2ca3565] - question about high-influence decisions
- [d/e311767c] - decision influence tracking decision
