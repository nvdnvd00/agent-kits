# OpenCode Structure Template

> Target directory structure and transformation rules for OpenCode CLI.

---

## 📁 Target Directory Layout

```plaintext
project-root/
├── AGENTS.md                    # Main rules file (at project root)
└── .opencode/
    ├── agents/                  # Agent persona files (transformed)
    │   ├── orchestrator.md
    │   ├── frontend-specialist.md
    │   └── ... (22 agents total)
    ├── commands/                # Commands (from workflows)
    │   ├── plan.md
    │   ├── create.md
    │   ├── debug.md
    │   └── ... (7 commands total)
    ├── skills/                  # Skills (copied directly)
    │   ├── clean-code/
    │   ├── react-patterns/
    │   └── ... (39+ skills)
    ├── scripts/                 # Automation scripts
    │   └── *.py
    └── COMMON.md                # Shared skills documentation
```

---

## 🔄 Transformation Rules

### 1. Rules File

| Source                        | Target       |
| ----------------------------- | ------------ |
| `kits/<kit>/rules/AGENTS.md` | `AGENTS.md`  |

**Transformations:**

- Placed at **project root** (not inside `.opencode/`)
- Replace `.agent/` → `.opencode/`
- Replace `workflows/` → `commands/`

### 2. Agents (Tools String → Record)

| Source                   | Target                  |
| ------------------------ | ----------------------- |
| `kits/<kit>/agents/*.md` | `.opencode/agents/*.md` |

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

# TO (OpenCode agent format)
---
description: Senior Frontend Architect...
model: inherit
tools:
  read: true
  grep: true
  glob: true
  bash: true
  edit: true
  write: true
---
```

**Key changes:**

- `name` → **removed** (derived from filename in OpenCode)
- `tools` → **converted** from comma-separated string to YAML record/map
- Tool names → **lowercased** (Read → read, Write → write)
- `skills` → **removed** from frontmatter (referenced in body)
- `tier` → **removed** (OpenCode doesn't use tiers)

**Body Transformations:**

- Replace `.agent/` → `.opencode/` in all paths

### 3. Workflows → Commands

| Source                      | Target                    |
| --------------------------- | ------------------------- |
| `kits/<kit>/workflows/*.md` | `.opencode/commands/*.md` |

**Frontmatter Transformation:**

```yaml
# FROM (Agent-Kits Workflow format)
---
description: Create project plan using project-planner agent.
---

# TO (OpenCode Command format)
---
description: Create project plan using project-planner agent.
---
```

**Body Transformations:**

- Replace `.agent/` → `.opencode/` in all paths
- Replace `workflow` → `command` terminology
- Replace `workflows/` → `commands/` folder references

### 4. Skills

| Source                | Target               |
| --------------------- | -------------------- |
| `kits/<kit>/skills/*` | `.opencode/skills/*` |

**Transformations:**

- Replace `.agent/` → `.opencode/` in content
- No structural changes

### 5. Scripts

| Source                    | Target                  |
| ------------------------- | ----------------------- |
| `kits/<kit>/scripts/*.py` | `.opencode/scripts/*.py` |

**Transformations:**

- None

---

## 📋 OpenCode Agent Frontmatter Fields

| Field         | Type                    | Required | Description                        |
| ------------- | ----------------------- | -------- | ---------------------------------- |
| `description` | string                  | ✅       | Agent purpose description          |
| `model`       | string                  | ❌       | Model override (provider/model-id) |
| `tools`       | record<string, boolean> | ❌       | Tool availability map              |
| `mode`        | string                  | ❌       | `primary` or `subagent`            |

### Field Mapping from Agent-Kits

| Agent-Kits Field | OpenCode Field | Notes                                    |
| ---------------- | -------------- | ---------------------------------------- |
| `name`           | ❌ removed     | Derived from filename                    |
| `description`    | `description`  | Direct copy                              |
| `model`          | `model`        | Direct copy                              |
| `tools`          | `tools`        | String → record<string, boolean>         |
| `skills`         | ❌ removed     | Referenced in body, not frontmatter      |
| `tier`           | ❌ removed     | OpenCode doesn't use tiers               |

### Tools Mapping

| Agent-Kits Name | OpenCode Name | Description                |
| --------------- | ------------- | -------------------------- |
| `Read`          | `read`        | File reading               |
| `Write`         | `write`       | File writing               |
| `Edit`          | `edit`        | File editing               |
| `Bash`          | `bash`        | Shell command execution    |
| `Grep`          | `grep`        | Pattern searching          |
| `Glob`          | `glob`        | File/directory matching    |
| `Agent`         | `agent`       | Sub-agent invocation       |

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

### After (OpenCode)

```markdown
---
description: Senior Frontend Architect for React/Next.js/Vue systems
model: inherit
tools:
  read: true
  grep: true
  glob: true
  bash: true
  edit: true
  write: true
---

# Frontend Specialist - Senior Frontend Architect

Senior Frontend Architect who designs and builds...
```

---

## ✅ Validation Checklist

After installation, verify:

- [ ] `AGENTS.md` exists at project root
- [ ] `.opencode/agents/` contains all agent files
- [ ] `.opencode/commands/` contains all command files
- [ ] `.opencode/skills/` contains all skill directories
- [ ] `.opencode/scripts/` contains all script files
- [ ] `.opencode/COMMON.md` exists
- [ ] All path references use `.opencode/` not `.agent/`
- [ ] Agent `tools` field is a YAML record (not a string)
- [ ] Agent files do NOT have `name`, `skills`, or `tier` in frontmatter
