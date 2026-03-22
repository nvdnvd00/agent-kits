---
name: systematic-debugging
description: 4-phase systematic debugging methodology with root cause analysis and evidence-based verification. Use when debugging complex issues, investigating production bugs, or when trial-and-error is failing.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Systematic Debugging - Scientific Defect Resolution

## ⚡ Quick Reference

- **4 phases**: Reproduce → Isolate → Root Cause (5 Whys) → Fix + Regression Test
- **Never guess**: Profile first · Read the full stack trace · Binary search commits with `git bisect`
- **Reproduce first**: Can't fix what you can't see · Get exact steps · Note env differences
- **Root cause**: Ask WHY 5 times · Fix cause not symptom · Symptom recurs if only patched
- **After fix**: Add regression test · Check similar code · Remove debug logs · Document root cause

---


---

## 🎯 Core Principle: Scientific Method for Bugs

```
❌ WRONG: Change random things → Hope it works → Repeat
✅ CORRECT: Observe → Hypothesize → Predict → Test → Verify
```

**The Scientific Debugging Approach:**

- Every change must be driven by a testable hypothesis
- One variable at a time
- Document evidence and outcomes
- Root cause, not symptom treatment

---

## 🔄 The 4-Phase Debugging Workflow

### Phase Overview

```
PHASE 1: REPRODUCE     → Reliably trigger the bug
    ↓
PHASE 2: DIAGNOSE      → Gather evidence, form hypotheses
    ↓
PHASE 3: FIX           → Apply targeted fix
    ↓
PHASE 4: VERIFY        → Confirm fix, prevent regression
```

---

## 📍 Phase 1: Reproduce

### Goal: Create a Minimal, Reliable Reproduction

**Without reliable reproduction, debugging is guessing.**

### Reproduction Checklist

```markdown
- [ ] Can trigger bug consistently (>90% success rate)
- [ ] Identified minimum steps to reproduce
- [ ] Know environment conditions (OS, browser, versions)
- [ ] Have isolated from unrelated factors
- [ ] Created automated test case if possible
```

### Information Gathering Template

```markdown
## Bug Reproduction Details

**Reported Behavior:** [What user/test observed]

**Expected Behavior:** [What should happen]

**Environment:**

- OS: [e.g., macOS 14.2]
- Runtime: [e.g., Node 20.10.0]
- Dependencies: [Key versions]

**Reproduction Steps:**

1. [Step 1]
2. [Step 2]
3. [Observe: Expected X, Got Y]

**Frequency:** [Always / Intermittent / Random]

**First Occurred:** [When / after what change]
```

### Handling Intermittent Bugs

| Pattern              | Investigation Approach                  |
| -------------------- | --------------------------------------- |
| Race condition       | Add timing logs, check for async issues |
| Memory-related       | Check for uninitialized variables       |
| State-dependent      | Log state at failure points             |
| Environment-specific | Compare configurations                  |
| Load-dependent       | Test under high load/concurrency        |

### If Bug Won't Reproduce

1. Check if bug is already fixed
2. Review recent code changes (git log)
3. Compare environments in detail
4. Add defensive logging for next occurrence
5. Set up alerts to capture live failure

---

## 🔬 Phase 2: Diagnose

### Goal: Identify Root Cause Through Evidence

### The Hypothesis Cycle

```
    ┌────────────────────────────────┐
    │         OBSERVE                │
    │   (Gather evidence/data)       │
    └──────────────┬─────────────────┘
                   ↓
    ┌────────────────────────────────┐
    │       HYPOTHESIZE              │
    │   (What could cause this?)     │
    └──────────────┬─────────────────┘
                   ↓
    ┌────────────────────────────────┐
    │         PREDICT                │
    │   (If hypothesis true, then..) │
    └──────────────┬─────────────────┘
                   ↓
    ┌────────────────────────────────┐
    │          TEST                  │
    │   (Run experiment)             │
    └──────────────┬─────────────────┘
                   ↓
             ┌─────┴─────┐
        Confirmed?   Refuted?
             ↓           ↓
         Refine      New Hypothesis
```

### Evidence Gathering Techniques

| Technique                | When to Use                        | How                             |
| ------------------------ | ---------------------------------- | ------------------------------- |
| **Strategic Logging**    | Understanding execution flow       | Add logs at decision points     |
| **Debugger Breakpoints** | Inspecting state at specific point | Set conditional breakpoints     |
| **Binary Search**        | Large codebase, unclear location   | Comment out half, narrow down   |
| **Stack Trace Analysis** | Exception/crash occurred           | Read trace bottom-up            |
| **Git Bisect**           | Bug appeared in recent commits     | Automate finding bad commit     |
| **Diff Analysis**        | Recently working code broke        | Compare working vs broken code  |
| **Rubber Duck**          | Logic seems correct but isn't      | Explain code line by line aloud |

### Hypothesis Documentation

```markdown
## Hypothesis #1: [Title]

**Statement:** [What you think is wrong]

**Evidence For:**

- [Supporting observation 1]
- [Supporting observation 2]

**Evidence Against:**

- [Contradicting observation if any]

**Test Plan:**

- [How to confirm or refute this]

**Prediction:**

- If true: [Expected observation]
- If false: [What we'd see instead]

**Result:** ✅ Confirmed / ❌ Refuted / 🔄 Needs more data
```

### Root Cause Categories

| Category          | Examples                              | Investigation Focus           |
| ----------------- | ------------------------------------- | ----------------------------- |
| **Logic Error**   | Wrong condition, off-by-one           | Step through logic carefully  |
| **State Problem** | Race condition, stale cache           | Track state changes over time |
| **Data Issue**    | Invalid input, null reference         | Inspect data at boundaries    |
| **Integration**   | API contract broken, version mismatch | Check integration points      |
| **Resource**      | Leak, exhaustion, timeout             | Monitor resource usage        |
| **Configuration** | Wrong env var, missing setting        | Compare environments          |

### 5 Whys Analysis

```markdown
## 5 Whys: [Bug Title]

1. **Why** did [observed failure occur]?
   → Because [immediate cause]

2. **Why** did [immediate cause] happen?
   → Because [deeper cause]

3. **Why** did [deeper cause] happen?
   → Because [even deeper cause]

4. **Why** did [even deeper cause] happen?
   → Because [near root cause]

5. **Why** did [near root cause] happen?
   → Because [ROOT CAUSE]

**Root Cause:** [Final answer]
```

---

## 🔧 Phase 3: Fix

### Goal: Apply Targeted, Minimal Fix

### Pre-Fix Checklist

```markdown
- [ ] Root cause is identified and documented
- [ ] Hypothesis has been tested and confirmed
- [ ] Understand the full impact of the fix
- [ ] Fix addresses root cause, not just symptom
- [ ] Have a test that will prove the fix works
```

### Fix Quality Criteria

| Criterion      | Description                             |
| -------------- | --------------------------------------- |
| **Targeted**   | Changes only what's necessary           |
| **Root-Cause** | Fixes the cause, not the symptom        |
| **Safe**       | Doesn't introduce new bugs              |
| **Readable**   | Future developers can understand why    |
| **Testable**   | Can verify it works with automated test |

### Fix Documentation

```markdown
## Fix Applied

**Root Cause:** [What was actually wrong]

**Solution:** [What change was made]

**Files Modified:**

- `path/to/file.ts` - [Description of change]

**Why This Fix:**

- [Rationale for this approach]

**Alternative Considered:**

- [Other option] - Not chosen because [reason]

**Risk Assessment:**

- [Low/Medium/High] - [Justification]
```

### Common Fix Patterns

| Bug Type         | Fix Pattern                             |
| ---------------- | --------------------------------------- |
| Null reference   | Add null check + handle gracefully      |
| Race condition   | Add synchronization/locking             |
| Off-by-one       | Adjust boundary condition               |
| State corruption | Reset or validate state at entry points |
| Memory leak      | Ensure resources are cleaned up         |
| Timeout          | Adjust timeout + add retry logic        |

---

## ✅ Phase 4: Verify

### Goal: Confirm Fix Works, Prevent Regression

### Verification Checklist

```markdown
## Verification Steps

### Immediate Verification

- [ ] Original reproduction steps no longer trigger bug
- [ ] Automated test for this bug passes
- [ ] Related functionality still works
- [ ] No new warnings/errors introduced

### Regression Prevention

- [ ] Unit test added for the specific case
- [ ] Edge cases tested
- [ ] Integration tests pass
- [ ] Code reviewed by another person

### Documentation

- [ ] Root cause documented (for future learning)
- [ ] Commit message explains the fix
- [ ] Ticket/issue updated with resolution
```

### Test Case Template

```markdown
## Regression Test: [Bug ID/Title]

**Purpose:** Prevent recurrence of [bug description]

**Test:**
```

// Test code or test case description
expect(buggyFunction(problematicInput)).toBe(correctOutput);

```

**Covers:**
- [x] The exact failure case
- [x] Similar edge cases: [list them]
```

### Rollback Strategy

```markdown
## Rollback Plan

**If fix causes issues:**

1. Revert commit: `git revert [commit-hash]`
2. Deploy previous version
3. Notify stakeholders
4. Document what went wrong with fix

**Monitoring:**

- [What metrics to watch]
- [Alert thresholds]
- [Duration of elevated monitoring]
```

---

## 🛠️ Debugging Tools & Techniques

### Tool Selection Guide

| Situation              | Tool/Technique | Command/Usage                      |
| ---------------------- | -------------- | ---------------------------------- |
| Find when bug appeared | Git Bisect     | `git bisect start; git bisect bad` |
| Trace execution path   | Debugger       | Set breakpoints, step through      |
| Find pattern in code   | Grep/Ripgrep   | `rg "pattern" --type ts`           |
| Profile performance    | Profiler       | Chrome DevTools, `node --prof`     |
| Monitor network        | Network tab    | Check request/response             |
| Find recent changes    | Git log/blame  | `git log -p --since="2 days ago"`  |

### Strategic Logging

```typescript
// Good: Context-rich, actionable logs
logger.debug("Processing order", {
  orderId,
  userId,
  itemCount: items.length,
  totalAmount,
});

// Bad: Vague, unhelpful
console.log("here"); // ❌
console.log(data); // ❌ No context
```

### Binary Search Debugging

```
Step 1: Identify a working point and broken point
Step 2: Test the midpoint
Step 3: If midpoint works → bug is after
        If midpoint broken → bug is before
Step 4: Repeat until bug location is isolated
```

---

## 🚨 Anti-Patterns

| ❌ Don't                   | ✅ Do                                       |
| -------------------------- | ------------------------------------------- |
| Change random things       | Test one hypothesis at a time               |
| Fix the symptom            | Find and fix root cause                     |
| Skip reproduction          | Establish reliable repro first              |
| Hope it's fixed            | Verify with tests                           |
| Fix and forget             | Document and add regression test            |
| Debug in production        | Reproduce in safe environment when possible |
| Remove code until it works | Understand why code was there               |
| Assume the obvious cause   | Test each hypothesis with evidence          |

---

## 📋 Debugging Session Template

```markdown
# Debug Session: [Issue Title]

**Date:** YYYY-MM-DD
**Status:** 🔄 In Progress | ✅ Resolved | ❌ Blocked

---

## Symptoms

[What's happening]

## Reproduction

[Steps to reproduce reliably]

---

## Diagnosis

### Hypothesis 1: [Title]

- **Test:** [How to test]
- **Result:** ❌ Refuted / ✅ Confirmed

### Hypothesis 2: [Title]

- **Test:** [How to test]
- **Result:** ❌ Refuted / ✅ Confirmed

---

## Root Cause

[What is actually wrong and why it causes the symptom]

---

## Fix

[What was changed]

---

## Verification

- [ ] Reproduction no longer triggers bug
- [ ] Regression test added
- [ ] Related functionality verified

---

## Lessons Learned

[What can prevent similar bugs in the future]
```

---

## 🔗 Related Skills

| Need                     | Skill              |
| ------------------------ | ------------------ |
| Understanding before fix | `brainstorming`    |
| Planning complex fixes   | `plan-writing`     |
| Writing regression tests | `testing-patterns` |
| Clean fix code           | `clean-code`       |

---

> **Remember:** The most expensive bugs are those that keep coming back. Invest in understanding the root cause, and your fix will stick.
