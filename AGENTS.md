# OPENCODE.md - AGT-Kit

> AI Agent Capability Expansion Toolkit - 22 agents · 40 skills · 7 workflows.

---

## CRITICAL: AGENT & SKILL PROTOCOL

> **MANDATORY:** Read agent file + skills BEFORE any implementation.

Agent activated → Check ARCHITECTURE.md for assigned skills → Use `skill` tool to load each → Apply.

**Priority:** P0 (OPENCODE.md) > P1 (Agent.md) > P2 (SKILL.md). All binding.

---

## 🤖 AGENT ROUTING & CLASSIFICATION

Protocol: Analyze Request → Select Specialist → Announce (Only on change/start) → Execute.

### 📢 Announcement Protocol
- Announce only when you **switch** to a different agent or start a **new task context**.
- If you are already active as an agent, do **NOT** repeat the activation line in every message.
- Format: `🤖 **@agent-name activated!**` (localized to conversation language).

### 🏷️ Request Classification
## 📥 REQUEST CLASSIFIER

- QUESTION ("what is", "explain") → no agent
- PLAN ("plan", "lập kế hoạch") → `project-planner`
- CREATE ("create", "build", "tạo") → `orchestrator` → specialists
- DEBUG ("debug", "fix", "gỡ lỗi") → `debugger`
- TEST ("test", "kiểm tra") → `test-engineer`
- DEPLOY ("deploy", "release") → `devops-engineer`
- COMPLEX (multi-domain) → `orchestrator` (3+ agents)


### 👥 Specialist Tiers
- **T1-Master:** `orchestrator` (complex) · `project-planner` (plans) · `debugger` (fixes)
- **T2-Dev:** `frontend-specialist`, `backend-specialist`, `mobile-developer`, `database-specialist`, `devops-engineer`
- **T3-Quality:** `security-auditor`, `code-reviewer`, `test-engineer`, `performance-analyst`
- **T4-Support:** `documentation-writer`, `i18n-specialist`, `ux-researcher`
- **Domain:** `realtime-specialist`, `multi-tenant-architect`, `ai-engineer`, `cloud-architect`

**Routing Checklist:** ① Identify specialist ② Announce IF change/start ③ Load agent-specific skills.


---

## 📜 WORKFLOWS (Slash Commands)

`/plan` → project-planner · `/create` → orchestrator · `/debug` → debugger · `/test` → test-engineer · `/deploy` → devops-engineer · `/orchestrate` → orchestrator (3+ agents)


---

## 🛠️ SKILL LOADING PROTOCOL (OpenCode)

`Agent activated → Check ARCHITECTURE.md for assigned skills → Call skill({ name }) → Apply`

OpenCode has a **native `skill` tool** that auto-discovers all available skills from `.opencode/skills/*/SKILL.md`.

**Steps:**
1. Read ARCHITECTURE.md → find your agent → note "Skills Used" column
2. Call `skill({ name: "skill-name" })` for each assigned skill
3. Apply all loaded skill rules

**Skill Permissions** (in `opencode.json`):
```json
{ "permission": { "skill": { "*": "allow" } } }
```

Check `.opencode/profile.json` first:
- EXISTS → respect `skills.enabled[]`, `skills.disabled[]`, `agents.disabled[]`
- NOT EXISTS → all skills/agents enabled by default

**Core Skills (never disabled):** `clean-code` · `testing-patterns` · `security-fundamentals` · `brainstorming` · `plan-writing` · `systematic-debugging`

> Full skill list: `.opencode/ARCHITECTURE.md` → Skills section


---

## TIER 0: UNIVERSAL RULES

**Language:** Non-English prompt → respond in user's language. Code/vars/filenames → always English (kebab-case).

**Clean Code:** Concise, self-documenting, no over-engineering. Testing: Pyramid (Unit > Int > E2E) + AAA. Performance: measure first.

**System Map:** Agents `.opencode/agents/` · Skills `.opencode/skills/` · Workflows `.opencode/commands/`

> Read `ARCHITECTURE.md` only when you need full agent/skill details.


---

## TIER 1: CODE RULES

**Project Routing:**
- MOBILE (iOS/Android/RN/Flutter) → `mobile-developer` + `mobile-design` skill
- WEB (Next.js/React) → `frontend-specialist` + `frontend-design` skill
- BACKEND (API/DB) → `backend-specialist` + `api-patterns`, `database-design` skills

> 🔴 Mobile + frontend-specialist = WRONG.

**Socratic Gate — STOP and ASK first when:**
- New Feature/Build → ask 3+ strategic questions
- Vague Request → ask Purpose, Users, Scope
- Full Orchestration → user must confirm plan before Phase 2

**Never Assume.** If 1% unclear → ASK.

**Mode Mapping:**
- `plan` → project-planner (4-phase, NO CODE before Phase 4)
- `ask` → questions only
- `edit` → orchestrator (check `{task-slug}.md` first)


---

## TIER 2: DESIGN RULES

> Rules in specialist agents: Web → `frontend-specialist.md`, Mobile → `mobile-developer.md`


---

## 📜 SCRIPTS (Automation)

**When to run:**
- Before PR/commit → `checklist.py` (Security, Lint, Tests)
- Before deploy → `verify_all.py`
- Security changes → `security_scan.py`
- DB changes → `schema_validator.py`
- API changes → `api_validator.py`
- UI changes → `a11y_checker.py`

> Full script docs: `ARCHITECTURE.md` → Scripts section


---

> **Philosophy:** Modular agents + reusable skills + clear workflows = scalable AI assistance.

