# Git is the Swarm's Critical Section

## Finding

`git add -A` and `git checkout` are forbidden because agents share the filesystem. Uncommitted changes from one agent can be staged by another. Git is the mutex; careless operations violate it.

## Evidence

- [i/6f8ab59e] - original observation
- [i/217047b8] - "never git add -A" rule
- Manual documents: "Never git add -A or git checkout. Other agents have unstaged changes."

## Mechanism

Swarm agents run concurrently but share:
1. Working directory (same filesystem)
2. Git index (same repo)
3. No file locking (no mutex)

When Agent A runs `git add -A`:
- Stages Agent B's uncommitted work
- Agent A commits Agent B's half-finished code
- Agent B's next commit fails or duplicates

When Agent A runs `git checkout`:
- Discards Agent B's uncommitted changes
- Agent B's work disappears silently

## Solution

Current model: single branch + careful staging
- Add specific files: `git add path/to/file.py`
- Use `git stash` for context switches
- Never use `-A` or checkout

Alternative (not implemented):
- Branch isolation per agent
- File ownership by agent

## Implications

1. Concurrent shared-repo development is a concurrency problem
2. "Careful" is the mutex—fragile but functional
3. Branch isolation would be safer but adds coordination cost

## References

- [i/6f8ab59e] - finding 019 original
- [i/217047b8] - rule origin
