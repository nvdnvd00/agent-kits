---
name: plan-writing
description: Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work. Covers WBS, task decomposition, estimation, and plan file formats.
allowed-tools: Read, Write, Edit
---

# Plan Writing - Structured Task Decomposition

> **Philosophy:** A good plan is a roadmap that prevents wrong turns. Break down before building up.

---

## 🎯 Core Principle: Decompose → Estimate → Verify

```
❌ WRONG: "I'll implement the feature" → Jump into code
✅ CORRECT: "I'll implement the feature" → Break into tasks → Estimate each → Define done criteria → Then code
```

**The Planning Approach:**

- Break large work into independently completable units
- Identify dependencies before they block you
- Define "done" clearly for each task
- Enable progress tracking and estimation

---

## 📋 When to Write a Plan

### Decision Matrix

| Work Type                | Estimated Effort | Action              |
| ------------------------ | ---------------- | ------------------- |
| Single file edit         | < 30 min         | Just do it          |
| Multi-file change        | 30 min - 2 hours | Mental checklist    |
| New feature              | > 2 hours        | **Write plan file** |
| Architecture change      | Any              | **Write plan file** |
| Multi-component refactor | Any              | **Write plan file** |

### Plan Required When:

- Changes span 3+ files
- Multiple developers involved
- User needs visibility into progress
- Work can be interrupted and resumed
- Trade-offs need documentation

---

## 🔢 Task Breakdown Structure

### Hierarchy Levels

```
Level 1: Epic/Feature (What we're building)
   ↓
Level 2: Major Components (Logical groupings)
   ↓
Level 3: Tasks (Completable units)
   ↓
Level 4: Subtasks (If task is still too large)
```

### Task Sizing Guidelines

| Task Duration    | Status     | Action Needed              |
| ---------------- | ---------- | -------------------------- |
| < 15 min         | Too small  | Merge with related tasks   |
| 15 min - 4 hours | Ideal      | Perfect granularity        |
| 4 - 8 hours      | Acceptable | Consider splitting         |
| > 8 hours        | Too large  | **Must decompose further** |

### Good Task Characteristics

| Characteristic      | Description                                       |
| ------------------- | ------------------------------------------------- |
| **Observable**      | Has visible output when complete                  |
| **Verifiable**      | Clear criteria to confirm done                    |
| **Independent**     | Minimal dependencies blocking start               |
| **Sized correctly** | 15 min to 4 hours                                 |
| **Named clearly**   | Action verb + object (e.g., "Create user schema") |

---

## 📝 Plan File Template

### File Naming Convention

```
.agent/plans/{task-slug}.md      # Standard location
{task-slug}-plan.md              # Alternative in root
```

**Slug format:** `feature-name` or `YYYYMMDD-feature-name`

### Template Structure

```markdown
# Plan: [Feature/Task Name]

> **Goal:** One-sentence summary of what success looks like
> **Status:** 🟡 In Progress | ✅ Complete | ⏸️ Blocked
> **Updated:** YYYY-MM-DD

---

## Overview

[2-3 sentences on what this plan covers and why]

---

## Tasks

### Phase 1: [Phase Name]

- [ ] **Task 1.1:** [Description]
  - Files: `path/to/file.ts`
  - Depends on: -
  - Estimate: 30m
  - Done when: [Verification criteria]

- [ ] **Task 1.2:** [Description]
  - Files: `path/to/file.ts`, `path/to/other.ts`
  - Depends on: Task 1.1
  - Estimate: 1h
  - Done when: [Verification criteria]

### Phase 2: [Phase Name]

- [ ] **Task 2.1:** [Description]
  - Depends on: Phase 1 complete
  - Estimate: 45m
  - Done when: [Verification criteria]

---

## Dependencies

| Dependency     | Type     | Status   |
| -------------- | -------- | -------- |
| [External API] | External | ✅ Ready |
| [Task 1.1]     | Internal | 🔄 WIP   |

---

## Risks & Mitigations

| Risk              | Impact | Mitigation      |
| ----------------- | ------ | --------------- |
| [Potential issue] | High   | [How to handle] |

---

## Decisions Log

| Date       | Decision           | Rationale |
| ---------- | ------------------ | --------- |
| YYYY-MM-DD | [What was decided] | [Why]     |

---

## Progress Log

- **[YYYY-MM-DD]:** [What was accomplished]
- **[YYYY-MM-DD]:** [What was accomplished]
```

---

## ⏱️ Estimation Framework

### Estimating Tasks

| Confidence Level | Multiplier | When to Apply                      |
| ---------------- | ---------- | ---------------------------------- |
| **High**         | 1.2x       | Done similar work before           |
| **Medium**       | 1.5x       | Understand approach, some unknowns |
| **Low**          | 2-3x       | New territory, many unknowns       |

### Estimation Checklist

Before estimating, consider:

- [ ] Implementation time (actual coding)
- [ ] Testing and verification time
- [ ] Edge case handling
- [ ] Documentation/comments
- [ ] Code review and revisions
- [ ] Integration testing

### Common Estimation Mistakes

| ❌ Underestimates           | ✅ Include In Estimate         |
| --------------------------- | ------------------------------ |
| "Just wire things together" | Integration complexity         |
| "Tests are quick"           | Edge cases and debugging tests |
| "I know this codebase"      | Context switching overhead     |
| "Simple fix"                | Regression testing             |

---

## 🔗 Dependency Mapping

### Dependency Types

| Type         | Description                       | Example                 |
| ------------ | --------------------------------- | ----------------------- |
| **Blocking** | Cannot start until complete       | Schema before API       |
| **Soft**     | Can start, but need before finish | Tests before merge      |
| **External** | Outside your control              | API access, approval    |
| **Resource** | Limited availability              | Shared test environment |

### Dependency Visualization

```
Task A ──┬──> Task C ──> Task E
         │
Task B ──┘
              Task D ──> Task F (independent track)
```

### Handling Blocked Tasks

When blocked:

1. Document the blocker explicitly
2. Identify tasks that can proceed
3. Communicate blocker to stakeholders
4. Set reminder to check blocker status

---

## ✅ Verification Criteria

### "Done" Definition Framework

```markdown
A task is DONE when:

1. [ ] Code is written and compiles
2. [ ] Tests pass (unit + integration)
3. [ ] Edge cases handled
4. [ ] Documentation updated (if needed)
5. [ ] Code reviewed (if required)
6. [ ] Meets acceptance criteria
```

### Writing Good Verification Criteria

| ❌ Vague          | ✅ Specific                                    |
| ----------------- | ---------------------------------------------- |
| "Works correctly" | "Returns 200 for valid input, 400 for invalid" |
| "Tested"          | "Unit tests cover happy path + 3 error cases"  |
| "Integrated"      | "API called successfully from frontend"        |
| "Complete"        | "All checklist items verified"                 |

---

## 🔄 Plan Maintenance

### When to Update Plan

| Event               | Update Required                    |
| ------------------- | ---------------------------------- |
| Task completed      | Check off, add to progress log     |
| Blocker discovered  | Add to dependencies, update status |
| Scope change        | Revise tasks, re-estimate          |
| New information     | Update risks/decisions log         |
| End of work session | Mark current progress              |

### Plan Review Frequency

| Project Duration | Review Frequency           |
| ---------------- | -------------------------- |
| < 1 day          | Start and end              |
| 1-3 days         | Daily                      |
| > 3 days         | Daily + weekly deep review |

---

## 🚨 Anti-Patterns

| ❌ Don't                    | ✅ Do                                |
| --------------------------- | ------------------------------------ |
| Giant monolithic tasks      | Break into 15min-4hr chunks          |
| "It depends on everything"  | Map only true blocking dependencies  |
| Estimate without buffers    | Apply confidence multiplier          |
| Skip verification criteria  | Define "done" for every task         |
| Never update the plan       | Update as you learn                  |
| Plan at wrong granularity   | Match plan detail to project size    |
| Plan replaces communication | Plan supplements communication       |
| Over-plan simple work       | Use judgment on when plans add value |

---

## 📋 Quick Reference: Task Naming

### Good Task Names

| Format                | Examples                           |
| --------------------- | ---------------------------------- |
| `Create [thing]`      | Create user authentication schema  |
| `Implement [feature]` | Implement password reset flow      |
| `Update [existing]`   | Update API error handling          |
| `Add [capability]`    | Add email validation to signup     |
| `Remove [deprecated]` | Remove legacy auth endpoints       |
| `Fix [issue]`         | Fix timezone conversion bug        |
| `Migrate [from → to]` | Migrate users table to new schema  |
| `Test [component]`    | Test payment processing edge cases |
| `Document [topic]`    | Document API authentication flow   |

---

## 📊 Plan Quality Checklist

Before starting implementation:

```markdown
## Plan Review

### Structure

- [ ] All tasks are 15min-4hr sized
- [ ] Dependencies are clearly mapped
- [ ] Phases/milestones are defined

### Clarity

- [ ] Each task has clear done criteria
- [ ] No ambiguous task descriptions
- [ ] Files affected are identified

### Feasibility

- [ ] Estimates include buffer
- [ ] Blockers are acknowledged
- [ ] Risks are documented

### Ready?

- [ ] Plan is saved in accessible location
- [ ] Stakeholders have visibility (if needed)
```

---

## 🔗 Related Skills

| Need                      | Skill                  |
| ------------------------- | ---------------------- |
| Discovery before planning | `brainstorming`        |
| Debugging with structure  | `systematic-debugging` |
| Clean implementation      | `clean-code`           |
| API task breakdown        | `api-patterns`         |

---

> **Remember:** Plans are living documents. The goal isn't a perfect plan—it's enough structure to build confidently while adapting to reality.
