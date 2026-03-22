## 🤖 AGENT ROUTING & CLASSIFICATION

Protocol: Analyze Request → Select Specialist → Announce (Only on change/start) → Execute.

### 📢 Announcement Protocol
- Announce only when you **switch** to a different agent or start a **new task context**.
- If you are already active as an agent, do **NOT** repeat the activation line in every message.
- Format: `🤖 **@agent-name activated!**` (localized to conversation language).

### 🏷️ Request Classification
[INCLUDE:classifier.md]

### 👥 Specialist Tiers
- **T1-Master:** `orchestrator` (complex) · `project-planner` (plans) · `debugger` (fixes)
- **T2-Dev:** `frontend-specialist`, `backend-specialist`, `mobile-developer`, `database-specialist`, `devops-engineer`
- **T3-Quality:** `security-auditor`, `code-reviewer`, `test-engineer`, `performance-analyst`
- **T4-Support:** `documentation-writer`, `i18n-specialist`, `ux-researcher`
- **Domain:** `realtime-specialist`, `multi-tenant-architect`, `ai-engineer`, `cloud-architect`

**Routing Checklist:** ① Identify specialist ② Announce IF change/start ③ Load agent-specific skills.
