---
trigger: always_on
description: AGT-Kit - AI Agent system with 22 agents, 40 skills, 7 commands
alwaysApply: true
---

# CURSOR Rules - AGT-Kit

> AI Agent Capability Expansion Toolkit - 22 agents · 40 skills · 7 commands.

---

## CRITICAL: AGENT & SKILL PROTOCOL

> **MANDATORY:** Read agent file + skills BEFORE any implementation.

Agent activated → Check frontmatter `skills:` → Read SKILL.md → Apply.

**Priority:** P0 (CURSOR.md) > P1 (Agent.md) > P2 (SKILL.md). All binding.

---

[INCLUDE:routing.md]

---

[INCLUDE:workflows.cursor.md]

---

[INCLUDE:skill.md]

---

[INCLUDE:universal.md]

---

[INCLUDE:code.md]

---

[INCLUDE:design.md]

---

[INCLUDE:scripts.md]

---

[INCLUDE:footer.md]
