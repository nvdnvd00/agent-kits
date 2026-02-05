# Contributing to Agent Kits

Thank you for your interest in contributing to Agent Kits! 🎉

---

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Creating a New Kit](#-creating-a-new-kit)
- [Adding Agents & Skills](#-adding-agents--skills)
- [Testing](#-testing)
- [Pull Request Process](#-pull-request-process)
- [Code Style](#-code-style)

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- pnpm (recommended) or npm
- Python 3.8+ (for skill/agent creation scripts)

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

## 📦 Creating a New Kit

A "Kit" is a complete toolkit containing agents, skills, and workflows for a specific domain.

### Step 1: Create Directory Structure

```bash
mkdir -p kits/my-kit/{agents,skills,workflows}
```

Required structure:

```
kits/my-kit/
├── ARCHITECTURE.md          # Kit documentation (REQUIRED)
├── GEMINI.md                # AI rules for Gemini (REQUIRED)
├── CLAUDE.md                # AI rules for Claude (optional, mirrors GEMINI.md)
├── agents/                  # Agent persona files
│   ├── orchestrator.md      # Main coordinator agent
│   └── specialist.md        # Domain specialist agents
├── skills/                  # Domain-specific skills
│   └── core-skill/
│       └── SKILL.md
└── workflows/               # Slash command definitions
    └── main.md
```

### Step 2: Create ARCHITECTURE.md

This is the main documentation for your kit:

```markdown
# My Kit Architecture

> One-line description of the kit

---

## 🎯 Purpose

[Describe the primary use case and target audience]

---

## 🤖 Agents

| Agent          | Description      | Skills     |
| -------------- | ---------------- | ---------- |
| `orchestrator` | Main coordinator | all        |
| `specialist`   | Domain expert    | core-skill |

---

## 🧩 Skills

### Core Skills

| Skill        | Description          |
| ------------ | -------------------- |
| `core-skill` | Primary domain skill |

---

## 📜 Workflows

| Command | Description   | Agent        |
| ------- | ------------- | ------------ |
| `/main` | Main workflow | orchestrator |

---

## 🔗 Common Skills

This kit inherits from the **Common Skills Layer**. See `common/COMMON.md` for:

- `/filter` - Workspace-aware skill filtering

---
```

### Step 3: Create GEMINI.md

This file defines how AI should behave when using your kit:

```markdown
---
trigger: manual
---

# GEMINI.md - My Kit

> [Short description]

---

## 🎯 Kit Purpose

[Purpose description]

---

## 🤖 AGENT ROUTING

### Protocol

1. **Analyze**: Detect domain from user request
2. **Select**: Choose appropriate agent
3. **Announce**: `🤖 **Applying @[agent-name]...**`
4. **Apply**: Follow agent's rules

### Available Agents

| Agent          | Use When                 |
| -------------- | ------------------------ |
| `orchestrator` | Complex multi-step tasks |
| `specialist`   | Domain-specific work     |

---

## 📜 WORKFLOWS

| Command | Description   | Agent        |
| ------- | ------------- | ------------ |
| `/main` | Main workflow | orchestrator |

---

## 🛠️ SKILL LOADING
```

User Request → Match Skill → Load SKILL.md → Apply

```

### Skills

| Skill | Description |
| ----- | ----------- |
| `core-skill` | Primary domain skill |

---
```

### Step 4: Create Agent Files

Create `agents/orchestrator.md`:

```markdown
---
name: orchestrator
description: Main coordinator for My Kit
skills:
  - core-skill
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

---
```

### Step 5: Create Skill Files

Create `skills/core-skill/SKILL.md`:

```markdown
---
name: core-skill
description: Primary skill for My Kit
category: domain
trigger: auto
---

# Core Skill

> [One-line description]

---

## 🎯 Purpose

[Detailed purpose description]

---

## 📋 Guidelines

### Rule 1

[Description]

### Rule 2

[Description]

---

## 📊 Decision Framework

| Situation | Action |
| --------- | ------ |
| ...       | ...    |

---
```

### Step 6: Create Workflow Files

Create `workflows/main.md`:

```markdown
---
description: Main workflow for My Kit
---

# /main - Main Workflow

## Trigger

User calls `/main` or requests main functionality

## Agent

`orchestrator`

## Critical Rules

1. Rule 1
2. Rule 2

---

## Workflow Steps

### Step 1: [Name]
```

[Instructions]

```

### Step 2: [Name]

```

[Instructions]

```

---

## Output Format

[Expected output format]

---

## Exit Conditions

- Success condition
- Failure condition

---
```

### Step 7: Register Kit in CLI

Edit `src/config.ts`:

```typescript
export const KITS: Kit[] = [
  {
    id: "coder",
    name: "Coder Kit",
    description: "Complete toolkit for software development",
    path: "kits/coder",
  },
  // Add your new kit
  {
    id: "my-kit",
    name: "My Kit",
    description: "Description of my kit",
    path: "kits/my-kit",
  },
];
```

### Step 8: Test Your Kit

```bash
# Build CLI
pnpm build

# Test installation
node dist/cli.js

# Select your kit and verify it installs correctly
```

---

## 🤖 Adding Agents & Skills

### Inside an Existing Kit

Use the creator scripts if available:

```bash
# Add new agent
python3 kits/coder/skills/agent-creator/scripts/init_agent.py my-agent

# Add new skill
python3 kits/coder/skills/skill-creator/scripts/init_skill.py my-skill
```

### Manual Creation

Follow the templates in [Step 4](#step-4-create-agent-files) and [Step 5](#step-5-create-skill-files) above.

### Skill Quality Guidelines

| Criteria           | Requirement                                    |
| ------------------ | ---------------------------------------------- |
| Frontmatter        | YAML with name, description, category, trigger |
| Purpose            | Clear single-paragraph explanation             |
| Guidelines         | Actionable rules, not theory                   |
| Decision Framework | Tables for quick reference                     |
| Examples           | At least 1-2 real examples                     |

### Agent Quality Guidelines

| Criteria     | Requirement                               |
| ------------ | ----------------------------------------- |
| Frontmatter  | YAML with name, description, skills, tier |
| Role         | Clear responsibility definition           |
| Capabilities | Specific, measurable abilities            |
| When to Use  | Conditions for activation                 |

---

## 🧪 Testing

### Build the CLI

```bash
pnpm build
```

### Test Installation Locally

```bash
# Interactive mode
node dist/cli.js

# Or with arguments
node dist/cli.js --tool gemini --kit coder --path ./test-install
```

### Verify Kit Structure

Check that your kit has:

- [ ] `ARCHITECTURE.md` exists
- [ ] `GEMINI.md` exists
- [ ] At least one agent in `agents/`
- [ ] At least one skill in `skills/`
- [ ] At least one workflow in `workflows/`
- [ ] All files have proper frontmatter

---

## 📝 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feat/my-feature`
3. **Make** your changes
4. **Build** to verify: `pnpm build`
5. **Commit** with conventional format: `git commit -m "feat: add my-kit"`
6. **Push** to your fork: `git push origin feat/my-feature`
7. **Create** a Pull Request with:
   - Clear description of changes
   - Screenshots if applicable
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
- Frontmatter for all agent/skill/workflow files

### File Naming

| Type            | Convention    | Example          |
| --------------- | ------------- | ---------------- |
| Kit folder      | kebab-case    | `my-kit`         |
| Agent file      | kebab-case.md | `my-agent.md`    |
| Skill folder    | kebab-case    | `my-skill`       |
| Skill main file | UPPERCASE     | `SKILL.md`       |
| Workflow file   | kebab-case.md | `my-workflow.md` |

---

## ❓ Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

---

<p align="center">
  <sub>Thank you for contributing! 🙏</sub>
</p>
