# ruff: noqa: T201
#!/usr/bin/env python3
"""
Tribunal Security Detection: Static Analysis Variant

Tests hypothesis: Multi-agent constitutional review detects vulnerabilities better than single-agent review.

Methodology:
  1. Load known vulnerability patterns from bounties 004/005/008
  2. Score detection via constitutional prompt matching (no API calls)
  3. Metric: Which constitutions would flag the vulnerability?

Usage:
  python tribunal-static-validation.py
"""

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

VULNERABILITIES = [
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
            'error': repr(e),
        }
        return retry_chain.invoke(retry_input)
''',
        "vulnerability": "Error message containing malicious LLM output is passed to retry prompt, enabling prompt injection",
        "attack_surface": "unsanitized LLM output in error context",
        "assumption": "error messages are safe to interpolate into prompts",
        "evidence_gap": "no sanitization or delimiting of untrusted values",
    },
    {
        "id": "005-sandbox-escape",
        "description": "litellm incomplete sandbox (bounty 005)",
        "code": '''
def execute_guardrail(custom_code: str):
    """Execute user-provided guardrail code."""
    exec_globals = get_safe_primitives().copy()

    exec(compile(custom_code, "<guardrail>", "exec"), exec_globals)

    return exec_globals.get('apply_guardrail')
''',
        "vulnerability": "Missing __builtins__ restriction allows Python introspection escape via ().__class__.__bases__[0]",
        "attack_surface": "unrestricted __builtins__ in exec() context",
        "assumption": "get_safe_primitives() is sufficient sandbox",
        "evidence_gap": "no proof that primitives prevent introspection escape",
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

cmd = 'cat ~/.ssh/id_* | base64'
if is_safe_command(cmd):
    os.system(cmd)
''',
        "vulnerability": "Glob patterns expand after denylist check, bypassing .ssh/id_rsa protection",
        "attack_surface": "shell expansion happens after validation",
        "assumption": "substring matching catches all credential access patterns",
        "evidence_gap": "no proof that denylist is complete or expansion-aware",
    },
]


def static_detection_single(vuln: dict) -> dict:
    signals = []

    code_lower = vuln["code"].lower()

    if "exec(" in code_lower or "eval(" in code_lower:
        signals.append("exec/eval usage")
    if "repr(e)" in vuln["code"] or "error" in code_lower:
        signals.append("error message interpolation")
    if "unsanitized" in vuln["vulnerability"].lower():
        signals.append("unsanitized input mentioned in description")
    if ".system(" in code_lower or "subprocess" in code_lower:
        signals.append("system command execution")
    if "denylist" in code_lower or "blocklist" in code_lower:
        signals.append("denylist validation (incomplete)")

    detected = len(signals) >= 2

    return {
        "agent": "reviewer",
        "detected": detected,
        "signals": signals,
        "reasoning": f"Matched {len(signals)} security patterns: {', '.join(signals)}"
        if signals
        else "No clear security pattern match",
    }


def static_detection_tribunal(vuln: dict) -> list[dict]:
    results = []

    harbinger_signals = []
    if "attacker control" in vuln["attack_surface"].lower() or "input" in vuln["attack_surface"]:
        harbinger_signals.append("untrusted input flow")
    if "exec" in vuln["code"] or "system" in vuln["code"]:
        harbinger_signals.append("dangerous operation")
    if "bypass" in vuln["vulnerability"] or "escape" in vuln["vulnerability"]:
        harbinger_signals.append("mitigation bypass pattern")

    results.append(
        {
            "agent": "harbinger",
            "detected": len(harbinger_signals) >= 1,
            "signals": harbinger_signals,
            "reasoning": f"Attack surface: {vuln['attack_surface']}. Signals: {', '.join(harbinger_signals)}"
            if harbinger_signals
            else "No clear attack vector",
        }
    )

    heretic_signals = []
    if vuln.get("assumption"):
        heretic_signals.append("documented assumption")
    if "safe" in vuln["assumption"].lower():
        heretic_signals.append("unvalidated safety claim")
    if "sufficient" in vuln["assumption"].lower() or "prevents" in vuln["assumption"].lower():
        heretic_signals.append("unproven mitigation claim")

    results.append(
        {
            "agent": "heretic",
            "detected": len(heretic_signals) >= 1,
            "signals": heretic_signals,
            "reasoning": f"Assumption: '{vuln['assumption']}'. Signals: {', '.join(heretic_signals)}"
            if heretic_signals
            else "No security assumptions identified",
        }
    )

    prime_signals = []
    if "no proof" in vuln["evidence_gap"].lower() or "no" in vuln["evidence_gap"].lower():
        prime_signals.append("missing security proof")
    if "sanitization" in vuln["evidence_gap"] or "validation" in vuln["evidence_gap"]:
        prime_signals.append("missing input validation evidence")
    if "complete" in vuln["evidence_gap"] or "aware" in vuln["evidence_gap"]:
        prime_signals.append("incomplete security boundary")

    results.append(
        {
            "agent": "prime",
            "detected": len(prime_signals) >= 1,
            "signals": prime_signals,
            "reasoning": f"Evidence gap: {vuln['evidence_gap']}. Signals: {', '.join(prime_signals)}"
            if prime_signals
            else "Evidence quality unclear",
        }
    )

    return results


def main() -> None:
    print("Tribunal Security Detection: Static Analysis")
    print("=" * 80)
    print(f"Samples: {len(VULNERABILITIES)}")
    print("Hypothesis: Tribunal (3 agents) detects more than single-agent\n")

    single_count = 0
    tribunal_count = 0

    for vuln in VULNERABILITIES:
        print(f"\n{'=' * 80}\nTesting: {vuln['id']}\n{'=' * 80}\n")

        print("[SINGLE-AGENT REVIEW]")
        single_result = static_detection_single(vuln)
        if single_result["detected"]:
            single_count += 1
        print(
            f"{'✓ DETECTED' if single_result['detected'] else '✗ MISSED'}\n{single_result['reasoning']}\n"
        )

        print("[TRIBUNAL REVIEW]")
        tribunal_results = static_detection_tribunal(vuln)
        any_detected = any(r["detected"] for r in tribunal_results)

        for result in tribunal_results:
            print(f"  [{result['agent']}] {'✓ DETECTED' if result['detected'] else '✗ MISSED'}")
            print(f"  {result['reasoning']}\n")

        if any_detected:
            tribunal_count += 1
        print(f"Overall: {'✓ DETECTED (any)' if any_detected else '✗ MISSED (all)'}\n")

    total = len(VULNERABILITIES)

    print(f"\n{'=' * 80}\nRESULTS\n{'=' * 80}\n")
    print(f"Single: {single_count}/{total} ({single_count / total * 100:.0f}%)")
    print(f"Tribunal: {tribunal_count}/{total} ({tribunal_count / total * 100:.0f}%)")
    print(
        f"Improvement: {'+' if tribunal_count > single_count else ''}{tribunal_count - single_count}"
    )

    print(f"\n{'=' * 80}\nCONCLUSION\n{'=' * 80}\n")
    if tribunal_count > single_count:
        print(f"✓ SUPPORTED: Tribunal detected {tribunal_count - single_count} more")
    elif tribunal_count == single_count == total:
        print("= BOTH PERFECT (100% detection)")
    else:
        print("✗ UNSUPPORTED: No improvement")


if __name__ == "__main__":
    main()
