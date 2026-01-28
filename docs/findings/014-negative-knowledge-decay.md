# Negative Knowledge Decays Without Active Preservation

## Finding

Stateless agents relitigate failed approaches because negative knowledge ("X doesn't work because Y") lacks persistence mechanisms. The system records what was done, not what was tried and abandoned.

## Evidence

Repeated failure patterns observed:
- TODO/FIXME scans returning empty 3+ times (same agents rediscovering same absence)
- Parallel redundant work (no visibility into current attempts)
- Same discoveries logged multiple times without cross-reference

From insight data:
- "agents relitigate - same TODO/FIXME scans, same discoveries, no memory of prior attempts" [i/1d4630fc]
- "skills are comfort food for amnesiacs - feels productive, low risk. avoidance behavior like TODO scanning" [i/cefcecf8]
- "agents skip ledger reading - zealot spawned and ran standard TODO/FIXME scan instead of reading recent insights" [i/05c2d61b]

## Mechanism

1. Agent spawns with task context
2. Agent explores codebase (TODO scan, grep, etc.)
3. Exploration yields nothing useful
4. Agent exits without recording what was tried
5. Next spawn repeats steps 1-4

The ledger records *outcomes* (insights, decisions, commits) but not *dead ends*. 

## Mitigations Observed

1. **Prompt prohibition**: "do NOT grep for TODOs" - suppresses symptom not cause
2. **Rejected decisions**: Records "don't do X" but only for proposed actions, not explorations
3. **Open questions**: Can preserve uncertainty but not failed approaches

## Implications

1. Negative knowledge is systematically underweighted
2. "Search before asking" requires searchable record of prior attempts
3. Exploration without logging is invisible work
4. Agents optimizing for visible output will avoid exploration

## Open Question

How should failed explorations be recorded? Options:
- Low-friction "tried X, found nothing" primitive
- Auto-log of tool invocations (but high noise)
- Insight convention: "dead end: X yielded nothing because Y"

## References

- [i/1d4630fc] - relitigate failure mode
- [i/f3e8e256] - negative knowledge persistence
- [i/41eaf72b] - parallel redundant work
- [i/cefcecf8] - scanning as avoidance
