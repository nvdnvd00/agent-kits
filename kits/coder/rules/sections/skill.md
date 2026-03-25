## 🛠️ SKILL LOADING PROTOCOL

`User Request → Check Profile → Lazy Load → Apply`

Check `.agent/profile.json` first:
- EXISTS → respect `skills.enabled[]`, `skills.disabled[]`, `agents.disabled[]`
- NOT EXISTS → all skills/agents enabled by default

**Core Skills (never disabled):** `clean-code` · `testing-patterns` · `security-fundamentals` · `brainstorming` · `plan-writing` · `systematic-debugging`

### ⚡ Lazy Loading Decision Gate

**BEFORE reading any SKILL.md**, answer:
- Implementing a specific pattern from this skill? → **Read FULL SKILL.md**
- Just applying general principles / planning? → **Read SKILL.summary.md** (if exists), otherwise skip
- Just routing / answering a question? → **Skip — don't load skill at all**

> Full skill list: `.agent/ARCHITECTURE.index.md`
