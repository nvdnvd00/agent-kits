# Antigravity Structure Template

> Target directory structure for Antigravity (standard Agent-Kits format).

---

## 📁 Target Directory Layout

```plaintext
.agent/
├── GEMINI.md                  # Main rules file
├── agents/                    # Agent persona files
│   ├── orchestrator.md
│   ├── frontend-specialist.md
│   └── ... (22 agents total)
├── workflows/                 # Slash command procedures
│   ├── plan.md
│   ├── create.md
│   └── ... (7 workflows total)
├── skills/                    # Skill modules
│   ├── clean-code/
│   ├── react-patterns/
│   └── ... (39+ skills)
├── scripts/                   # Automation scripts
│   └── *.py
└── COMMON.md                  # Shared skills documentation
```

---

## 🔄 Transformation Rules

### No Structural Transformation Required

Antigravity uses the **standard Agent-Kits format**. Files are copied with minimal transformation:

### 1. Rules File

| Source                       | Target             |
| ---------------------------- | ------------------ |
| `kits/<kit>/rules/GEMINI.md` | `.agent/GEMINI.md` |

**Transformations:**

- None (source format matches target format)

### 2. Agents

| Source                   | Target               |
| ------------------------ | -------------------- |
| `kits/<kit>/agents/*.md` | `.agent/agents/*.md` |

**Transformations:**

- None (standard format is preserved)

### 3. Workflows

| Source                      | Target                  |
| --------------------------- | ----------------------- |
| `kits/<kit>/workflows/*.md` | `.agent/workflows/*.md` |

**Transformations:**

- None

### 4. Skills

| Source                | Target            |
| --------------------- | ----------------- |
| `kits/<kit>/skills/*` | `.agent/skills/*` |

**Transformations:**

- None

### 5. Scripts

| Source                    | Target                |
| ------------------------- | --------------------- |
| `kits/<kit>/scripts/*.py` | `.agent/scripts/*.py` |

**Transformations:**

- None

---

## 📋 Agent Frontmatter (Standard Format)

Antigravity uses the full Agent-Kits frontmatter:

```yaml
---
name: <agent-name>
description: <routing description>
tools: Read, Write, Edit, Bash, Agent
model: inherit
skills: skill-1, skill-2, skill-3
tier: <1-5>
---
```

### Field Descriptions

| Field         | Type   | Required | Description                             |
| ------------- | ------ | -------- | --------------------------------------- |
| `name`        | string | ✅       | Unique identifier                       |
| `description` | string | ✅       | Used for agent routing                  |
| `tools`       | string | ✅       | Available tools for this agent          |
| `model`       | string | ❌       | AI model to use (default: `inherit`)    |
| `skills`      | string | ✅       | Comma-separated list of required skills |
| `tier`        | number | ✅       | Agent tier (1-5) for priority           |

---

## 📝 Example (No Transformation)

### Source (Agent-Kits)

```markdown
---
name: frontend-specialist
description: Senior Frontend Architect for React/Next.js/Vue systems
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, react-patterns, typescript-patterns
tier: 2
---

# Frontend Specialist - Senior Frontend Architect

Senior Frontend Architect who designs and builds...
```

### Target (Antigravity) - Same format

```markdown
---
name: frontend-specialist
description: Senior Frontend Architect for React/Next.js/Vue systems
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, react-patterns, typescript-patterns
tier: 2
---

# Frontend Specialist - Senior Frontend Architect

Senior Frontend Architect who designs and builds...
```

---

## ✅ Validation Checklist

After installation, verify:

- [ ] `.agent/GEMINI.md` exists
- [ ] `.agent/agents/` contains all agent files
- [ ] `.agent/workflows/` contains all workflow files
- [ ] `.agent/skills/` contains all skill directories
- [ ] `.agent/scripts/` contains all script files
- [ ] `.agent/COMMON.md` exists
- [ ] Agent files have standard frontmatter format
