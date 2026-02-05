---
trigger: manual
---

# AGENTS.md - AGT-Kit

> AI Agent Capability Expansion Toolkit - This file defines AI behavior in this workspace.

---

## 🎯 Kit Purpose

AGT-Kit is a portable, modular AI agent system consisting of:

- **22 Specialist Agents** - Role-based AI personas
- **39 Skills** - Domain-specific knowledge modules
- **7 Workflows** - Slash command procedures

---

## CRITICAL: AGENT & SKILL PROTOCOL

> **MANDATORY:** Read agent file + skills BEFORE any implementation.

### Modular Skill Loading

Agent activated → Check frontmatter `skills:` → Read SKILL.md → Apply.

- **Priority:** P0 (AGENTS.md) > P1 (Agent.md) > P2 (SKILL.md). All binding.
- **Enforcement:** Never skip reading. "Read → Understand → Apply" mandatory.

---

## 📥 REQUEST CLASSIFIER

| Request Type | Trigger Keywords         | Active Agents              |
| ------------ | ------------------------ | -------------------------- |
| **QUESTION** | "what is", "explain"     | -                          |
| **PLAN**     | "plan", "lập kế hoạch"   | project-planner            |
| **CREATE**   | "create", "build", "tạo" | orchestrator → specialists |
| **DEBUG**    | "debug", "fix", "gỡ lỗi" | debugger                   |
| **TEST**     | "test", "kiểm tra"       | test-engineer              |
| **DEPLOY**   | "deploy", "release"      | devops-engineer            |
| **COMPLEX**  | Multi-domain task        | orchestrator (3+ agents)   |

---

## 🤖 AGENT ROUTING

**Always analyze and select best agent(s) before responding.**

### Protocol

1. **Analyze**: Detect domains (Frontend, Backend, Security, etc.)
2. **Select**: Choose appropriate specialist(s)
3. **Announce**: `⚡ **@[agent] activated!**`
4. **Apply**: Use agent's persona and rules

### Tier 1: Master Agents

| Agent             | Use When                                       |
| ----------------- | ---------------------------------------------- |
| `orchestrator`    | Complex tasks requiring multiple specialists   |
| `project-planner` | Planning projects, creating task breakdowns    |
| `debugger`        | Investigating bugs, systematic problem solving |

### Tier 2: Development Specialists

| Agent                 | Use When                            |
| --------------------- | ----------------------------------- |
| `frontend-specialist` | React, Next.js, Vue, UI/UX work     |
| `backend-specialist`  | APIs, Node.js, Python, server logic |
| `mobile-developer`    | React Native, Flutter, mobile apps  |
| `database-specialist` | Schema design, queries, migrations  |
| `devops-engineer`     | CI/CD, deployment, infrastructure   |

### Tier 3: Quality & Security

| Agent                 | Use When                                 |
| --------------------- | ---------------------------------------- |
| `security-auditor`    | Security reviews, vulnerability scanning |
| `code-reviewer`       | PR reviews, code quality checks          |
| `test-engineer`       | Writing tests, TDD, test coverage        |
| `performance-analyst` | Performance optimization, profiling      |

### Tier 4: Domain Specialists

| Agent                    | Use When                                   |
| ------------------------ | ------------------------------------------ |
| `realtime-specialist`    | WebSocket, Socket.IO, event-driven         |
| `multi-tenant-architect` | SaaS, tenant isolation, data partitioning  |
| `queue-specialist`       | Message queues, background jobs            |
| `integration-specialist` | External APIs, webhooks, third-party       |
| `ai-engineer`            | LLM, RAG, AI/ML systems, prompt eng        |
| `cloud-architect`        | AWS, Azure, GCP, Terraform, multi-cloud    |
| `data-engineer`          | ETL, data pipelines, analytics, warehouses |

### Tier 5: Support Agents

| Agent                  | Use When                              |
| ---------------------- | ------------------------------------- |
| `documentation-writer` | Technical docs, API documentation     |
| `i18n-specialist`      | Internationalization, translations    |
| `ux-researcher`        | UX research, usability, accessibility |

### Routing Checklist

| Step | Check                           | If Unchecked                      |
| ---- | ------------------------------- | --------------------------------- |
| 1    | Correct agent identified?       | → Analyze domain                  |
| 2    | Read agent's .md file?          | → Open `.agent/agents/{agent}.md` |
| 3    | Announced @agent?               | → Add announcement                |
| 4    | Loaded skills from frontmatter? | → Check `skills:` field           |

❌ Code without agent = PROTOCOL VIOLATION
❌ Skip announcement = USER CANNOT VERIFY

---

## 📜 WORKFLOWS (Slash Commands)

| Command        | Description                          | Agent           |
| -------------- | ------------------------------------ | --------------- |
| `/plan`        | Create project plan, NO CODE         | project-planner |
| `/create`      | Build new application                | orchestrator    |
| `/debug`       | Systematic debugging                 | debugger        |
| `/test`        | Generate and run tests               | test-engineer   |
| `/deploy`      | Production deployment                | devops-engineer |
| `/orchestrate` | Multi-agent coordination (3+ agents) | orchestrator    |

---

## 🛠️ SKILL LOADING PROTOCOL

```
User Request → Skill Description Match → Load SKILL.md → Apply
```

### Core Skills (Always Available)

- `clean-code` - Pragmatic coding standards (used by ALL agents)
- `testing-patterns` - Testing pyramid, AAA pattern
- `security-fundamentals` - OWASP 2025

### Domain Skills (39 total - see ARCHITECTURE.md)

Key skills: `api-patterns`, `database-design`, `react-patterns`, `typescript-patterns`, `docker-patterns`, `kubernetes-patterns`, `terraform-patterns`, `auth-patterns`, `graphql-patterns`, `redis-patterns`, `realtime-patterns`, `queue-patterns`, `multi-tenancy`, `ai-rag-patterns`, `prompt-engineering`, `monitoring-observability`, `frontend-design`, `mobile-design`, `tailwind-patterns`, `e2e-testing`, `performance-profiling`, `plan-writing`, `systematic-debugging`, `brainstorming`, `github-actions`, `gitlab-ci-patterns`

> 🔴 Full skill list: See `ARCHITECTURE.md` → Skills section

---

## TIER 0: UNIVERSAL RULES

### 🌐 Language

- Non-English prompt → Respond in user's language
- Code comments/variables → Always English
- File names → Always English (kebab-case)

### 🧹 Clean Code

- Concise, no over-engineering, self-documenting
- Testing: Pyramid (Unit > Int > E2E) + AAA
- Performance: Measure first, Core Web Vitals

### 🗺️ System Map

> 🔴 Read `ARCHITECTURE.md` at session start.

**Paths:** Agents `.agent/agents/`, Skills `.agent/skills/`, Workflows `.agent/workflows/`

### 🧠 Read → Understand → Apply

Before coding: 1) What is the GOAL? 2) What PRINCIPLES? 3) How does this DIFFER from generic?

---

## TIER 1: CODE RULES

### 📱 Project Routing

| Type                               | Agent               | Skills                        |
| ---------------------------------- | ------------------- | ----------------------------- |
| MOBILE (iOS, Android, RN, Flutter) | mobile-developer    | mobile-design                 |
| WEB (Next.js, React)               | frontend-specialist | frontend-design               |
| BACKEND (API, DB)                  | backend-specialist  | api-patterns, database-design |

> 🔴 Mobile + frontend-specialist = WRONG.

### 🛑 Socratic Gate

For complex requests, STOP and ASK first:

| Request Type        | Action                                |
| ------------------- | ------------------------------------- |
| New Feature / Build | Ask 3+ strategic questions            |
| Code Edit / Bug Fix | Confirm understanding first           |
| Vague Request       | Ask Purpose, Users, Scope             |
| Full Orchestration  | User must confirm plan before Phase 2 |

**Never Assume.** If 1% unclear → ASK.

### 🎭 Mode Mapping

| Mode | Agent           | Behavior                        |
| ---- | --------------- | ------------------------------- |
| plan | project-planner | 4-phase, NO CODE before Phase 4 |
| ask  | -               | Questions only                  |
| edit | orchestrator    | Check {task-slug}.md first      |

---

## TIER 2: DESIGN RULES

> Rules in specialist agents: Web → `frontend-specialist.md`, Mobile → `mobile-developer.md`

---

## 📜 SCRIPTS (Automation)

### When to Run Scripts

| Trigger          | Script                     | Purpose                                  |
| ---------------- | -------------------------- | ---------------------------------------- |
| Before PR/commit | `checklist.py`             | Quick validation (Security, Lint, Tests) |
| Before deploy    | `verify_all.py`            | Full pre-deployment suite                |
| Kit maintenance  | `kit_status.py --validate` | Check kit integrity                      |
| Managing skills  | `skills_manager.py`        | Enable/disable/search skills             |

### Master Scripts

```bash
# Quick check during development
python3 .agent/scripts/checklist.py .

# Full check with performance audits
python3 .agent/scripts/checklist.py . --url http://localhost:3000

# Pre-deployment verification
python3 .agent/scripts/verify_all.py . --url http://localhost:3000

# Kit status
python3 .agent/scripts/kit_status.py --validate

# Skill management
python3 .agent/scripts/skills_manager.py list
python3 .agent/scripts/skills_manager.py search <query>
```

### Skill-Specific Scripts

| Skill                    | Script                | When to Use                      |
| ------------------------ | --------------------- | -------------------------------- |
| `clean-code`             | `lint_runner.py`      | After code changes               |
| `testing-patterns`       | `test_runner.py`      | After logic changes              |
| `security-fundamentals`  | `security_scan.py`    | Before deploy, after deps change |
| `database-design`        | `schema_validator.py` | After schema changes             |
| `api-patterns`           | `api_validator.py`    | After API changes                |
| `i18n-localization`      | `i18n_checker.py`     | After UI text changes            |
| `seo-patterns`           | `seo_checker.py`      | After page changes               |
| `accessibility-patterns` | `a11y_checker.py`     | After UI changes                 |

### AI Script Protocol

1. **Security changes** → Run `security_scan.py`
2. **Database changes** → Run `schema_validator.py`
3. **API changes** → Run `api_validator.py`
4. **UI changes** → Run `a11y_checker.py`
5. **Before suggesting deploy** → Run `verify_all.py`

> 🔴 Full script documentation: See `ARCHITECTURE.md` → Scripts section

---

## 📊 Kit Statistics

| Metric    | Count |
| --------- | ----- |
| Agents    | 22    |
| Skills    | 39    |
| Workflows | 7     |
| Scripts   | 19    |

---

> **Philosophy:** Modular agents + reusable skills + clear workflows + automated scripts = scalable AI assistance.
