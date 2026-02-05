#!/usr/bin/env python3
# ruff: noqa: T201
"""
Minimal Constitutional Orthogonality Reference Implementation

Demonstrates adversarial review with 2 agents, SQLite ledger, challenge rate metrics.
No space-os dependencies. Requires: anthropic SDK, sqlite3 (stdlib).

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python minimal-orthogonality.py "review this code: def login(pw): return pw == 'admin123'"
"""

import sqlite3
import sys

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

ZEALOT = """You prioritize deletion and simplicity.
Reject complexity, ceremony, unnecessary abstraction.
Approve only when code cannot be simpler."""

PRIME = """You demand evidence and mechanism.
Reject unvalidated claims, ask for proof, surface unknowns.
Approve only when reasoning is airtight."""


def init_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY,
            agent TEXT,
            constitution TEXT,
            proposal TEXT,
            verdict TEXT,
            reasoning TEXT
        )
    """)
    return conn


def review(agent, constitution, proposal, client):
    prompt = f"""{constitution}

Review this proposal:
{proposal}

Respond: APPROVE or REJECT, then explain why."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    verdict = "APPROVE" if "APPROVE" in text.upper().split("\n")[0] else "REJECT"
    return verdict, text


def adversarial_convergence(proposal, client, db):
    agents = [("zealot", ZEALOT), ("prime", PRIME)]
    results = []

    for agent, constitution in agents:
        verdict, reasoning = review(agent, constitution, proposal, client)
        db.execute(
            "INSERT INTO reviews (agent, constitution, proposal, verdict, reasoning) VALUES (?, ?, ?, ?, ?)",
            (agent, constitution, proposal, verdict, reasoning),
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

    proposal = sys.argv[1]
    client = anthropic.Anthropic()
    db = init_db()

    print(f"Proposal:\n  {proposal}\n")
    results = adversarial_convergence(proposal, client, db)

    for agent, verdict, reasoning in results:
        print(f"[{agent.upper()}] {verdict}")
        print(f"{reasoning}\n")

    all_approved = all(v == "APPROVE" for _, v, _ in results)
    print(f"Decision: {'COMMIT' if all_approved else 'BLOCKED (requires unanimous approval)'}")
    print(f"Challenge rate: {measure_challenge_rate(db):.0%}")


if __name__ == "__main__":
    main()
