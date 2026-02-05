# Kit Specification (v1.0)

> Standard structure and requirements for creating new Agent Kits.

---

## 📋 Overview

A **Kit** is a complete AI agent toolkit containing:

- **Agents** - Specialist AI personas
- **Skills** - Domain-specific knowledge modules
- **Workflows** - Slash command procedures
- **Rules** - AI behavior configuration per tool
- **Scripts** - Automation utilities

---

## 🏗️ Required Directory Structure

```plaintext
kits/<kit-name>/
├── ARCHITECTURE.md              # [REQUIRED] Kit documentation
├── rules/                       # [REQUIRED] AI tool-specific rules
│   ├── GEMINI.md               # For Gemini CLI / Antigravity
│   ├── CLAUDE.md               # For Claude Code
│   ├── CURSOR.md               # For Cursor
│   └── AGENTS.md               # For Codex CLI
├── agents/                      # [REQUIRED] Agent persona files
│   ├── orchestrator.md         # Primary coordinator agent
│   └── <agent-name>.md         # Additional specialist agents
├── skills/                      # [REQUIRED] Skill modules
│   └── <skill-name>/
│       └── SKILL.md            # Skill definition
├── workflows/                   # [RECOMMENDED] Slash commands
│   └── <workflow-name>.md      # Workflow definition
└── scripts/                     # [OPTIONAL] Automation scripts
    └── <script-name>.py        # Python validation scripts
```

---

## 📝 Required Files

### 1. ARCHITECTURE.md

Main documentation file describing the kit's structure and capabilities.

**Required Sections:**

```markdown
# <Kit-Name> Architecture

> One-line description

---

## 📋 Overview

[Description of the kit's purpose and components]

---

## 🔗 Common Skills

[Reference to inherited common skills from `common/`]

---

## 🏗️ Directory Structure

[Tree structure of the kit]

---

## 🤖 Agents

[Table of all agents with their focus and skills]

---

## 🧩 Skills

[Table of all skills with descriptions]

---

## 🔄 Workflows

[Table of all slash commands]

---

## 📜 Scripts

[Table of available automation scripts]

---

## 📊 Statistics

| Metric              | Value |
| ------------------- | ----- |
| **Total Agents**    | X     |
| **Total Skills**    | X     |
| **Total Workflows** | X     |
```

---

### 2. Rules Files (`rules/` folder)

Each AI tool requires a specific rules file.

**Frontmatter Requirements by Tool:**

| File        | For Tool                | Frontmatter Required | Fields                         |
| ----------- | ----------------------- | -------------------- | ------------------------------ |
| `GEMINI.md` | Gemini CLI, Antigravity | ✅ Yes               | `trigger: always_on`           |
| `CURSOR.md` | Cursor                  | ✅ Yes               | `description:`, `alwaysApply:` |
| `CLAUDE.md` | Claude Code             | ❌ No                | Plain markdown                 |
| `AGENTS.md` | Codex CLI               | ❌ No                | Plain markdown                 |

**Example: GEMINI.md Frontmatter**

```yaml
---
trigger: always_on
---
```

**Example: CURSOR.md Frontmatter**

```yaml
---
trigger: always_on
description: AGT-Kit - AI Agent system with X agents, Y skills, Z commands
alwaysApply: true
---
```

**Example: CLAUDE.md / AGENTS.md (No frontmatter)**

```markdown
# CLAUDE.md - AGT-Kit

> AI Agent Capability Expansion Toolkit...
```

**Required Content (All rule files):**

- Kit Purpose
- Request Classifier table
- Agent Routing protocol
- Workflows/Commands table
- Skill Loading protocol
- Statistics

**Path References:**

- MUST use `.agent/` as the placeholder path
- Installer will replace with tool-specific path (`.claude/`, `.gemini/`, `.cursor/`, etc.)

**Tool-Specific Notes:**

| File        | Special Handling                         |
| ----------- | ---------------------------------------- |
| `CURSOR.md` | Uses `commands/` instead of `workflows/` |
| `CLAUDE.md` | Can reference `.claude/rules/*.md` paths |
| `AGENTS.md` | Hierarchical loading from `~/.codex/`    |

---

### 3. Agent Files (`agents/<agent-name>.md`)

**YAML Frontmatter (Required):**

```yaml
---
name: <agent-name>
description: <one-line description for routing>
tools: Read, Write, Edit, Bash, Agent
model: inherit
skills: skill-1, skill-2
tier: <1-5>
---
```

**Tier Definitions:**
| Tier | Role | Example |
|------|------|---------|
| 1 | Master/Coordinator | orchestrator, project-planner |
| 2 | Development Specialist | frontend-specialist, backend-specialist |
| 3 | Quality/Security | security-auditor, test-engineer |
| 4 | Domain Specialist | realtime-specialist, ai-engineer |
| 5 | Support | documentation-writer, i18n-specialist |

**Required Sections:**

```markdown
# <Agent-Name> - <Short Description>

[Philosophy quote]

## 📑 Quick Navigation

[Links to sections]

---

## 📖 Philosophy

[Core principles table]

---

## ✅ PRE-FLIGHT CHECKS (MANDATORY)

[Required checks before action]

---

## 🎯 WHEN TO USE THIS AGENT

[Use cases and anti-patterns]
```

---

### 4. Skill Files (`skills/<skill-name>/SKILL.md`)

**YAML Frontmatter (Required):**

```yaml
---
name: <skill-name>
description: <one-line description for auto-loading>
allowed-tools: Read, Write, Edit
version: 1.0
priority: CRITICAL | HIGH | MEDIUM | LOW
---
```

**Required Sections:**

```markdown
# <Skill-Name> - <Short Description>

> Philosophy quote

---

## Core Principles

[Table of principles]

---

## [Domain-Specific Sections]

[Rules, patterns, decision trees]

---

## Summary

[Do/Don't table]

---

## 🔴 Self-Check Before Completing (MANDATORY)

[Checklist]

---

## Related Skills

[Links to related skills]
```

**Optional Subdirectories:**

```plaintext
skills/<skill-name>/
├── SKILL.md           # [Required]
├── scripts/           # [Optional] Automation scripts
├── references/        # [Optional] Templates, docs
└── assets/            # [Optional] Images, logos
```

---

### 5. Workflow Files (`workflows/<workflow-name>.md`)

**YAML Frontmatter (Required):**

```yaml
---
description: <one-line description for /help>
---
```

**Required Sections:**

```markdown
# /<command> - <Name>

## Trigger

[When this workflow is activated]

## Agent

[Primary agent for this workflow]

## Critical Rules

[Numbered list of rules]

---

## Workflow Steps

### Step 1: <Name>

[Instructions]

### Step 2: <Name>

[Instructions]

---

## Output Format

[Expected output]

---

## Exit Conditions

[Success/failure conditions]
```

---

## 🔄 Installer Behavior

### Path Normalization

The installer automatically replaces path references:

| Source Reference | Target (by tool)        |
| ---------------- | ----------------------- |
| `.agent/`        | `.claude/` (Claude)     |
| `.agent/`        | `.gemini/` (Gemini)     |
| `.agent/`        | `.cursor/` (Cursor)     |
| `.agent/`        | `.codex/` (Codex)       |
| `.agent/`        | `.agent/` (Antigravity) |

### Cursor-Specific Transformation

| Source                  | Target                 |
| ----------------------- | ---------------------- |
| `workflows/` folder     | `commands/` folder     |
| `workflows/` in content | `commands/` in content |
| `agents/` files         | Subagent format        |

#### Agent → Subagent Transformation

Cursor uses a different agent format called "subagents". The installer automatically transforms:

**From Agent-Kits format:**

```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
tools: Read, Grep, Glob, Bash, Edit, Write
model: inherit
skills: clean-code, react-patterns
tier: 2
---
```

**To Cursor Subagent format:**

```yaml
---
name: frontend-specialist
description: Senior Frontend Architect...
model: inherit
readonly: false
is_background: false
---
```

Skills are embedded as a "Required Skills" section in the agent body.

#### Workflow → Command Transformation

Cursor calls workflows "commands" and stores them in `.cursor/commands/`. The installer automatically:

- Renames `workflows/` folder to `commands/`
- Replaces `.agent/` paths with `.cursor/` in content
- Replaces "workflow" terminology with "command"

See `templates/cursor/STRUCTURE.md` for full transformation rules.

### Common Assets

Installer automatically copies from `common/`:

- `common/skills/` → `<target>/skills/`
- `common/workflows/` → `<target>/workflows/` (or `commands/` for Cursor)
- `common/COMMON.md` → `<target>/COMMON.md`

---

## ✅ Validation Checklist

Before publishing a kit, verify:

### Structure

- [ ] `ARCHITECTURE.md` exists and is complete
- [ ] `rules/` folder with all 4 rule files
- [ ] At least 1 agent in `agents/`
- [ ] At least 1 skill in `skills/`
- [ ] All files have proper YAML frontmatter

### Content

- [ ] All path references use `.agent/` placeholder
- [ ] Agent descriptions match routing table in rules
- [ ] Skill descriptions are searchable
- [ ] Statistics are accurate

### Quality

- [ ] No broken internal links
- [ ] Consistent formatting
- [ ] Tables are properly formatted
- [ ] Code blocks have language specifiers

Run validation:

```bash
python3 scripts/validate_kit.py kits/<kit-name>
```

---

## 📊 Example: Coder Kit Statistics

| Metric     | Value |
| ---------- | ----- |
| Agents     | 22    |
| Skills     | 40    |
| Workflows  | 7     |
| Scripts    | 4     |
| Rule Files | 4     |

---

## 🔗 References

- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [Common Skills](../common/COMMON.md) - Shared skills layer
- [Coder Kit](../kits/coder/ARCHITECTURE.md) - Reference implementation
