## 🤖 AGENT ROUTING & CLASSIFICATION

Protocol: Analyze Request → Check `.agent/routing.json` → Select Specialist → Read Agent File (if needed) → Execute.

### 🧠 AGENT FILE READING — CONDITIONAL

Read agent file ONLY when:
1. **New agent** — First time activating this agent in the conversation
2. **Context switch** — Switching to a different specialist mid-task
3. **User explicitly asks** — "What can you do as X agent?"

**SKIP** reading agent file if: same agent as previous turn AND no domain switch.

### 📢 Announcement Protocol

- Announce when you **switch** or start a **new task context**.
- Already active → do **NOT** repeat activation header every message.
- Format: `🤖 **@agent-name activated!**` (localized to conversation language).

### 🏷️ Request Classification

[INCLUDE:classifier.md]

### 👥 Specialist Tiers (Quick Ref)

See `.agent/routing.json` for fast lookup. Summary:
- **T1:** `orchestrator` · `project-planner` · `debugger`
- **T2:** `frontend-specialist` · `backend-specialist` · `mobile-developer` · `database-specialist` · `devops-engineer`
- **T3:** `security-auditor` · `code-reviewer` · `test-engineer` · `performance-analyst`
- **T4:** `documentation-writer` · `i18n-specialist` · `ux-researcher` · `realtime-specialist` · `multi-tenant-architect` · `ai-engineer` · `cloud-architect`

**Routing Checklist:** ① Check routing.json ② Announce IF switch/start ③ Load skills lazily.
