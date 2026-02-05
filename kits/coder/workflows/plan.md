---
description: Create project plan using project-planner agent. No code writing - only plan file generation.
---

# /plan - Project Planning Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "plan", "lập kế hoạch", "create plan", "make a plan for", or `/plan`

## Agent

Route to `project-planner` agent

---

## 🔴 Critical Rules

1. **NO CODE WRITING** - This workflow creates plan file ONLY
2. **Use project-planner agent** - Follow 4-phase methodology
3. **Socratic Gate** - Ask clarifying questions BEFORE planning
4. **Dynamic Naming** - Plan file named based on task

---

## Workflow

### Phase 1: Context Check

Understand the user's request:

- What is being planned?
- Is this a new project or feature addition?
- Any constraints mentioned?

### Phase 2: Socratic Gate

Ask minimum 3 clarifying questions:

```markdown
Before I create the plan, I need to understand:

1. **Scope**: What are the main features/requirements?
2. **Users**: Who is the target audience?
3. **Tech**: Any technology preferences or constraints?
```

Wait for user response before proceeding.

### Phase 3: Planning

Using `project-planner` agent, create plan with:

- Task breakdown (WBS)
- Dependencies and ordering
- Agent assignments
- Verification checklist

**Dynamic Naming Convention:**

| Rule                        | Example                  |
| --------------------------- | ------------------------ |
| Extract 2-3 key words       | "e-commerce cart"        |
| Lowercase, hyphen-separated | `ecommerce-cart`         |
| Max 30 characters           | `PLAN-ecommerce-cart.md` |

Output file: `docs/PLAN-{task-slug}.md`

### Phase 4: Report

Report to user:

```markdown
✅ **Plan Created:** `docs/PLAN-{slug}.md`

**Contents:**

- [ ] Requirements analysis
- [ ] Task breakdown
- [ ] Agent assignments
- [ ] Verification checklist

**Next Steps:**

- Review the plan
- Run `/create` to start implementation
- Or modify plan manually
```

---

## Expected Output

| Deliverable            | Location                   |
| ---------------------- | -------------------------- |
| Project Plan           | `docs/PLAN-{task-slug}.md` |
| Task Breakdown         | Inside plan file           |
| Agent Assignments      | Inside plan file           |
| Verification Checklist | Phase X in plan file       |

---

## Naming Examples

| Request                           | Plan File                     |
| --------------------------------- | ----------------------------- |
| `/plan e-commerce site with cart` | `docs/PLAN-ecommerce-cart.md` |
| `/plan mobile app for fitness`    | `docs/PLAN-fitness-app.md`    |
| `/plan add dark mode feature`     | `docs/PLAN-dark-mode.md`      |
| `/plan fix authentication bug`    | `docs/PLAN-auth-fix.md`       |
| `/plan SaaS dashboard`            | `docs/PLAN-saas-dashboard.md` |

---

## Exit Conditions

- ✅ **Success:** Plan file created in `docs/` directory
- ❌ **Failure:** User cancels or requirements too vague after 3 attempts
- ⚠️ **Warning:** Partial plan due to incomplete information

---

## Usage

```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
/plan thêm tính năng dark mode
```
