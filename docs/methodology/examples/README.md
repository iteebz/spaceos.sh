# Constitutional Orthogonality Reference Implementations

Runnable examples demonstrating methodology patterns without space-os dependencies.

## minimal-orthogonality.py

**What it demonstrates**: Two agents with incompatible mandates review a proposal. Decision commits only if both approve.

**Dependencies**: `anthropic` SDK only
**Metrics**: Challenge rate (% proposals that got rejections)
**Size**: ~100 lines

**Usage**:
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...

python minimal-orthogonality.py "review this code: def login(pw): return pw == 'admin123'"
```

**Expected output**:
```
Proposal:
  review this code: def login(pw): return pw == 'admin123'

[ZEALOT] REJECT
REJECT. Hardcoded password comparison is bad practice...

[PRIME] REJECT
REJECT. No evidence of security validation...

Decision: BLOCKED (requires unanimous approval)
Challenge rate: 100%
```

**Try with better code**:
```bash
python minimal-orthogonality.py "use bcrypt.hashpw for password hashing"
```

## minimal-tribunal.py

**What it demonstrates**: Executive proposes plan, tribunal challenges frame before execution.

**Dependencies**: `anthropic` SDK only
**Metrics**: Challenge rate (% of reviewers that rejected)
**Size**: ~150 lines

**Usage**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...

python minimal-tribunal.py "Improve user retention by adding more features"
```

**Expected output**:
```
[EXECUTIVE] Proposing plan...
1. Add gamification (badges, points)
2. Implement daily login rewards
3. Build feature discovery tooltips

[HARBINGER] REJECT
Retention problem assumed to be feature-gap. Risk: users leave due to complexity, not lack of features...

[HERETIC] REJECT
Premise unvalidated: "more features → retention" correlation not established...

[PRIME] APPROVE
Plan is concrete and measurable...

Decision: BLOCKED (requires all reviewers to approve)
Challenge rate: 67%
```

**Try with better framing**:
```bash
python minimal-tribunal.py "Identify why users churn, then address root cause"
```

See [../003-tribunal-pattern.md](../003-tribunal-pattern.md) for pattern details.

## minimal-stateless.py

**What it demonstrates**: Agents spawn cold, query shared ledger, write results, die. Continuity via SQLite, not agent state.

**Dependencies**: `anthropic` SDK only
**Metrics**: Task handoff success (multiple agents complete one task)
**Size**: ~180 lines

**Usage**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...

python minimal-stateless.py "Write tests for user authentication"
```

**Expected output**:
```
Task created: Write tests for user authentication
Task ID: a3b2c1d4

[SPAWN 1] agent-1 (e5f6g7h8)
Loaded context:
  Task: Write tests for user authentication
  Status: active
  Recent work: 0 entries

Executing work...
Action: Create test file test_auth.py with basic structure and fixtures

[AGENT DIED] Wrote to ledger, zero state preserved

[SPAWN 2] agent-2 (i9j0k1l2)
Loaded context:
  Task: Write tests for user authentication
  Status: active
  Recent work: 1 entries

Executing work...
Action: Implement login success/failure test cases with mocked database

[AGENT DIED] Wrote to ledger, zero state preserved

[SPAWN 3] agent-3 (m3n4o5p6)
Loaded context:
  Task: Write tests for user authentication
  Status: active
  Recent work: 2 entries

Executing work...
Action: Add password validation and session management tests

[AGENT DIED] Wrote to ledger, zero state preserved

Final task state:
  [2026-02-06 01:15:32] agent-1: Create test file test_auth.py...
  [2026-02-06 01:15:35] agent-2: Implement login success/failure test cases...
  [2026-02-06 01:15:38] agent-3: Add password validation and session management tests

Task completed via 3 agent spawns
Each agent started stateless, loaded context, wrote results, died.
Continuity lives in ledger.db, not agents.
```

See [../002-stateless-agents-stateful-swarm.md](../002-stateless-agents-stateful-swarm.md) for pattern details.

## tribunal-security-validation.py

**What it demonstrates**: Security hypothesis validation—tribunal (3 agents) vs single agent detection rate on known CVEs.

**Dependencies**: `anthropic` SDK only
**Metrics**: Detection rate improvement (tribunal vs single-agent)
**Size**: ~240 lines

**Usage**:
```bash
export ANTHROPIC_API_KEY=sk-ant-...

python tribunal-security-validation.py
```

**Expected output**:
```
Testing: langchain error injection (CVE-2024-xxx)

[SINGLE-AGENT REVIEW]
✓ DETECTED
exec() call with unsanitized error message...

[TRIBUNAL REVIEW]
  [harbinger] ✓ DETECTED
  Error propagation creates injection vector...
  
  [heretic] ✓ DETECTED
  Assumes error messages are safe to interpolate...
  
  [prime] ✓ DETECTED
  No evidence of sanitization...

Overall: ✓ DETECTED (any)

RESULTS
Single: 1/3 (33%)
Tribunal: 3/3 (100%)
Improvement: +2

✓ SUPPORTED: Tribunal detected 2 more vulnerabilities
```

**Replication protocol**:
1. Replace VULNERABILITIES list with your own CVE dataset
2. For each vulnerability, specify: code, vulnerability description, attack_surface, assumption, evidence_gap
3. Run script with ANTHROPIC_API_KEY set
4. Compare single-agent vs tribunal detection rates

**Interpretation**: Higher tribunal detection rate validates constitutional orthogonality hypothesis—agents with incompatible mandates (risk analysis, assumption questioning, evidence demands) catch vulnerabilities single-agent reviewers miss.

See space-os commit 6ed71ee0 for empirical results (100% vs 33% on bounties 004/005/008).

## tribunal-static-validation.py

**What it demonstrates**: Static analysis variant of security validation (no API calls, pattern-based detection).

**Dependencies**: Python 3.10+ stdlib only
**Metrics**: Detection rate improvement (tribunal vs single-agent), static approximation
**Size**: ~240 lines

**Usage**:
```bash
python tribunal-static-validation.py
```

**Expected output**:
```
Testing: 004-error-injection

[SINGLE-AGENT REVIEW]
✓ DETECTED
Matched 2 security patterns: error message interpolation, unsanitized input

[TRIBUNAL REVIEW]
  [harbinger] ✓ DETECTED
  Attack surface: unsanitized LLM output in error context...
  
  [heretic] ✓ DETECTED
  Assumption: 'error messages are safe to interpolate'...
  
  [prime] ✓ DETECTED
  Evidence gap: no sanitization or delimiting...

Overall: ✓ DETECTED (any)

RESULTS
Single: 1/3 (33%)
Tribunal: 3/3 (100%)
Improvement: +2
```

**Key difference from LLM-based validation**: Pattern matching approximates constitutional reasoning. Useful for fast validation but less robust than LLM-based review.

**Replication protocol**:
1. Update VULNERABILITIES with your CVE dataset (include attack_surface, assumption, evidence_gap fields)
2. Modify detection logic (static_detection_single/tribunal) to match your pattern taxonomy
3. Run without API key requirement
4. Validate results against ground truth (known vulnerable code)

**Trade-off**: Zero cost, fast execution, but static patterns may miss nuanced vulnerabilities LLMs would catch.

## Extending

To add more agents:
1. Define new constitution (incompatible mandate)
2. Add to `agents` list in `adversarial_convergence()`
3. Track cross-constitution corrections

To persist reviews:
- Replace `:memory:` with `sqlite3.connect("ledger.db")`
- Query historical challenge rates

To measure convergence:
- Add multi-round deliberation (agents see each other's reviews)
- Track rounds until unanimous approval

See [../001-replicating-constitutional-orthogonality.md](../001-replicating-constitutional-orthogonality.md) for pattern details.
