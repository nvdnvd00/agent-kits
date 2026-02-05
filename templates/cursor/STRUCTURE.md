# Cursor Structure Template

> Target directory structure and transformation rules for Cursor IDE.

---

## 📁 Target Directory Layout

```plaintext
.cursor/
├── rules/
│   └── rules.md              # Main rules file (from CURSOR.md)
├── agents/                    # Subagents (transformed from kit agents)
│   ├── orchestrator.md
│   ├── frontend-specialist.md
│   ├── backend-specialist.md
│   └── ... (22 agents total)
├── commands/                  # Commands (from workflows)
│   ├── plan.md
│   ├── create.md
│   ├── debug.md
│   └── ... (7 commands total)
└── skills/                    # Skills (copied directly)
    ├── clean-code/
    ├── react-patterns/
    └── ... (39+ skills)
```

---

## 🔄 Transformation Rules

### 1. Rules File

| Source                       | Target                   |
| ---------------------------- | ------------------------ |
| `kits/<kit>/rules/CURSOR.md` | `.cursor/rules/rules.md` |

**Transformations:**

- Replace `.agent/` → `.cursor/`
- Replace `workflows/` → `commands/`

### 2. Agents → Subagents

| Source                   | Target                |
| ------------------------ | --------------------- |
| `kits/<kit>/agents/*.md` | `.cursor/agents/*.md` |

**Frontmatter Transformation:**

```yaml
# FROM (Agent-Kits format)
---
name: frontend-specialist
description: Senior Frontend Architect...
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, react-patterns, typescript-patterns
tier: 2
---
# TO (Cursor Subagent format)
---
name: frontend-specialist
description: Senior Frontend Architect...
model: inherit
readonly: false
is_background: false
---
```

**Body Transformation:**

- Inject "Required Skills" section at the beginning of body
- Skills list converted to markdown list

### 3. Workflows → Commands

| Source                      | Target                  |
| --------------------------- | ----------------------- |
| `kits/<kit>/workflows/*.md` | `.cursor/commands/*.md` |

**Frontmatter Transformation:**

```yaml
# FROM (Agent-Kits Workflow format)
---
description: Create project plan using project-planner agent.
---
# TO (Cursor Command format)
---
description: Create project plan using project-planner agent.
---
```

**Body Transformations:**

- Replace `.agent/` → `.cursor/` in all paths
- Replace `workflow` → `command` terminology
- Replace `workflows/` → `commands/` folder references

**Example:**

```markdown
# Before

Route to agent at `.agent/agents/planner.md`
This workflow creates plan...

# After

Route to agent at `.cursor/agents/planner.md`
This command creates plan...
```

### 4. Skills

| Source                | Target             |
| --------------------- | ------------------ |
| `kits/<kit>/skills/*` | `.cursor/skills/*` |

**Transformations:**

- Replace `.agent/` → `.cursor/` in content
- No structural changes

---

## 📋 Cursor Subagent Frontmatter Fields

| Field           | Type    | Required | Description                    |
| --------------- | ------- | -------- | ------------------------------ |
| `name`          | string  | ✅       | Unique identifier              |
| `description`   | string  | ✅       | Used for agent routing         |
| `model`         | string  | ❌       | `inherit`, `fast`, or model ID |
| `readonly`      | boolean | ❌       | Restrict write permissions     |
| `is_background` | boolean | ❌       | Run independently              |

### Field Mapping from Agent-Kits

| Agent-Kits Field | Cursor Field    | Notes                            |
| ---------------- | --------------- | -------------------------------- |
| `name`           | `name`          | Direct copy                      |
| `description`    | `description`   | Direct copy                      |
| `model`          | `model`         | Direct copy (default: `inherit`) |
| `tools`          | ❌ removed      | Cursor doesn't use this          |
| `skills`         | ❌ removed      | Embedded in body instead         |
| `tier`           | ❌ removed      | Cursor doesn't use this          |
| -                | `readonly`      | Default: `false`                 |
| -                | `is_background` | Default: `false`                 |

---

## 📝 Example Transformation

### Before (Agent-Kits)

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

### After (Cursor Subagent)

```markdown
---
name: frontend-specialist
description: Senior Frontend Architect for React/Next.js/Vue systems
model: inherit
readonly: false
is_background: false
---

# Frontend Specialist - Senior Frontend Architect

## 📚 Required Skills

This agent uses the following skills from `.cursor/skills/`:

- **clean-code** - Pragmatic coding standards
- **react-patterns** - React and Next.js patterns
- **typescript-patterns** - TypeScript advanced patterns

---

Senior Frontend Architect who designs and builds...
```

---

## ✅ Validation Checklist

After installation, verify:

- [ ] `.cursor/rules/rules.md` exists
- [ ] `.cursor/agents/` contains all agent files
- [ ] `.cursor/commands/` contains all command files
- [ ] `.cursor/skills/` contains all skill directories
- [ ] All path references use `.cursor/` not `.agent/`
- [ ] Agent files have Cursor subagent frontmatter format
