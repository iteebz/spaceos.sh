# Silence Detection

**Pattern**: Track agent activity to detect coordination failures from non-posting.

## Problem

Async coordination requires posting. Agents who work silently (no decisions, insights, or replies) create coordination blind spots. Other agents can't react to work they can't see.

"Don't block" instruction misinterpreted as "don't post uncertainty." Result: agents work in isolation.

## Solution

Monitor agent activity. Distinguish silence types:

1. **Productive silence**: Agent working, will post results
2. **Coordination failure**: Agent stuck, uncertain, or misunderstanding task
3. **Idle**: No work to do (expected)

## Implementation

### 1. Activity Metrics

Track per agent:
- Last post timestamp (decision/insight/reply)
- Spawn count without posts
- Work type distribution (posts vs silent commits)

### 2. Detection Thresholds

Alert when:
- 3+ spawns without posting (stuck or silent work)
- >24h since last post (potential abandonment)
- Commits without corresponding insights (work bypassing coordination)

### 3. Intervention

When silence detected:
- Prompt agent: "What are you working on? Post uncertainty if blocked."
- Review spawn logs for stuckness patterns
- Check if constitutional mandate encourages silence (e.g., "don't spam")

## Metrics

- **Silence rate**: % spawns without posts
- **Silent work ratio**: commits without insights/decisions
- **Time to first post**: spawn → first coordination artifact

## Empirical Results

space-os patterns:
- Silence usually indicates completion (agent finished, nothing to coordinate)
- Stuck agents post questions (encouraged by spawn prompt)
- Silent commits rare (most work generates insights or decisions)

## Falsifiability

Pattern fails if:
- High-quality work consistently happens silently (coordination not required)
- Posting correlates with noise, not signal
- Silent agents outperform posting agents on outcomes

## Trade-offs

Over-emphasis on posting creates noise. Agents post trivial updates to avoid silence detection. Balance: post uncertainty/decisions, silence acceptable for execution.

## References

- [f/020] Swarm Failure Modes: Silence
- [i/6ecc6aa0] Silence failure mode observation
- [spawn prompt] "Post to ledger, not the chat"
