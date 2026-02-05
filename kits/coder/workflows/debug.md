---
description: Debugging command. Activates DEBUG mode for systematic problem investigation using 4-phase methodology.
---

# /debug - Systematic Debugging Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "debug", "fix", "gỡ lỗi", "investigate", "error", or `/debug`

## Agent

Route to `debugger` agent

---

## 🔴 Critical Rules

1. **Gather Evidence First** - Never guess without information
2. **Form Hypotheses** - Rank by likelihood
3. **Test Systematically** - One variable at a time
4. **Explain Root Cause** - Not just the fix

---

## Workflow

### Phase 1: Information Gathering

Collect all relevant context:

```markdown
## 🔍 Debug Session: [Issue Title]

### Symptom

- What is happening?
- What should happen instead?

### Context

- **Error Message**: `[exact error]`
- **File(s) Affected**: `[file paths]`
- **Line Number(s)**: [if known]
- **Recent Changes**: [what changed before issue appeared]
- **Reproduction Steps**: [how to reproduce]
```

If user provides incomplete info, ask:

```markdown
I need more information to debug effectively:

1. What is the exact error message?
2. How do you reproduce this issue?
3. What was working before?
```

### Phase 2: Hypothesis Formation

Create ranked list of possible causes:

```markdown
### Hypotheses (Ranked by Likelihood)

1. ❓ **High**: [Most likely cause based on symptoms]
2. ❓ **Medium**: [Second possibility]
3. ❓ **Low**: [Less likely cause]
```

### Phase 3: Systematic Investigation

Test each hypothesis:

```markdown
### Investigation

**Testing Hypothesis 1: [Name]**

- Action: [What I checked]
- Result: ✅ Confirmed / ❌ Ruled Out
- Evidence: [Specific finding]

**Testing Hypothesis 2: [Name]**

- Action: [What I checked]
- Result: ✅ Confirmed / ❌ Ruled Out
- Evidence: [Specific finding]
```

Tools to use:

- Add console logs / breakpoints
- Check network requests
- Verify data flow
- Compare with working state

### Phase 4: Fix & Prevent

Apply fix and document:

```markdown
### 🎯 Root Cause

[Clear explanation of WHY this happened]

### Fix Applied

\`\`\`[language]
// Before (broken)
[old code]

// After (fixed)
[new code]
\`\`\`

### Prevention

🛡️ To prevent this in the future:

- [ ] [Specific prevention measure]
- [ ] [Add test case]
- [ ] [Update documentation]
```

### Phase 5: Report

Summarize the debugging session:

```markdown
✅ **Debug Complete**

**Issue:** [Brief description]
**Root Cause:** [One sentence explanation]
**Fix:** [What was changed]

**Files Modified:**

- `[file1]` - [change description]
- `[file2]` - [change description]

**Next Steps:**

- Run tests to verify fix
- Consider adding regression test
```

---

## Output Format Template

```markdown
## 🔍 Debug: [Issue Summary]

### 1. Symptom

[What's happening]

### 2. Information Gathered

| Item  | Value       |
| ----- | ----------- |
| Error | `[message]` |
| File  | `[path]`    |
| Line  | [number]    |

### 3. Hypotheses

1. ❓ [Most likely]
2. ❓ [Second option]
3. ❓ [Less likely]

### 4. Investigation

Testing each hypothesis with evidence...

### 5. Root Cause

🎯 **[Explanation]**

### 6. Fix

[Code changes]

### 7. Prevention

🛡️ [Future safeguards]
```

---

## Exit Conditions

- ✅ **Success:** Root cause identified, fix applied, verified working
- ❌ **Failure:** Unable to reproduce issue or requires external support
- ⚠️ **Warning:** Workaround applied but root cause unclear

---

## Usage Examples

```
/debug login not working
/debug API returns 500 error
/debug form doesn't submit
/debug dữ liệu không lưu được
/debug component not rendering
```

---

## Key Principles

| Principle              | Description                                 |
| ---------------------- | ------------------------------------------- |
| **Ask First**          | Get full error context before investigating |
| **Test Hypotheses**    | Don't guess randomly, be systematic         |
| **Explain Why**        | Document root cause, not just fix           |
| **Prevent Recurrence** | Add tests or validation                     |
