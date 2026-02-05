---
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# /orchestrate - Multi-Agent Coordination Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "orchestrate", "coordinate", "multi-agent", or `/orchestrate`

## Agent

Route to `orchestrator` agent

---

## 🔴 Critical Rules

1. **Minimum 3 Agents** - Orchestration requires 3+ different specialists
2. **2-Phase Execution** - Planning first, then implementation
3. **Context Passing** - Always pass full context to subagents
4. **User Approval** - Get approval before Phase 2

---

## Agent Selection Matrix

| Task Type      | REQUIRED Agents (minimum)                                                 |
| -------------- | ------------------------------------------------------------------------- |
| **Web App**    | frontend-specialist, backend-specialist, test-engineer                    |
| **API**        | backend-specialist, security-auditor, test-engineer                       |
| **UI/Design**  | frontend-specialist, ux-researcher, performance-analyst                   |
| **Database**   | database-specialist, backend-specialist, security-auditor                 |
| **Full Stack** | project-planner, frontend-specialist, backend-specialist, devops-engineer |
| **Debug**      | debugger, test-engineer, performance-analyst                              |
| **Security**   | security-auditor, test-engineer, devops-engineer                          |

---

## Workflow

### Phase 1: Planning (Sequential)

Only these agents allowed during planning:

| Agent             | Purpose              |
| ----------------- | -------------------- |
| `project-planner` | Create PLAN.md       |
| `orchestrator`    | Coordinate and route |

```markdown
## Phase 1: Planning

1. Analyze task domains
2. Create docs/PLAN-{slug}.md
3. Define agent assignments
4. Wait for user approval
```

### ⏸️ CHECKPOINT: User Approval

After plan is created, ask:

```markdown
✅ **Plan created:** `docs/PLAN-{slug}.md`

Proceed with implementation? (Y/N)

- Y: Start Phase 2 with multiple agents
- N: Modify plan first
```

🔴 **DO NOT proceed to Phase 2 without explicit approval!**

### Phase 2: Implementation (Parallel)

After approval, invoke agents in parallel groups:

| Group          | Agents                                  | Tasks                    |
| -------------- | --------------------------------------- | ------------------------ |
| **Foundation** | database-specialist, security-auditor   | Schema, security review  |
| **Core**       | backend-specialist, frontend-specialist | API, UI implementation   |
| **Polish**     | test-engineer, devops-engineer          | Tests, deployment config |

### Phase 3: Verification

Last agent runs verification:

```bash
# Run security scan
python .agent/skills/security-fundamentals/scripts/security_scan.py .

# Run linting
pnpm lint

# Run tests
pnpm test
```

### Phase 4: Synthesis

Combine all agent outputs into unified report.

---

## Context Passing Protocol (MANDATORY)

When invoking ANY subagent, include:

```markdown
## CONTEXT for [Agent Name]

**Original Request:** [Full user request]
**Decisions Made:** [All answers to Socratic questions]
**Previous Agent Work:** [Summary of completed work]
**Current Plan:** [Reference to PLAN.md if exists]

**YOUR TASK:** [Specific task for this agent]
```

⚠️ **VIOLATION:** Invoking agent without context = wrong assumptions!

---

## Output Format

```markdown
## 🎼 Orchestration Report

### Task

[Original task summary]

### Agents Invoked (MINIMUM 3)

| #   | Agent               | Focus Area         | Status |
| --- | ------------------- | ------------------ | ------ |
| 1   | project-planner     | Task breakdown     | ✅     |
| 2   | frontend-specialist | UI implementation  | ✅     |
| 3   | backend-specialist  | API implementation | ✅     |
| 4   | test-engineer       | Verification       | ✅     |

### Phase 1: Planning

- [x] PLAN.md created
- [x] User approved plan

### Phase 2: Implementation

- [x] Database schema designed
- [x] API endpoints implemented
- [x] UI components built
- [x] Tests written

### Phase 3: Verification

- [x] Security scan passed
- [x] Lint check passed
- [x] All tests passing

### Key Findings

1. **project-planner**: Identified 12 tasks across 4 domains
2. **frontend-specialist**: Created 8 reusable components
3. **backend-specialist**: Implemented 15 API endpoints
4. **test-engineer**: Added 45 test cases

### Deliverables

| Deliverable | Location              |
| ----------- | --------------------- |
| Plan        | `docs/PLAN-{slug}.md` |
| API         | `src/api/`            |
| UI          | `src/components/`     |
| Tests       | `tests/`              |

### Summary

[One paragraph synthesis of all agent work]
```

---

## Exit Gate

Before completing orchestration, verify:

| Check            | Requirement                    |
| ---------------- | ------------------------------ |
| ✅ Agent Count   | `invoked_agents >= 3`          |
| ✅ Plan Approved | User said Y to proceed         |
| ✅ Verification  | At least one scan/test ran     |
| ✅ Report        | Orchestration report generated |

If any check fails → DO NOT complete. Invoke more agents or run verification.

---

## Available Agents (19)

### Tier 1: Master

- `orchestrator`, `project-planner`, `debugger`

### Tier 2: Development

- `frontend-specialist`, `backend-specialist`, `mobile-developer`
- `database-specialist`, `devops-engineer`

### Tier 3: Quality

- `security-auditor`, `code-reviewer`, `test-engineer`, `performance-analyst`

### Tier 4: Domain

- `realtime-specialist`, `multi-tenant-architect`, `queue-specialist`, `integration-specialist`

### Tier 5: Support

- `documentation-writer`, `i18n-specialist`, `ux-researcher`

---

## Exit Conditions

- ✅ **Success:** 3+ agents invoked, plan approved, verification passed, report generated
- ❌ **Failure:** Fewer than 3 agents, user rejected plan, verification failed
- ⚠️ **Warning:** Completed but with verification warnings

---

## Usage Examples

```
/orchestrate build e-commerce site
/orchestrate full security audit
/orchestrate refactor with tests
/orchestrate xây dựng API cho mobile app
```
