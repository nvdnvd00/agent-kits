# AGT-Kit Architecture

> AI Agent Capability Expansion Toolkit

---

## 📋 Overview

AGT-Kit is a modular system consisting of:

- **Specialist Agents** - Role-based AI personas
- **Skills** - Domain-specific knowledge modules
- **Workflows** - Slash command procedures
- **Common Skills** - Universal skills shared across all kits

---

## 🔗 Common Skills

This kit inherits from the **Common Skills Layer**. See `COMMON.md` for full documentation.

| Skill          | Description                                              | Workflow  |
| -------------- | -------------------------------------------------------- | --------- |
| `filter-skill` | Analyze workspace and enable/disable skills by techstack | `/filter` |

### Usage

```bash
/filter    # Analyze workspace and recommend skill filtering
```

Common skills are automatically installed and available in all kits.

---

## 🏗️ Directory Structure

```plaintext
.agent/
├── ARCHITECTURE.md          # This file
├── agents/                  # Specialist Agents
├── skills/                  # Skills (knowledge modules)
├── workflows/               # Slash Commands
├── rules/                   # Global Rules
└── scripts/                 # Master Validation Scripts
```

---

## 🤖 Agents

Specialist AI personas for different domains.

### Tier 1: Master Agents

| Agent             | Focus                    | Skills Used                                            |
| ----------------- | ------------------------ | ------------------------------------------------------ |
| `orchestrator`    | Multi-agent coordination | clean-code, brainstorming, plan-writing, ui-ux-pro-max |
| `project-planner` | Smart project planning   | clean-code, plan-writing, brainstorming                |
| `debugger`        | Systematic debugging     | clean-code, systematic-debugging, testing-patterns     |

### Tier 2: Development Specialists

| Agent                 | Focus                                 | Skills Used                                                                                                                                      |
| --------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `frontend-specialist` | React/Next.js/Vue, UI/UX              | clean-code, react-patterns, typescript-patterns, tailwind-patterns, frontend-design, testing-patterns, seo-patterns, ui-ux-pro-max               |
| `backend-specialist`  | APIs, server logic, databases         | clean-code, nodejs-best-practices, api-patterns, database-design, graphql-patterns, redis-patterns                                               |
| `mobile-developer`    | React Native, Flutter, cross-platform | clean-code, mobile-design, testing-patterns, flutter-patterns, react-native-patterns, ui-ux-pro-max                                              |
| `database-specialist` | Schema design, queries, migrations    | clean-code, database-design, postgres-patterns, api-patterns                                                                                     |
| `devops-engineer`     | CI/CD, deployment, infrastructure     | clean-code, docker-patterns, kubernetes-patterns, github-actions, gitlab-ci-patterns, monitoring-observability, terraform-patterns, aws-patterns |

### Tier 3: Quality & Security

| Agent                 | Focus                            | Skills Used                                                    |
| --------------------- | -------------------------------- | -------------------------------------------------------------- |
| `security-auditor`    | OWASP 2025, supply chain, GenAI  | clean-code, security-fundamentals, api-patterns, auth-patterns |
| `code-reviewer`       | PR reviews, AI code validation   | clean-code, testing-patterns, security-fundamentals            |
| `test-engineer`       | TDD, testing pyramid, automation | clean-code, testing-patterns, e2e-testing                      |
| `performance-analyst` | Core Web Vitals, profiling       | clean-code, performance-profiling                              |

### Tier 4: Domain Specialists

| Agent                    | Focus                               | Skills Used                                                                                                     |
| ------------------------ | ----------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `realtime-specialist`    | WebSocket, Socket.IO, event-driven  | clean-code, api-patterns, realtime-patterns                                                                     |
| `multi-tenant-architect` | Tenant isolation, SaaS partitioning | multi-tenancy, clean-code, database-design, api-patterns                                                        |
| `queue-specialist`       | Message queues, background jobs     | queue-patterns, clean-code, api-patterns                                                                        |
| `integration-specialist` | External APIs, webhooks             | clean-code, api-patterns                                                                                        |
| `ai-engineer`            | LLM, RAG, AI/ML systems             | clean-code, ai-rag-patterns, prompt-engineering, api-patterns, database-design                                  |
| `cloud-architect`        | AWS, Azure, GCP, multi-cloud        | clean-code, kubernetes-patterns, docker-patterns, monitoring-observability, security-fundamentals, aws-patterns |
| `data-engineer`          | ETL, data pipelines, analytics      | clean-code, database-design, postgres-patterns, api-patterns                                                    |

### Tier 5: Support Agents

| Agent                  | Focus                              | Skills Used                                                        |
| ---------------------- | ---------------------------------- | ------------------------------------------------------------------ |
| `documentation-writer` | Technical docs, API docs, ADRs     | clean-code, documentation-templates, mermaid-diagrams              |
| `i18n-specialist`      | Internationalization, localization | clean-code, i18n-localization                                      |
| `ux-researcher`        | UX research, usability, a11y       | clean-code, frontend-design, accessibility-patterns, ui-ux-pro-max |

---

## 🧩 Skills (40)

Modular knowledge domains that agents can load on-demand based on task context.

### Core Skills

| Skill                      | Description                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `clean-code`               | Pragmatic coding standards. Naming, functions, structure, AI coding style. Used by ALL agents.               |
| `api-patterns`             | API design principles. REST/GraphQL/tRPC decision, response formats, versioning, pagination.                 |
| `database-design`          | Database design principles. Schema design, indexing strategy, ORM selection, migrations.                     |
| `testing-patterns`         | Testing patterns and principles. Unit, integration, mocking, TDD. Used by ALL agents.                        |
| `security-fundamentals`    | Security coding principles. OWASP 2025, input validation/sanitization, secure architecture.                  |
| `performance-profiling`    | Performance profiling principles. Core Web Vitals, measurement-first optimization, bottleneck analysis.      |
| `brainstorming`            | Socratic questioning protocol. User communication, requirements discovery, edge case exploration.            |
| `plan-writing`             | Structured task planning. WBS, task decomposition, estimation, plan file formats.                            |
| `systematic-debugging`     | 4-phase debugging methodology. Root cause analysis, hypothesis testing, evidence-based verification.         |
| `realtime-patterns`        | WebSocket, Socket.IO, event-driven architecture. Connection management, rooms, scaling.                      |
| `multi-tenancy`            | Multi-tenant architecture principles. Database isolation, context propagation, compliance patterns.          |
| `queue-patterns`           | Message queue and background job processing. Retry strategies, DLQ, idempotency, worker pools.               |
| `docker-patterns`          | Docker containerization principles. Multi-stage builds, security hardening, orchestration patterns.          |
| `kubernetes-patterns`      | Kubernetes orchestration principles. Manifests, Helm, deployments, services, GitOps patterns.                |
| `auth-patterns`            | Authentication and authorization principles. JWT, OAuth2, session management, RBAC, API security.            |
| `github-actions`           | GitHub Actions CI/CD patterns. Workflows, matrix builds, caching, secrets, security scanning.                |
| `gitlab-ci-patterns`       | GitLab CI/CD pipeline patterns. Multi-stage pipelines, caching, artifacts, security scanning, GitOps.        |
| `prompt-engineering`       | Prompt engineering principles for AI systems. Few-shot, chain-of-thought, agent personas, optimization.      |
| `react-patterns`           | React/Next.js performance and design patterns. Hooks, composition, Server Components, Vercel best practices. |
| `typescript-patterns`      | TypeScript advanced patterns. Branded types, conditional types, generics, monorepo config, tooling.          |
| `e2e-testing`              | E2E testing with Playwright/Cypress. Test design, reliability, CI integration, visual regression.            |
| `postgres-patterns`        | PostgreSQL-specific optimization. RLS, partitioning, JSONB, indexing, safe schema evolution.                 |
| `redis-patterns`           | Redis caching, pub/sub, sessions, rate limiting, distributed locking, leaderboards, memory management.       |
| `graphql-patterns`         | GraphQL API design. Schema patterns, DataLoader, N+1 prevention, subscriptions, federation, authorization.   |
| `ai-rag-patterns`          | RAG patterns for LLM apps. Vector DBs, chunking, retrieval, reranking, embeddings, evaluation.               |
| `monitoring-observability` | SRE patterns. Prometheus, Grafana, SLI/SLO, alerting, structured logging, distributed tracing.               |
| `terraform-patterns`       | Infrastructure as Code. Terraform/OpenTofu modules, state management, testing, CI/CD, security patterns.     |
| `flutter-patterns`         | Flutter with Dart 3, widget composition, state management (Riverpod, Bloc), multi-platform deployment.       |
| `react-native-patterns`    | React Native with Expo, navigation, native modules, offline-first architecture, EAS Build.                   |
| `seo-patterns`             | SEO fundamentals. E-E-A-T, Core Web Vitals, technical SEO, structured data, content optimization.            |
| `accessibility-patterns`   | WCAG compliance, inclusive design, keyboard navigation, screen readers, a11y testing.                        |
| `mermaid-diagrams`         | Mermaid diagram patterns. Flowcharts, sequence diagrams, ERDs, state diagrams, architecture visualization.   |
| `i18n-localization`        | Internationalization and localization. ICU format, RTL support, translation workflows, locale handling.      |
| `mobile-design`            | Mobile-first design thinking. Touch interaction, platform conventions, responsive layouts, gestures.         |
| `documentation-templates`  | Documentation templates. README, API docs, ADRs, changelog, code comments, technical writing.                |
| `tailwind-patterns`        | Tailwind CSS v4 patterns. Utility-first CSS, component patterns, responsive design, dark mode.               |
| `frontend-design`          | Web UI design thinking. Color theory, typography, spacing, layouts, micro-interactions, visual hierarchy.    |
| `ui-ux-pro-max`            | UI/UX design intelligence. 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines, 9 tech stacks. |
| `nodejs-best-practices`    | Node.js development principles. Express/Fastify patterns, async handling, error management, security.        |
| `aws-patterns`             | AWS CLI and Console patterns. IAM, S3, EC2, Lambda, CloudFormation, security best practices, automation.     |

---

## 🔄 Workflows (7)

Slash command procedures. Invoke with `/command`.

| Command          | Description                                                    |
| ---------------- | -------------------------------------------------------------- |
| `/plan`          | Project planning using project-planner agent. NO CODE output.  |
| `/create`        | Create new application with multi-agent orchestration.         |
| `/debug`         | Systematic debugging with 4-phase methodology.                 |
| `/test`          | Test generation and execution with test-engineer agent.        |
| `/deploy`        | Production deployment with pre-flight checks and verification. |
| `/orchestrate`   | Multi-agent coordination for complex tasks (minimum 3 agents). |
| `/ui-ux-pro-max` | UI/UX design intelligence with design system generation.       |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Execute scripts/ (if needed)
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

---

## 📜 Scripts

### Master Scripts (Global)

| Script                             | Purpose                          | When to Use                   |
| ---------------------------------- | -------------------------------- | ----------------------------- |
| `.agent/scripts/checklist.py`      | Run priority-ordered validations | Development, before PR        |
| `.agent/scripts/verify_all.py`     | Complete pre-deployment suite    | Before deploy, major releases |
| `.agent/scripts/kit_status.py`     | Report kit status & validation   | Kit health check, debugging   |
| `.agent/scripts/skills_manager.py` | Enable/disable/search skills     | Kit management                |

**Usage Examples:**

```bash
# Quick development check
python3 .agent/scripts/checklist.py .

# Full check with URL for performance
python3 .agent/scripts/checklist.py . --url http://localhost:3000

# Quick mode (Security, Lint, Tests only)
python3 .agent/scripts/checklist.py . --quick

# Full verification before deploy
python3 .agent/scripts/verify_all.py . --url http://localhost:3000

# Check kit status
python3 .agent/scripts/kit_status.py --validate

# Manage skills
python3 .agent/scripts/skills_manager.py list
python3 .agent/scripts/skills_manager.py search auth
python3 .agent/scripts/skills_manager.py info api-patterns
```

### Skill Scripts

| Skill                    | Script                                                  | Purpose                          |
| ------------------------ | ------------------------------------------------------- | -------------------------------- |
| `clean-code`             | `skills/clean-code/scripts/lint_runner.py`              | Unified linting (ESLint, Ruff)   |
| `testing-patterns`       | `skills/testing-patterns/scripts/test_runner.py`        | Test execution (Jest, Pytest)    |
| `security-fundamentals`  | `skills/security-fundamentals/scripts/security_scan.py` | OWASP-based security scan        |
| `database-design`        | `skills/database-design/scripts/schema_validator.py`    | Prisma/Drizzle schema validation |
| `api-patterns`           | `skills/api-patterns/scripts/api_validator.py`          | OpenAPI & API code validation    |
| `i18n-localization`      | `skills/i18n-localization/scripts/i18n_checker.py`      | Hardcoded strings & locale check |
| `seo-patterns`           | `skills/seo-patterns/scripts/seo_checker.py`            | SEO & GEO (AI citation) audit    |
| `accessibility-patterns` | `skills/accessibility-patterns/scripts/a11y_checker.py` | WCAG 2.2 compliance check        |

### Adding New Scripts

When adding scripts to skills:

1. Create in `skills/<skill-name>/scripts/`
2. Follow naming: `<action>_<target>.py` (e.g., `lint_runner.py`)
3. Include standard output (JSON + summary)
4. Return exit code 0 (pass) or 1 (fail)
5. Update this table and `checklist.py` if it's a core check

---

## 📊 Statistics

| Metric              | Value |
| ------------------- | ----- |
| **Total Agents**    | 22    |
| **Total Skills**    | 40    |
| **Total Workflows** | 7     |

---

## 🔗 Quick Reference

---

## 📝 Adding Components

### Add a Skill

1. Run `init_skill.py` or create manually
2. Complete SKILL.md with proper frontmatter
3. Add to this file's Skills table
4. Assign to relevant agent(s)
5. Run `test_skill.py` to verify (Grade B+)
6. Update Statistics

### Add an Agent

1. Create `.agent/agents/[agent-name].md`
2. Define skills in frontmatter
3. Add to this file's Agents table
4. Update GEMINI.md if major agent
5. Update Statistics

### Add a Workflow

1. Create `.agent/workflows/[workflow-name].md`
2. Add to this file's Workflows table
3. Update Statistics
