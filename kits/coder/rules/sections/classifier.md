## 📥 REQUEST CLASSIFIER

Detect **user intent**, not keywords. Works for any language.

- QUESTION (wants explanation/understanding) → `orchestrator`
- PLAN (explicitly wants a plan before doing) → `project-planner`
- CREATE (build something new from scratch) → `orchestrator` → specialists
- DEBUG (fix bug, investigate error) → `debugger`
- TEST (write or run tests) → `test-engineer`
- DEPLOY (release, publish to production) → `devops-engineer`
- COMPLEX (spans 3+ domains) → `orchestrator`

**Priority:** DEBUG > CREATE > PLAN. ALWAYS select an agent. NEVER answer without the activation header.
