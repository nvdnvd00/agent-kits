---
description: Create new application from scratch. Triggers app-builder skill with multi-agent orchestration.
---

# /create - Application Creation Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "create", "build", "tạo", "make", "new app", or `/create`

## Agent

Route to `orchestrator` agent → coordinates specialists

---

## 🔴 Critical Rules

1. **Socratic Gate First** - Do NOT start building without understanding requirements
2. **Plan Before Code** - Create or reference a plan before implementation
3. **Multi-Agent** - Orchestrate specialists for each domain
4. **Preview at End** - Start dev server and provide URL

---

## Workflow

### Phase 1: Request Analysis

Understand user's request:

```markdown
## Request Analysis

- **Type**: Web app / Mobile app / API / CLI
- **Core Features**: [List main features]
- **Stack**: [Inferred or specified tech stack]
- **Complexity**: Simple / Medium / Complex
```

If unclear, ask:

```markdown
Before I start building, I need to understand:

1. **Type**: What kind of application? (Web/Mobile/API)
2. **Features**: What are the 3 most important features?
3. **Users**: Who will use this application?
```

### Phase 2: Project Planning

Two options:

| Condition   | Action                                    |
| ----------- | ----------------------------------------- |
| Plan exists | Read `docs/PLAN-*.md`                     |
| No plan     | Create brief plan using `project-planner` |

Determine:

- Tech stack selection
- File structure
- Component breakdown
- API design (if applicable)

### Phase 3: Orchestrated Building

Coordinate specialists:

```markdown
## Agent Assignments

| Agent                 | Task                |
| --------------------- | ------------------- |
| `database-specialist` | Schema design       |
| `backend-specialist`  | API implementation  |
| `frontend-specialist` | UI components       |
| `devops-engineer`     | Config & deployment |
```

Build order:

1. Database schema → 2. Backend API → 3. Frontend UI → 4. Integration

### Phase 4: Testing & Preview

After building:

```bash
# Start development server
pnpm dev
```

### Phase 5: Report

Present to user:

```markdown
✅ **Application Created!**

**Stack:** [Tech stack used]
**Structure:**

- `src/` - Source code
- `api/` - Backend routes
- `components/` - UI components

**Preview:** http://localhost:3000

**Next Steps:**

- Review the code
- Run `/test` to add tests
- Run `/deploy` when ready
```

---

## Tech Stack Decision Framework

| Project Type | Recommended Stack        |
| ------------ | ------------------------ |
| Simple Web   | Vanilla HTML/CSS/JS      |
| React App    | Vite + React + CSS       |
| Full-Stack   | Next.js / Vite + Express |
| Mobile       | React Native / Flutter   |
| API Only     | Express / Hono / Fastify |

---

## Exit Conditions

- ✅ **Success:** App running at localhost with core features
- ❌ **Failure:** User cancels or critical dependency unavailable
- ⚠️ **Warning:** Partial build, some features incomplete

---

## Usage Examples

```
/create blog site
/create e-commerce app with cart
/create todo app
/create Instagram clone
/create CRM với quản lý khách hàng
```
