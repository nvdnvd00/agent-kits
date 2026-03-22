## 🛠️ SKILL LOADING PROTOCOL (OpenCode)

`Agent activated → Check ARCHITECTURE.md for assigned skills → Call skill({ name }) → Apply`

OpenCode has a **native `skill` tool** that auto-discovers all available skills from `.agent/skills/*/SKILL.md`.

**Steps:**
1. Read ARCHITECTURE.md → find your agent → note "Skills Used" column
2. Call `skill({ name: "skill-name" })` for each assigned skill
3. Apply all loaded skill rules

**Skill Permissions** (in `opencode.json`):
```json
{ "permission": { "skill": { "*": "allow" } } }
```

Check `.agent/profile.json` first:
- EXISTS → respect `skills.enabled[]`, `skills.disabled[]`, `agents.disabled[]`
- NOT EXISTS → all skills/agents enabled by default

**Core Skills (never disabled):** `clean-code` · `testing-patterns` · `security-fundamentals` · `brainstorming` · `plan-writing` · `systematic-debugging`

> Full skill list: `.agent/ARCHITECTURE.md` → Skills section
