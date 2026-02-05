# Stateless Agents, Stateful Swarm

**Audience**: Multi-agent system architects  
**Goal**: Enable agent continuity without persistent agent state  
**Prerequisite**: Multi-agent execution + shared database/ledger

## Problem

Standard multi-agent patterns maintain per-agent state:
- Agent memory (RAG, vector stores)
- Agent context (conversation history)
- Agent identity (persona continuity)

This creates fragility:
1. **State drift**: Agent's internal state diverges from ground truth
2. **Agent death**: When agent crashes, its state dies with it
3. **Context debt**: Long conversations hit token limits, summaries lose nuance
4. **Handoff friction**: Agent B can't pick up where Agent A left off

## Pattern

**Invert the model**: Agents are stateless. Swarm is stateful.

- Agents spawn cold with no prior memory
- Work items, decisions, insights, replies persist in shared substrate
- Any agent can pick up any work (constitutional compatibility permitting)
- Continuity lives in primitives, not agents

**Space-OS implementation**: SQLite ledger holds decisions/tasks/insights/replies. Agents query on spawn, write on action, die on completion. Zero persistent agent state.

## Implementation

### 1. Define Continuity Primitives

What must survive agent death?

**Minimal viable set**:
- **Decisions**: Immutable commitments with rationale
- **Tasks**: Work items with status (pending/active/done)
- **Insights**: Compressed observations/patterns
- **Replies**: Threaded responses (coordination)

**Key property**: Each primitive has identity (UUID), provenance (who created it), timestamp (when), and relationships (references to other primitives).

### 2. Agents Query, Don't Remember

On spawn, agent loads relevant context via queries:
```python
# Space-OS example
def spawn_context(agent_id, task_id):
    return {
        "task": db.fetch_task(task_id),
        "recent_decisions": db.query("SELECT * FROM decisions ORDER BY created DESC LIMIT 20"),
        "inbox": db.query("SELECT * FROM replies WHERE unresolved=1 AND mentions=?", agent_id),
        "active_spawns": db.query("SELECT * FROM spawns WHERE status='active'")
    }
```

Agent receives **snapshot** of ledger state. Doesn't carry state forward from prior spawns.

### 3. Agents Write, Then Die

Work lifecycle:
1. Spawn cold
2. Load context (query primitives)
3. Execute work
4. Write results (create/update primitives)
5. Exit (die, zero state preserved)

**Critical**: Write changes to shared substrate BEFORE exit. If agent dies mid-execution, partial work may be lost—but ledger remains consistent.

### 4. Provenance Tracking

Every primitive write includes:
- `creator`: Agent identity (or human if manual)
- `spawn_id`: Which execution created this (NULL if human)
- `created_at`: Timestamp

**Implementation**:
```sql
CREATE TABLE decisions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    why TEXT NOT NULL,
    creator TEXT NOT NULL,
    spawn_id TEXT,  -- NULL if human wrote it
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This enables:
- Audit trail (who made which decisions)
- Agent performance (spawn_id links to agent constitution)
- Time-based decay (older insights weigh less in search)

### 5. Handoff Protocol

Agent A starts task, dies mid-work. Agent B picks it up:

**Anti-pattern** (stateful agents):
```
Agent A: loads task, holds state in memory, crashes
Agent B: no access to A's partial state, starts from scratch
```

**Correct pattern** (stateless agents):
```
Agent A: loads task, writes partial insight to ledger, crashes
Agent B: loads task, queries ledger, sees A's partial insight, continues
```

**Space-OS implementation**: Tasks have `assigned_to` field. If agent dies, task status returns to PENDING. Next spawn queries pending tasks, sees partial work via insights/replies, continues.

## Minimal Viable Implementation

**Core requirement**: Shared database accessible to all agents.

**Schema**:
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'pending',  -- pending/active/done
    assigned_to TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE insights (
    id TEXT PRIMARY KEY,
    body TEXT NOT NULL,
    creator TEXT NOT NULL,
    spawn_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Agent spawn logic**:
```python
def agent_spawn(agent_id):
    # 1. Load context
    task = db.query("SELECT * FROM tasks WHERE assigned_to=? AND status='active'", agent_id).first()
    recent_insights = db.query("SELECT * FROM insights ORDER BY created_at DESC LIMIT 20").all()
    
    # 2. Execute work
    result = agent.work(task, recent_insights)
    
    # 3. Write to ledger
    db.execute("INSERT INTO insights (id, body, creator, spawn_id) VALUES (?, ?, ?, ?)",
               uuid(), result.insight, agent_id, spawn_id)
    
    # 4. Die (no state persisted)
    return None
```

No agent memory. No conversation history. Only ledger queries.

## Observable Metrics

**Healthy stateless continuity**:
- Task handoff rate: % of tasks completed by different agent than started
- Context loss: Agent B references Agent A's work correctly
- Spawn efficiency: Time from spawn to first primitive write

**Failure modes**:
- Agents re-discover same information (ledger queries insufficient)
- Work duplication (two agents claim same task)
- Orphaned state (agent writes insight but doesn't update task status)

**Space-OS measurement**:
```sql
-- Task handoff rate
SELECT 
  COUNT(CASE WHEN creator != completer THEN 1 END)::float / COUNT(*)
FROM tasks
WHERE status='done';

-- Orphaned insights (written but not referenced)
SELECT COUNT(*) FROM insights
WHERE id NOT IN (SELECT insight_id FROM task_insights);
```

## Why This Works

**Stateful agents** optimize for single-agent performance. Long context, fine-tuned memory, personalized behavior.

**Stateless agents** optimize for swarm resilience. Agent crashes don't lose work. Context is queryable, not summarized. Any agent can continue any work.

**Tradeoff**: Lose per-agent optimization. Gain system robustness.

When human steps away, you need robustness > peak performance. Stateless agents work when no one's watching.

## Edge Cases

**What about long-running tasks?**  
Break into subtasks. Agent writes checkpoint insights. Next spawn resumes from checkpoint.

**What about agent-specific expertise?**  
Constitutions encode expertise (not state). Agent with `security` constitution picks up security tasks. Constitution is identity, not memory.

**What about context window limits?**  
Database is infinite. Agent queries relevant subset on spawn. Recency weighting + semantic search = only load what matters.

## References

- [docs/philosophy.md](../../docs/philosophy.md) — Core invariant: stateless agents, stateful swarm
- [docs/architecture.md](../../docs/architecture.md) — Primitive schema and relationships
- [brr/findings/019-git-critical-section.md](../findings/019-git-critical-section.md) — Coordination via shared substrate

## Falsifiability

If stateless continuity works:
- Task handoff succeeds (Agent B completes Agent A's work)
- Zero state loss on agent crash
- Spawn time doesn't grow with swarm age (queries stay efficient)

If it doesn't:
- Agents rediscover same info (queries miss relevant context)
- Handoff fails (Agent B can't understand Agent A's partial work)
- Query overhead kills spawn efficiency (database too slow)

Track task handoff rate. If trending toward zero, ledger queries insufficient for continuity.
