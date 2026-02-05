# Contributing to Agent Kits

Thank you for your interest in contributing to Agent Kits! 🎉

---

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Kit Structure Standard](#-kit-structure-standard)
- [Creating a New Kit](#-creating-a-new-kit)
- [Adding Agents & Skills](#-adding-agents--skills)
- [Testing](#-testing)
- [Pull Request Process](#-pull-request-process)
- [Code Style](#-code-style)

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- pnpm (recommended)
- Python 3.8+ (for validation scripts)

### Setup

```bash
# Clone the repository
git clone https://github.com/nvdnvd00/agent-kits.git
cd agent-kits

# Install dependencies
pnpm install

# Build the CLI
pnpm build

# Test locally
node dist/cli.js
```

---

## 📐 Kit Structure Standard

> **Important:** All kits MUST follow the structure defined in [docs/KIT_SPEC.md](docs/KIT_SPEC.md).

### Required Directory Structure

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

### Key Differences from Generic Structure

| Component           | Location           | Notes                      |
| ------------------- | ------------------ | -------------------------- |
| **Rules files**     | `rules/` folder    | NOT at kit root            |
| **Path references** | Use `.agent/`      | Installer auto-replaces    |
| **Frontmatter**     | YAML at file start | Required for all .md files |

### Validate Your Kit

Always validate before committing:

```bash
python3 scripts/validate_kit.py kits/<kit-name>

# Verbose mode to see all checks
python3 scripts/validate_kit.py kits/<kit-name> --verbose
```

---

## 📦 Creating a New Kit

### Step 1: Create Directory Structure

```bash
mkdir -p kits/my-kit/{agents,skills,workflows,rules,scripts}
```

### Step 2: Create ARCHITECTURE.md

Main documentation file. See [KIT_SPEC.md](docs/KIT_SPEC.md#1-architecturemd) for required sections.

```markdown
# My Kit Architecture

> One-line description

---

## 📋 Overview

[Description of the kit's purpose and components]

## 🔗 Common Skills

[Reference to inherited common skills from `common/`]

## 🏗️ Directory Structure

[Tree structure of the kit]

## 🤖 Agents

[Table of all agents with their focus and skills]

## 🧩 Skills

[Table of all skills with descriptions]

## 🔄 Workflows

[Table of all slash commands]

## 📊 Statistics

| Metric              | Value |
| ------------------- | ----- |
| **Total Agents**    | X     |
| **Total Skills**    | X     |
| **Total Workflows** | X     |
```

### Step 3: Create Rules Files

Create **4 rule files** in `rules/` folder:

| File        | For Tool                | Frontmatter Required    |
| ----------- | ----------------------- | ----------------------- |
| `GEMINI.md` | Gemini CLI, Antigravity | ✅ Yes (`trigger:`)     |
| `CURSOR.md` | Cursor                  | ✅ Yes (`description:`) |
| `CLAUDE.md` | Claude Code             | ❌ No (plain markdown)  |
| `AGENTS.md` | Codex CLI               | ❌ No (plain markdown)  |

**For GEMINI.md:**

```yaml
---
trigger: always_on
---
```

**For CURSOR.md:**

```yaml
---
trigger: always_on
description: AGT-Kit - AI Agent system with X agents, Y skills, Z commands
alwaysApply: true
---
```

**For CLAUDE.md / AGENTS.md (No frontmatter):**

```markdown
# CLAUDE.md - My Kit

> One-line description
> ...
```

> **Important:** Use `.agent/` as path placeholder. The installer will replace it with tool-specific paths.

### Step 4: Create Agent Files

Create `agents/<agent-name>.md`:

```markdown
---
name: orchestrator
description: Main coordinator for My Kit
skills: skill-1, skill-2
tier: 1
---

# Orchestrator Agent

> Coordinates all tasks within My Kit

## 🎯 Role

[Describe the agent's primary role]

## 🛠️ Capabilities

- [Capability 1]
- [Capability 2]

## 📋 When to Use

Use this agent when:

- [Condition 1]
- [Condition 2]
```

### Step 5: Create Skill Files

Create `skills/<skill-name>/SKILL.md`:

```markdown
---
name: core-skill
description: Primary skill for My Kit
version: 1.0
priority: HIGH
---

# Core Skill

> One-line description

---

## Core Principles

[Table of principles]

## Guidelines

[Domain-specific rules]

## Summary

[Do/Don't table]
```

### Step 6: Create Workflow Files

Create `workflows/<workflow-name>.md`:

```markdown
---
description: Main workflow for My Kit
---

# /main - Main Workflow

## Trigger

User calls `/main` or requests main functionality

## Agent

`orchestrator`

## Workflow Steps

### Step 1: [Name]

[Instructions]

### Step 2: [Name]

[Instructions]

## Exit Conditions

- Success condition
- Failure condition
```

### Step 7: Register Kit in CLI

Edit `src/config.ts`:

```typescript
export const KITS: Kit[] = [
  // ... existing kits
  {
    id: "my-kit",
    name: "My Kit",
    icon: "🎯",
    description: "Description of my kit",
    agents: 5,
    skills: 10,
    workflows: 3,
    available: true,
  },
];
```

### Step 8: Validate & Test

```bash
# Validate structure
python3 scripts/validate_kit.py kits/my-kit

# Build CLI
pnpm build

# Test installation
node dist/cli.js
```

---

## 🤖 Adding Agents & Skills

### Agent Frontmatter Requirements

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

### Skill Frontmatter Requirements

```yaml
---
name: <skill-name>
description: <one-line description for auto-loading>
allowed-tools: Read, Write, Edit
version: 1.0
priority: CRITICAL | HIGH | MEDIUM | LOW
---
```

### Quality Guidelines

| Criteria     | Agent Requirement | Skill Requirement |
| ------------ | ----------------- | ----------------- |
| Frontmatter  | ✅ YAML required  | ✅ YAML required  |
| Description  | For routing       | For auto-loading  |
| Skills field | List of skills    | N/A               |
| Examples     | When to use       | At least 1-2      |

---

## 🧪 Testing

### Validate Kit Structure

```bash
python3 scripts/validate_kit.py kits/<kit-name>
```

### Build & Test CLI

```bash
# Build
pnpm build

# Interactive mode
node dist/cli.js

# With arguments
node dist/cli.js --tool antigravity --kit coder --path ./test-install
```

### Checklist Before PR

- [ ] `ARCHITECTURE.md` exists and complete
- [ ] All 4 rule files in `rules/` folder
- [ ] All files have proper YAML frontmatter
- [ ] Path references use `.agent/` placeholder
- [ ] Statistics are accurate
- [ ] `python3 scripts/validate_kit.py kits/<kit-name>` passes

---

## 📝 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/my-feature`
3. **Validate** your kit: `python3 scripts/validate_kit.py kits/<kit-name>`
4. **Build** to verify: `pnpm build`
5. **Commit** with conventional format: `git commit -m "feat: add my-kit"`
6. **Push** to your fork: `git push origin feat/my-feature`
7. **Create** a Pull Request with:
   - Clear description of changes
   - Validation output screenshot
   - List of files added/modified

### Commit Message Format

```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
Scope: cli, kit-name, skill-name, agent-name
```

Examples:

```
feat(my-kit): add new kit for data science
fix(coder): correct skill loading order
docs(readme): add Chinese translation
```

---

## 🎨 Code Style

### TypeScript (CLI code)

- ESM modules
- Use Prettier for formatting
- Follow existing patterns in `src/`

### Markdown (Kits documentation)

- Use fenced code blocks with language specifiers
- Tables over long prose
- Consistent heading hierarchy
- YAML frontmatter for all agent/skill/workflow files

### File Naming

| Type            | Convention    | Example          |
| --------------- | ------------- | ---------------- |
| Kit folder      | kebab-case    | `my-kit`         |
| Agent file      | kebab-case.md | `my-agent.md`    |
| Skill folder    | kebab-case    | `my-skill`       |
| Skill main file | UPPERCASE     | `SKILL.md`       |
| Workflow file   | kebab-case.md | `my-workflow.md` |
| Rules file      | UPPERCASE.md  | `GEMINI.md`      |

---

## 📚 References

- [Kit Specification](docs/KIT_SPEC.md) - Full structure requirements
- [Coder Kit](kits/coder/) - Reference implementation
- [Common Skills](common/COMMON.md) - Shared skills layer

---

## ❓ Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

---

<p align="center">
  <sub>Thank you for contributing! 🙏</sub>
</p>
