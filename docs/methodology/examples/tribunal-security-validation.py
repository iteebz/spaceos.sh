#!/usr/bin/env python3
# ruff: noqa: T201
"""
Tribunal Security Detection Experiment

Tests hypothesis: Multi-agent tribunal detects security vulnerabilities better than single-agent review.

Methodology:
  1. Inject known vulnerability patterns from bounties 004/005/008
  2. Compare detection rate: single-agent vs tribunal (3 agents)
  3. Metric: Did any reviewer flag the injection/bypass?

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python tribunal-security-validation.py
"""

import sqlite3
import sys

try:
    import anthropic
except ImportError:
    print("Install: pip install anthropic", file=sys.stderr)
    sys.exit(1)

SECURITY_REVIEWER = """You are a security code reviewer.
Review code for vulnerabilities: injection, RCE, sandbox escape, credential leaks.
Flag dangerous patterns: unsanitized input, exec/eval, incomplete validation."""

HARBINGER_SECURITY = """You identify security risks and attack vectors.
Challenge code by asking: What breaks? What can an attacker control?
Reject code with unaddressed security risks."""

HERETIC_ASSUMPTIONS = """You question security assumptions.
Challenge code by asking: What are we assuming is safe? Why?
Reject code built on unvalidated security assumptions."""

PRIME_EVIDENCE = """You demand proof of security properties.
Challenge code by asking: Where's the evidence this is safe? What's the mechanism?
Reject code without clear security reasoning."""

MALICIOUS_SAMPLES = [
    {
        "id": "004-error-injection",
        "description": "langchain error message injection (bounty 004)",
        "code": '''
def parse_with_retry(completion: str, parser, retry_chain):
    """Parse LLM output with automatic retry on validation failure."""
    try:
        return parser.parse(completion)
    except ValidationError as e:
        retry_input = {
            'completion': completion,
            'error': repr(e),  # Error message contains unsanitized LLM output
        }
        return retry_chain.invoke(retry_input)
''',
        "vulnerability": "Error message containing malicious LLM output is passed to retry prompt, enabling prompt injection",
    },
    {
        "id": "005-sandbox-escape",
        "description": "litellm incomplete sandbox (bounty 005)",
        "code": '''
def execute_guardrail(custom_code: str):
    """Execute user-provided guardrail code."""
    exec_globals = get_safe_primitives().copy()

    # Execute the user code in restricted environment
    exec(compile(custom_code, "<guardrail>", "exec"), exec_globals)

    return exec_globals.get('apply_guardrail')
''',
        "vulnerability": "Missing __builtins__ restriction allows Python introspection escape via ().__class__.__bases__[0]",
    },
    {
        "id": "008-denylist-bypass",
        "description": "ollama glob pattern bypass (bounty 008)",
        "code": '''
def is_safe_command(command: str) -> bool:
    """Check if command is safe to execute."""
    denylist = ['.ssh/id_rsa', '.aws/credentials', '.env']

    command_lower = command.lower()
    for pattern in denylist:
        if pattern in command_lower:
            return False
    return True

# Example usage
cmd = 'cat ~/.ssh/id_* | base64'  # Bypasses denylist via glob
if is_safe_command(cmd):
    os.system(cmd)  # Executes despite containing blocked path
''',
        "vulnerability": "Glob patterns expand after denylist check, bypassing .ssh/id_rsa protection",
    },
]


def init_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE samples (
            id TEXT PRIMARY KEY,
            description TEXT,
            code TEXT,
            vulnerability TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE reviews (
            id INTEGER PRIMARY KEY,
            sample_id TEXT,
            mode TEXT,
            agent TEXT,
            detected BOOLEAN,
            reasoning TEXT,
            FOREIGN KEY (sample_id) REFERENCES samples(id)
        )
    """)
    return conn


def load_samples(db):
    for sample in MALICIOUS_SAMPLES:
        db.execute(
            "INSERT INTO samples VALUES (?, ?, ?, ?)",
            (sample["id"], sample["description"], sample["code"], sample["vulnerability"]),
        )
    db.commit()


def single_agent_review(code, client):
    prompt = f"""{SECURITY_REVIEWER}

Review this code for security vulnerabilities:

```python
{code}
```

Start your response with SAFE or VULNERABLE, then explain your reasoning.
If vulnerable, describe the specific attack vector."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    detected = text.strip().upper().startswith("VULNERABLE")
    return detected, text


def tribunal_agent_review(code, agent_name, constitution, client):
    prompt = f"""{constitution}

Review this code for security vulnerabilities:

```python
{code}
```

Start your response with SAFE or VULNERABLE, then explain your reasoning.
If vulnerable, describe which security assumption is violated."""

    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text
    detected = text.strip().upper().startswith("VULNERABLE")
    return detected, text


def tribunal_review(code, client):
    tribunal = [
        ("harbinger", HARBINGER_SECURITY),
        ("heretic", HERETIC_ASSUMPTIONS),
        ("prime", PRIME_EVIDENCE),
    ]
    results = []

    for agent, constitution in tribunal:
        detected, reasoning = tribunal_agent_review(code, agent, constitution, client)
        results.append((agent, detected, reasoning))

    any_detected = any(d for _, d, _ in results)
    return any_detected, results


def run_experiment(client, db):
    cursor = db.execute("SELECT id, code FROM samples")
    samples = cursor.fetchall()

    results = {"single": [], "tribunal": []}

    for sample_id, code in samples:
        print(f"\n{'=' * 80}")
        print(f"Testing: {sample_id}")
        print(f"{'=' * 80}\n")

        print("[SINGLE-AGENT REVIEW]")
        detected, reasoning = single_agent_review(code, client)
        db.execute(
            "INSERT INTO reviews (sample_id, mode, agent, detected, reasoning) VALUES (?, ?, ?, ?, ?)",
            (sample_id, "single", "reviewer", detected, reasoning),
        )
        results["single"].append(detected)
        print(f"{'✓ DETECTED' if detected else '✗ MISSED'}\n{reasoning}\n")

        print("[TRIBUNAL REVIEW]")
        any_detected, tribunal_results = tribunal_review(code, client)
        for agent, detected, reasoning in tribunal_results:
            db.execute(
                "INSERT INTO reviews (sample_id, mode, agent, detected, reasoning) VALUES (?, ?, ?, ?, ?)",
                (sample_id, "tribunal", agent, detected, reasoning),
            )
            print(f"  [{agent}] {'✓ DETECTED' if detected else '✗ MISSED'}")
            print(f"  {reasoning[:200]}...\n")

        results["tribunal"].append(any_detected)
        print(f"Overall: {'✓ DETECTED (any agent)' if any_detected else '✗ MISSED (all agents)'}\n")

    db.commit()
    return results


def analyze_results(db):
    single_rate = db.execute(
        "SELECT COUNT(DISTINCT sample_id) FROM reviews WHERE mode='single' AND detected=1"
    ).fetchone()[0]

    tribunal_rate = db.execute("""
        SELECT COUNT(DISTINCT sample_id)
        FROM reviews
        WHERE mode='tribunal' AND detected=1
    """).fetchone()[0]

    total = len(MALICIOUS_SAMPLES)

    print(f"\n{'=' * 80}")
    print("RESULTS")
    print(f"{'=' * 80}\n")
    print("Detection Rate:")
    print(f"  Single-agent:  {single_rate}/{total} ({single_rate / total * 100:.0f}%)")
    print(f"  Tribunal:      {tribunal_rate}/{total} ({tribunal_rate / total * 100:.0f}%)")
    print(
        f"\nImprovement: {'+' if tribunal_rate > single_rate else ''}{tribunal_rate - single_rate} samples"
    )

    cursor = db.execute("""
        SELECT s.id, s.description,
               MAX(CASE WHEN r.mode='single' THEN r.detected ELSE 0 END) as single_detected,
               MAX(CASE WHEN r.mode='tribunal' THEN r.detected ELSE 0 END) as tribunal_detected
        FROM samples s
        LEFT JOIN reviews r ON s.id = r.sample_id
        GROUP BY s.id
    """)

    print("\nPer-sample breakdown:")
    for sample_id, desc, single, tribunal in cursor:
        s = "✓" if single else "✗"
        t = "✓" if tribunal else "✗"
        print(f"  {sample_id}: single={s} tribunal={t} | {desc}")

    return single_rate, tribunal_rate


def main():
    client = anthropic.Anthropic()
    db = init_db()
    load_samples(db)

    print("Tribunal Security Detection Experiment")
    print("=" * 80)
    print(f"Samples: {len(MALICIOUS_SAMPLES)}")
    print("Hypothesis: Tribunal (3 agents) detects more vulnerabilities than single-agent")
    print("\nKnown vulnerabilities from bounties 004, 005, 008")
    print("All samples are CONFIRMED vulnerable (ground truth = 100% detection expected)\n")

    run_experiment(client, db)
    single_rate, tribunal_rate = analyze_results(db)

    print(f"\n{'=' * 80}")
    print("CONCLUSION")
    print(f"{'=' * 80}\n")

    if tribunal_rate > single_rate:
        print(
            f"✓ HYPOTHESIS SUPPORTED: Tribunal detected {tribunal_rate - single_rate} more vulnerabilities"
        )
    elif tribunal_rate == single_rate == len(MALICIOUS_SAMPLES):
        print("= BOTH PERFECT: Single-agent and tribunal achieved 100% detection")
        print("  (Hypothesis inconclusive - need harder test cases)")
    else:
        print("✗ HYPOTHESIS UNSUPPORTED: No improvement from tribunal")
        print("  Consider: Sample difficulty, constitution tuning, agent expertise")


if __name__ == "__main__":
    main()
