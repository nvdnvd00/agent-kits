# Common Skills Layer

> Universal skills shared across ALL kits in @neyugn/agent-kits

---

## 🎯 Purpose

The Common Skills Layer contains special skills that are shared across **all kits**. These skills:

1. **Installed with every kit** - When a user installs any kit (coder, writer, etc.), common skills are installed automatically
2. **Referenced in ARCHITECTURE.md** - Each kit's architecture document mentions these skills
3. **Have dedicated workflows** - Invoked only when user calls the corresponding slash command

---

## 📁 Directory Structure

```plaintext
common/
├── COMMON.md                    # This file - documentation
├── skills/                      # Common skills
│   ├── scan-techstack/          # Techstack detection skill
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── techstack_scanner.py
│   ├── filter-skill/            # Skill filtering skill
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── workspace_analyzer.py
│   └── filter-agent/            # Agent filtering skill
│       └── SKILL.md
└── workflows/                   # Common workflows
    └── filter.md                # /filter command
```

---

## 🧩 Common Skills

| Skill            | Description                                             | Trigger                |
| ---------------- | ------------------------------------------------------- | ---------------------- |
| `scan-techstack` | Analyze workspace to detect technologies and frameworks | Part of `/filter` flow |
| `filter-skill`   | Recommend enable/disable skills based on techstack      | Part of `/filter` flow |
| `filter-agent`   | Recommend disable agents based on techstack             | Part of `/filter` flow |

---

## 🔄 How It Works

### Installation

When user runs `npx @neyugn/agent-kits`:

1. User selects a kit (e.g., `coder`)
2. Installer copies kit to workspace
3. Installer copies `common/` skills to the same location
4. Common skills are merged into the kit's architecture

### Usage

```bash
# User invokes workflow to filter skills and agents
/filter

# The workflow will:
# 1. scan-techstack: Analyze workspace (package.json, pubspec.yaml, etc.)
# 2. filter-skill: Recommend skill enable/disable based on techstack
# 3. filter-agent: Recommend agent disable based on techstack
# 4. Ask user confirmation + future techstack plans
# 5. Save results to .agent/profile.json
```

### Workflow Flow

```
/filter
  │
  ├── Step 1: scan-techstack
  │   └── Output: TechstackProfile (languages, frameworks, categories)
  │
  ├── Step 2: filter-skill
  │   └── Output: SkillRecommendations (enable/disable lists)
  │
  ├── Step 3: filter-agent
  │   └── Output: AgentRecommendations (disable list)
  │
  ├── Step 4: User Confirmation
  │   └── Ask about future techstack plans
  │
  └── Step 5: Save to profile.json
```

---

## 📊 Integration with Kits

Each kit's `ARCHITECTURE.md` MUST mention:

```markdown
## 🔗 Common Skills

This kit inherits from the **Common Skills Layer**. See `common/COMMON.md` for:

- `/filter` - Workspace-aware skill and agent filtering
  - `scan-techstack` - Techstack detection
  - `filter-skill` - Skill recommendations
  - `filter-agent` - Agent recommendations

Common skills are automatically installed and available in all kits.
```

---

## 📄 Profile Format

The `/filter` workflow saves results to `.agent/profile.json`:

```json
{
  "version": "1.0",
  "generatedAt": "2026-02-05T12:00:00Z",
  "analyzedBy": "filter-workflow v1.0",
  "techstack": {
    "languages": ["typescript", "python"],
    "frameworks": ["nextjs", "tailwindcss"],
    "databases": ["postgresql"],
    "tools": ["docker", "github-actions"]
  },
  "skills": {
    "enabled": ["react-patterns", "tailwind-patterns", "postgres-patterns"],
    "disabled": ["flutter-patterns", "mobile-design", "queue-patterns"],
    "userOverrides": {
      "force-enabled": ["ai-rag-patterns"],
      "force-disabled": []
    }
  },
  "agents": {
    "disabled": ["mobile-developer", "queue-specialist", "realtime-specialist"]
  },
  "futureTechstack": ["react-native", "kubernetes"]
}
```

---

## 🚀 Future Common Skills (Planned)

| Skill             | Description                                   | Status  |
| ----------------- | --------------------------------------------- | ------- |
| `context-manager` | Manage context length, auto-summarize history | Planned |
| `memory-skill`    | Store and recall important information        | Planned |
| `preference-sync` | Sync user preferences between sessions        | Planned |

---

## 📝 Adding Common Skills

1. Create skill folder in `common/skills/`
2. Create SKILL.md with proper frontmatter
3. (Optional) Create scripts/ for automation
4. Update workflow in `common/workflows/` if needed
5. Update this file's Skills table
6. Update all kits' ARCHITECTURE.md to reference

---
