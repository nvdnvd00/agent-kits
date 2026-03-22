<p align="center">
  <img src="./assets/logo.svg" width="200" alt="Agent Kits Logo" />
</p>

<h1 align="center">Agent Kits</h1>

<p align="center">
  <b>Universal AI Agent Toolkit</b><br/>
  <sub>Skills, Agents, and Workflows for any AI coding assistant</sub>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/v/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm version" /></a>
  <a href="https://www.npmjs.com/package/@neyugn/agent-kits"><img src="https://img.shields.io/npm/dm/@neyugn/agent-kits?style=flat-square&color=00ADD8" alt="npm downloads" /></a>
  <a href="https://github.com/nvdnvd00/agent-kits/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="license" /></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-cli-commands">CLI Commands</a> •
  <a href="#-important-notes">Important Notes</a> •
  <a href="#-features">Features</a> •
  <a href="#-kits">Kits</a> •
  <a href="#-filter-skill">Filter Skill</a> •
  <a href="#-documentation">Documentation</a>
</p>

<p align="center">
  <b>English</b> •
  <a href="./README.vi.md">Tiếng Việt</a> •
  <a href="./README.zh.md">中文</a>
</p>

<br/>

## ✨ What is Agent Kits?

**Agent Kits** is a universal toolkit that supercharges your AI coding assistant with:

- 🤖 **Specialist Agents** — Pre-defined personas with deep domain expertise
- 🧩 **Reusable Skills** — Best practices and decision frameworks
- 📜 **Workflows** — Slash commands for common tasks
- 🔍 **Smart Filtering** — Auto-detect techstack and optimize loaded skills

Works with **any AI tool** — Claude, Gemini, Codex, Cursor, OpenCode, and more.

<br/>

## 🚀 Quick Start

```bash
npx @neyugn/agent-kits@latest
```

That's it! The interactive installer will guide you through:

1. Selecting your AI tool (Claude, Gemini, Cursor, etc.)
2. Choosing installation scope (Global or Workspace)
3. Selecting which kits to install
4. Confirming the installation path

<br/>

## 🖥️ CLI Commands

```bash
npx @neyugn/agent-kits              # Start interactive setup wizard
npx @neyugn/agent-kits --check-updates  # Check for new version
npx @neyugn/agent-kits --version        # Show current version
npx @neyugn/agent-kits --help            # Show help
```

**Example output when update is available:**

```
╭─────────────────────────╮
│  agent-kits v0.5.0     │
│  Latest:   v0.6.0      │
╰─────────────────────────╯

  ⚠ Update available! Run below to update:
  npx @neyugn/agent-kits@latest
```

<br/>

## 📌 Important Notes

### Slash commands not appearing in IDE dropdown

If `.agent/` (or `.cursor/`, `.opencode/`, etc.) is listed in `.gitignore`, some IDEs will skip indexing files inside it — including the `workflows/` folder that powers slash commands like `/plan`, `/debug`, `/create`.

**Fix:** Add a negation rule to force-include the workflows folder:

```gitignore
# Ignore the kit folder (optional)
.agent/

# But always index workflows so slash commands work in the IDE
!.agent/workflows/
!.agent/workflows/**
```

> **Recommended:** Remove the kit folder from `.gitignore` entirely and commit it. This is the preferred approach for workspace installations.

<br/>

### 🌍 Global vs Workspace Installation

| Mode         | Location      | Use Case                       |
| ------------ | ------------- | ------------------------------ |
| 📁 Workspace | `./{{tool}}/` | Project-specific configuration |
| 🌍 Global    | `~/{{tool}}/` | Shared across all projects     |

**Global Paths by Tool:**

| Tool        | Global Path           | Workspace Path |
| ----------- | --------------------- | -------------- |
| Claude Code | `~/.claude/`          | `.claude/`     |
| Gemini CLI  | `~/.gemini/`          | `.gemini/`     |
| Codex CLI   | `~/.codex/`           | `.codex/`      |
| Antigravity | `~/.agent/`           | `.agent/`      |
| OpenCode    | `~/.config/opencode/` | `.opencode/`   |
| Cursor      | `~/.cursor/`          | `.cursor/`     |

> **Note:** On Windows, `~` is replaced with `C:\Users\<username>\`

### 🔄 Existing Installation Detection

If the installer detects an existing installation, you'll be prompted:

- **🔄 Replace**: Remove existing and install fresh
- **🔀 Merge**: Keep config files, update skills only
- **⏭️ Skip**: Keep existing, don't install
- **❌ Cancel**: Exit installer

### 🔌 Universal Compatibility

| Tool        | Workspace Path    | Global Path           | Status             |
| ----------- | ----------------- | --------------------- | ------------------ |
| Antigravity | `.agent/skills/`  | `~/.agent/`           | ✅ Fully Supported |
| OpenCode    | `.opencode/`      | `~/.config/opencode/` | ✅ Fully Supported |
| Cursor      | `.cursor/skills/` | `~/.cursor/`          | ✅ Fully Supported |
| Claude Code | `.claude/skills/` | `~/.claude/`          | 🔜 Coming Soon     |
| Gemini CLI  | `.gemini/skills/` | `~/.gemini/`          | 🔜 Coming Soon     |
| Codex CLI   | `.codex/skills/`  | `~/.codex/`           | 🔜 Coming Soon     |
| Custom      | Configurable      | `~/.ai/`              | 🔜 Coming Soon     |

> **Note:** Tools marked as 🔜 Coming Soon are planned for future releases. The infrastructure is ready, but these tools require additional testing and configuration.

### 💻 Cross-Platform Support

Works on **Windows**, **macOS**, and **Linux** with automatic path adaptation:

| Platform | Example Global Path          |
| -------- | ---------------------------- |
| Windows  | `C:\Users\username\.claude\` |
| macOS    | `/Users/username/.claude/`   |
| Linux    | `/home/username/.claude/`    |

<br/>

## 🔍 Smart Filter (Workspace Analysis)

The **Filter** feature is the "brain" of Agent Kits, ensuring your AI assistant stays sharp and focused. Instead of overwhelming the AI with dozens of irrelevant instructions (skills), the system automatically analyzes your workspace to enable only what’s necessary.

### Why use Filtering?

As projects grow complex, providing too many instructions (System Prompts) to an AI can lead to:
- **Context Bloat**: Makes AI prone to confusion and slower responses.
- **Lost Focus**: AI might suggest patterns from one framework for another (e.g., suggesting Tailwind v4 patterns in a project using CSS Modules).
- **Token Waste**: Sending redundant instructions increases API costs.

### How `/filter` Works

The system uses a multi-layered scanning mechanism to provide the best recommendations:

1.  **Techstack Detection**: Scans project identifiers (`package.json`, `go.mod`, `requirements.txt`, `composer.json`, `Cargo.toml`, etc.).
2.  **Structural Analysis**: Checks for characteristic directories (`src/app` for Next.js App Router, `android/` for Mobile, etc.).
3.  **Agent & Skill Mapping**: Matches the detected techstack against the Agent Kits library to select the most relevant Specialists (Agents) and capabilities (Skills).
4.  **Profile Tuning**: Creates or updates a `.agent/profile.json` file to precisely configure what the AI can access.

### Example Analysis Report

```markdown
## 🔍 Workspace Analysis: E-commerce Project (Next.js + NestJS)

**Detected Techstack:**
- Frontend: `Next.js 14`, `Tailwind CSS`, `Zustand`
- Backend: `NestJS`, `PostgreSQL`, `Prisma`
- DevOps: `Docker`, `GitHub Actions`

**✅ Activated Agents (Specialists):**
- `frontend-specialist`: Optimized for Next.js and Tailwind.
- `backend-specialist`: Expert in NestJS architecture.
- `database-specialist`: Advanced Prisma query optimization.
- `devops-engineer`: Manages Docker and CI/CD pipelines.

**🧩 Loaded Skills:**
- `react-patterns`, `tailwind-patterns`, `nodejs-best-practices`, `postgres-patterns`, `docker-patterns`.

**🚫 Hidden Skills (To reduce noise):**
- `flutter-patterns`, `mobile-design`, `aws-patterns` (Not used in this project).
```

### Control Commands

```bash
/filter                           # Re-scan workspace and auto-update
/filter --force-enable ai-rag     # Always enable RAG skill regardless of techstack
/filter --force-disable mobile    # Always disable mobile-related skills
/filter --reset                   # Reset to default state (enable all)
```

### Core Skills (Always Ready)

Certain fundamental skills and core Agents are never disabled to maintain system-level reasoning:

| Skill | Value Proposition |
| :--- | :--- |
| `clean-code` | Ensures code is clean and maintainable. |
| `brainstorming` | Activates Socratic reasoning for complex problem solving. |
| `plan-writing` | Detailed planning before any code implementation. |
| `systematic-debugging` | 4-step evidence-based debugging process. |
| `security-fundamentals` | OWASP 2025 compliant security checks. |

<br/>

## 📦 Kits

### 💻 Coder Kit

Complete toolkit for software development with **22 specialist agents**, **40 skills**, and **7 workflows**.

<details>
<summary><b>🤖 Agents (22)</b></summary>

#### Tier 1: Master Agents

| Agent             | Description              |
| ----------------- | ------------------------ |
| `orchestrator`    | Multi-agent coordination |
| `project-planner` | Smart project planning   |
| `debugger`        | Systematic debugging     |

#### Tier 2: Development Specialists

| Agent                 | Description                |
| --------------------- | -------------------------- |
| `frontend-specialist` | React, Next.js, Vue, UI/UX |
| `backend-specialist`  | APIs, Node.js, Python      |
| `mobile-developer`    | React Native, Flutter      |
| `database-specialist` | Schema design, queries     |
| `devops-engineer`     | CI/CD, deployment          |

#### Tier 3: Quality & Security

| Agent                 | Description                 |
| --------------------- | --------------------------- |
| `security-auditor`    | OWASP 2025, vulnerabilities |
| `code-reviewer`       | PR reviews, code quality    |
| `test-engineer`       | TDD, testing pyramid        |
| `performance-analyst` | Core Web Vitals, profiling  |

#### Tier 4: Domain Specialists

| Agent                    | Description                     |
| ------------------------ | ------------------------------- |
| `realtime-specialist`    | WebSocket, Socket.IO            |
| `multi-tenant-architect` | Tenant isolation, SaaS          |
| `queue-specialist`       | Message queues, background jobs |
| `integration-specialist` | External APIs, webhooks         |
| `ai-engineer`            | LLM, RAG, AI/ML systems         |
| `cloud-architect`        | AWS, Azure, GCP, Terraform      |
| `data-engineer`          | ETL, pipelines, analytics       |

#### Tier 5: Support Agents

| Agent                  | Description              |
| ---------------------- | ------------------------ |
| `documentation-writer` | Technical docs, API docs |
| `i18n-specialist`      | Internationalization     |
| `ux-researcher`        | UX research, usability   |

</details>

<details>
<summary><b>🧩 Skills (40)</b></summary>

**Core Skills:**
| Skill | Description |
| ----------------------- | ----------------------------- |
| `clean-code` | Pragmatic coding standards |
| `api-patterns` | REST/GraphQL/tRPC decisions |
| `database-design` | Schema design, indexing |
| `testing-patterns` | Unit, integration, E2E |
| `security-fundamentals` | OWASP 2025, secure coding |
| `performance-profiling` | Core Web Vitals, optimization |

**Process Skills:**
| Skill | Description |
| ----------------------- | ----------------------------- |
| `brainstorming` | Socratic questioning protocol |
| `plan-writing` | Task breakdown, WBS |
| `systematic-debugging` | 4-phase debugging |

**Domain Skills (31):** `react-patterns`, `typescript-patterns`, `docker-patterns`, `kubernetes-patterns`, `terraform-patterns`, `auth-patterns`, `graphql-patterns`, `redis-patterns`, `realtime-patterns`, `queue-patterns`, `multi-tenancy`, `ai-rag-patterns`, `prompt-engineering`, `monitoring-observability`, `frontend-design`, `mobile-design`, `tailwind-patterns`, `e2e-testing`, `github-actions`, `gitlab-ci-patterns`, `flutter-patterns`, `react-native-patterns`, `seo-patterns`, `accessibility-patterns`, `mermaid-diagrams`, `i18n-localization`, `postgres-patterns`, `nodejs-best-practices`, `documentation-templates`, `ui-ux-pro-max`, `aws-patterns`

</details>

<details>
<summary><b>📜 Workflows (7)</b></summary>

| Command          | Description                   |
| ---------------- | ----------------------------- |
| `/plan`          | Create project plan (no code) |
| `/create`        | Build new application         |
| `/debug`         | Systematic debugging          |
| `/test`          | Generate and run tests        |
| `/deploy`        | Production deployment         |
| `/orchestrate`   | Multi-agent coordination      |
| `/ui-ux-pro-max` | UI/UX design intelligence     |

> **Note:** The `/filter` command is part of **Common Skills Layer** (see below) and available in all kits.

</details>

### 🔜 Coming Soon

| Kit               | Description                   | Status            |
| ----------------- | ----------------------------- | ----------------- |
| ✍️ **Writer**     | Content creation, copywriting | 🚧 In Development |
| 🔬 **Researcher** | Research, analysis, synthesis | 📋 Planned        |
| 🎨 **Designer**   | UI/UX design, branding        | 📋 Planned        |

<br/>

## 🛠️ Usage

### Using Agents

Reference agents with `@agent-name`:

```markdown
@backend-specialist design an API for user management
@security-auditor review this authentication code
@test-engineer write tests for the payment service
```

### Using Workflows

Invoke workflows with slash commands:

```bash
/plan my new e-commerce site     # Create project plan
/create todo app                 # Build application
/debug login not working         # Fix bugs
/test user service               # Generate tests
/filter                          # Optimize skills for workspace
```

<br/>

## 📚 Documentation

After installation, find documentation in your project:

- **Architecture Guide**: `<path>/ARCHITECTURE.md`
- **Agent Details**: `<path>/agents/*.md`
- **Skill Guides**: `<path>/skills/*/SKILL.md`
- **Workflow Docs**: `<path>/workflows/*.md`
- **Common Skills**: `common/COMMON.md`

<br/>

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on:

- Creating new kits
- Adding agents and skills
- Submitting pull requests

<br/>

## 📄 License

MIT © [Neos](https://github.com/nvdnvd00)

---

<p align="center">
  <sub>Built with ❤️ for the AI-assisted development community</sub>
</p>
