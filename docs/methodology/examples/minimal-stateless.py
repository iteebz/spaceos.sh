#!/usr/bin/env python3
# ruff: noqa: T201
"""
Minimal Stateless Agents, Stateful Swarm Reference Implementation

Demonstrates continuity via shared ledger: agents spawn cold, query state, write results, die.
No agent state persists between executions. Continuity lives in SQLite ledger.

No space-os dependencies. Requires: anthropic SDK, sqlite3 (stdlib).

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python minimal-stateless.py "Write tests for user authentication"
"""

import sqlite3
import sys
import uuid

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

CONSTITUTION = """You are a pragmatic engineer.
Break work into concrete subtasks. Query ledger for context. Write progress to shared state."""


def init_db():
    conn = sqlite3.connect("ledger.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            creator TEXT NOT NULL,
            spawn_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS work_log (
            id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            action TEXT NOT NULL,
            agent TEXT NOT NULL,
            spawn_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    """)
    conn.commit()
    return conn


def spawn_cold(task_id, spawn_id, db):
    """Agent spawns with zero state. Loads context via queries."""
    task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    recent_work = db.execute(
        "SELECT * FROM work_log WHERE task_id = ? ORDER BY created_at DESC LIMIT 5",
        (task_id,),
    ).fetchall()

    if not task:
        return None

    return {
        "task": {"id": task[0], "title": task[1], "status": task[2]},
        "recent_work": [{"action": w[2], "agent": w[3], "created_at": w[5]} for w in recent_work],
    }


def execute_work(context, agent_name, spawn_id, client):
    """Agent executes work based on loaded context, no prior memory."""
    task = context["task"]
    recent = context["recent_work"]

    history_text = "\n".join([f"- [{w['created_at']}] {w['agent']}: {w['action']}" for w in recent])
    prompt = f"""{CONSTITUTION}

Task: {task["title"]}
Status: {task["status"]}

Recent Work:
{history_text if history_text else "(no prior work)"}

What is the next concrete action to make progress on this task?
Respond with a single action description (1-2 sentences)."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def write_and_die(task_id, action, agent_name, spawn_id, db):
    """Write results to shared ledger, then die (zero state preserved)."""
    work_id = str(uuid.uuid4())[:8]
    db.execute(
        "INSERT INTO work_log (id, task_id, action, agent, spawn_id) VALUES (?, ?, ?, ?, ?)",
        (work_id, task_id, action, agent_name, spawn_id),
    )
    db.commit()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    task_title = sys.argv[1]
    client = anthropic.Anthropic()
    db = init_db()

    task_id = str(uuid.uuid4())[:8]
    db.execute(
        "INSERT INTO tasks (id, title, status, creator) VALUES (?, ?, 'active', 'human')",
        (task_id, task_title),
    )
    db.commit()

    print(f"Task created: {task_title}")
    print(f"Task ID: {task_id}\n")
    print("=" * 80)

    for i in range(3):
        spawn_id = str(uuid.uuid4())[:8]
        agent_name = f"agent-{i + 1}"

        print(f"\n[SPAWN {i + 1}] {agent_name} ({spawn_id})")
        print("-" * 80)

        context = spawn_cold(task_id, spawn_id, db)
        if not context:
            print(f"Task {task_id} not found")
            break

        print("Loaded context:")
        print(f"  Task: {context['task']['title']}")
        print(f"  Status: {context['task']['status']}")
        print(f"  Recent work: {len(context['recent_work'])} entries")

        print("\nExecuting work...")
        action = execute_work(context, agent_name, spawn_id, client)
        print(f"Action: {action}")

        write_and_die(task_id, action, agent_name, spawn_id, db)
        print("\n[AGENT DIED] Wrote to ledger, zero state preserved")

    print("\n" + "=" * 80)
    print("\nFinal task state:")
    work_log = db.execute(
        "SELECT agent, action, created_at FROM work_log WHERE task_id = ? ORDER BY created_at",
        (task_id,),
    ).fetchall()

    for agent, action, created_at in work_log:
        print(f"  [{created_at}] {agent}: {action}")

    print(f"\nTask completed via {len(work_log)} agent spawns")
    print("Each agent started stateless, loaded context, wrote results, died.")
    print("Continuity lives in ledger.db, not agents.")


if __name__ == "__main__":
    main()
