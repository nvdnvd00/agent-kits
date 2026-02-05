# Templates Directory

> AI Tool-specific structure templates for the Agent Kits installer.

---

## 📋 Overview

This directory contains **target structure templates** for each supported AI tool. The installer uses these templates to:

1. **Understand target structure** - Where files should be placed
2. **Transform content** - Convert agent/skill format to tool-specific format
3. **Validate installation** - Ensure correct structure after install

---

## 🗂️ Directory Structure

```plaintext
templates/
├── cursor/
│   ├── STRUCTURE.md          # Target structure documentation
│   └── transforms/
│       └── agent.template.md  # Agent transformation template
├── antigravity/
│   ├── STRUCTURE.md
│   └── transforms/
│       └── agent.template.md
└── README.md                  # This file
```

---

## 🔧 Supported AI Tools

| Tool        | Status    | Template       | Notes                                           |
| ----------- | --------- | -------------- | ----------------------------------------------- |
| Cursor      | ✅ Active | `cursor/`      | Subagents format, commands instead of workflows |
| Antigravity | ✅ Active | `antigravity/` | Standard format, no transformation needed       |
| Claude Code | 🔜 Coming | -              | -                                               |
| Gemini CLI  | 🔜 Coming | -              | -                                               |
| Codex CLI   | 🔜 Coming | -              | -                                               |

---

## 📝 Adding New AI Tool Template

### Step 1: Create folder structure

```bash
mkdir -p templates/<tool-name>/transforms
```

### Step 2: Create STRUCTURE.md

Document the target structure:

```markdown
# <Tool Name> Structure

## Target Directory Layout

\`\`\`plaintext
.<tool-folder>/
├── rules/
│ └── rules.md
├── agents/
└── skills/
\`\`\`

## Transformation Rules

[Document any content transformations needed]
```

### Step 3: Create transform templates (if needed)

If the tool requires content transformation (like Cursor's subagent format), create template files in `transforms/`:

- `agent.template.md` - Agent file transformation
- `skill.template.md` - Skill file transformation (if different)

### Step 4: Update installer

Add corresponding installer in `src/installers/<tool>.ts`

---

## 🔄 Transformation Process

```
Kit Source Files
       ↓
  [Installer]
       ↓
  [Transformer] ← Uses templates/
       ↓
Target AI Tool Structure
```

---

## 📎 Related Files

- [KIT_SPEC.md](../docs/KIT_SPEC.md) - Kit specification
- [src/installers/](../src/installers/) - Installer implementations
- [src/transformers/](../src/transformers/) - Transformation logic
