## 🛠️ SKILL LOADING PROTOCOL

`User Request → Check Profile → Match Skill → Read SKILL.md → Apply`

Check `.agent/profile.json` first:
- EXISTS → respect `skills.enabled[]`, `skills.disabled[]`, `agents.disabled[]`
- NOT EXISTS → all skills/agents enabled by default

**Core Skills (never disabled):** `clean-code` · `testing-patterns` · `security-fundamentals` · `brainstorming` · `plan-writing` · `systematic-debugging`

> Full skill list: `ARCHITECTURE.md` → Skills section
