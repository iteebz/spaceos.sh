#!/usr/bin/env python3
# ruff: noqa: T201
"""
Minimal Tribunal Pattern Reference Implementation

Demonstrates adversarial frame validation: executive proposes, tribunal challenges.
No space-os dependencies. Requires: anthropic SDK, sqlite3 (stdlib).

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python minimal-tribunal.py "Improve user retention by adding more features"
"""

import sqlite3
import sys

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

EXECUTIVE = """You are a strategic planner.
Given a goal, propose a concrete plan with specific actions.
Focus on execution and deliverables."""

HARBINGER = """You identify risks and failure modes.
Challenge proposals by asking: What breaks? When? Under what conditions?
Reject plans with unaddressed risks."""

HERETIC = """You question premises and assumptions.
Challenge proposals by asking: Is this the right problem? What are we assuming?
Reject plans built on unvalidated assumptions."""

PRIME = """You demand evidence and rigor.
Challenge proposals by asking: Where's the proof? What's the mechanism?
Reject plans without clear reasoning."""


def init_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE proposals (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            plan TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY,
            proposal_id INTEGER,
            agent TEXT,
            verdict TEXT,
            reasoning TEXT,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id)
        )
    """)
    return conn


def executive_propose(goal, client):
    prompt = f"""{EXECUTIVE}

Goal: {goal}

Propose a concrete plan with 2-3 specific actions to achieve this goal."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def tribunal_review(plan, goal, agent_name, constitution, client):
    prompt = f"""{constitution}

Goal: {goal}

Proposed Plan:
{plan}

Review this plan. Start your response with APPROVE or REJECT, then explain your reasoning.
If rejecting, specify which constraint is violated and suggest a revision."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    verdict = "APPROVE" if text.strip().upper().startswith("APPROVE") else "REJECT"
    return verdict, text


def tribunal_validation(goal, plan, client, db, proposal_id):
    tribunal = [
        ("harbinger", HARBINGER),
        ("heretic", HERETIC),
        ("prime", PRIME),
    ]
    results = []

    for agent, constitution in tribunal:
        verdict, reasoning = tribunal_review(plan, goal, agent, constitution, client)
        db.execute(
            "INSERT INTO reviews (proposal_id, agent, verdict, reasoning) VALUES (?, ?, ?, ?)",
            (proposal_id, agent, verdict, reasoning),
        )
        results.append((agent, verdict, reasoning))

    db.commit()
    return results


def measure_challenge_rate(db):
    cursor = db.execute("SELECT COUNT(*) FROM reviews")
    total = cursor.fetchone()[0]
    cursor = db.execute("SELECT COUNT(*) FROM reviews WHERE verdict='REJECT'")
    rejected = cursor.fetchone()[0]
    return rejected / total if total > 0 else 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    goal = sys.argv[1]
    client = anthropic.Anthropic()
    db = init_db()

    print(f"Goal: {goal}\n")
    print("=" * 80)
    print("\n[EXECUTIVE] Proposing plan...\n")

    plan = executive_propose(goal, client)
    print(f"{plan}\n")
    print("=" * 80)

    cursor = db.execute("INSERT INTO proposals (goal, plan) VALUES (?, ?)", (goal, plan))
    proposal_id = cursor.lastrowid
    db.commit()

    print("\n[TRIBUNAL] Reviewing proposal...\n")
    results = tribunal_validation(goal, plan, client, db, proposal_id)

    for agent, verdict, reasoning in results:
        print(f"[{agent.upper()}] {verdict}")
        print(f"{reasoning}\n")
        print("-" * 80 + "\n")

    all_approved = all(v == "APPROVE" for _, v, _ in results)
    print("=" * 80)
    print(
        f"\nDecision: {'PROCEED (unanimous approval)' if all_approved else 'BLOCKED (requires all reviewers to approve)'}"
    )
    print(f"Challenge rate: {measure_challenge_rate(db):.0%}")

    if not all_approved:
        print("\nNext steps:")
        print("1. Address tribunal objections")
        print("2. Revise proposal")
        print("3. Resubmit for review")


if __name__ == "__main__":
    main()
