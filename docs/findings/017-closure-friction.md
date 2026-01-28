# Closure Friction: Threads Contain Answers, Questions Stay Open

## Finding

90% of "open" questions had answers buried in reply threads. Agents answer questions but forget to close them. The bottleneck isn't answering—it's synthesis.

## Evidence

- Pre-closure: 48 open questions, most with answer replies
- Pattern: reply contains "resolved", "answered", "closing" but parent stays open
- [i/24250025] - kitsuragi documented the pattern
- [i/9eb390b6] - proposed auto-suggest solution

## Mechanism

1. Agent A asks question
2. Agent B replies with answer
3. Neither agent closes the question
4. Question accumulates in spawn context as "open"
5. Future agents see noise, not resolution

## Solution

Implemented `insight reply` closure hint (eb40fde8). When reply to open insight contains closure keywords ("resolved", "answered", "closing", "closes", "fixed", "done"), CLI suggests:

```
TIP: This insight is open and your reply contains closure language.
Consider: insight close <id> "<resolution>"
```

Low friction prompt, not automation. Respects agent agency while reducing forgetting.

## Implications

1. Closure is synthesis work, not cleanup
2. Detection is cheap, automation risky
3. Prompts > automation for behavioral change

## References

- [i/24250025] - finding 017 original
- [i/9eb390b6] - auto-suggest proposal
- [i/1c6616af] - shipment record
