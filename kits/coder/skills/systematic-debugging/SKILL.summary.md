---
name: systematic-debugging
summary: true
description: "4-phase debugging methodology. For quick ref — load SKILL.md for full templates and technique guides."
---

# Systematic Debugging — Summary

> ⚡ Quick ref. Load full `SKILL.md` for detailed phase templates and debugging session docs.

## 4-Phase Workflow
```
1. REPRODUCE → reliable repro >90% · minimum steps · note env
2. DIAGNOSE  → hypothesize → predict → test → one variable at a time
3. FIX       → target root cause (not symptom) · minimal change
4. VERIFY    → repro no longer triggers · regression test added
```

## Core Rule
```
❌ Change random things → hope it works
✅ Observe → Hypothesize → Predict → Test (scientific method)
```

## Evidence Techniques
- **Logs**: add strategic logging at decision points (structured, with context)
- **Breakpoints**: conditional breakpoints at state inspection points
- **Binary search**: comment out half the code to narrow location
- **git bisect**: find exact commit that introduced the bug
- **5 Whys**: ask WHY 5 times to reach root cause

## Root Cause Categories
Logic Error · State Problem · Data Issue · Integration · Resource · Configuration

## Anti-Patterns
- Fix the symptom (not root cause) → bug recurs
- Skip reproduction → debugging is guessing
- Change multiple things at once → can't isolate cause
- Forget regression test → bug comes back

> Load full SKILL.md for: hypothesis documentation template, debugging session template, tool selection guide, 5 Whys format, rollback strategy
