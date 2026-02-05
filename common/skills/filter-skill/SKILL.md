---
name: filter-skill
description: Automatically analyze workspace and enable/disable skills/agents based on detected techstack. Reduces noise from irrelevant skills.
category: common
trigger: manual
workflow: /filter
---

# Filter Skill

> Workspace-aware skill/agent filtering for optimal AI performance.

---

## 🎯 Purpose

Filter Skill solves the **skill overload** problem - when too many skills are loaded but aren't relevant to the current project. This skill:

1. **Analyzes techstack** of the workspace
2. **Recommends enable/disable** for skills/agents
3. **Asks user confirmation** before applying changes
4. **Persists profile** for use in subsequent sessions

---

## 🔍 Detection Criteria

### Package Managers & Config Files

| File/Pattern       | Detected Techstack                      |
| ------------------ | --------------------------------------- |
| `package.json`     | Node.js, check dependencies for details |
| `pubspec.yaml`     | Flutter/Dart                            |
| `pyproject.toml`   | Python (Poetry/PDM)                     |
| `requirements.txt` | Python (pip)                            |
| `Cargo.toml`       | Rust                                    |
| `go.mod`           | Go                                      |
| `build.gradle`     | Android (Java/Kotlin)                   |
| `Podfile`          | iOS                                     |
| `composer.json`    | PHP                                     |
| `Gemfile`          | Ruby                                    |

### Framework Markers

| File/Pattern           | Framework        | Enable Skills                                 |
| ---------------------- | ---------------- | --------------------------------------------- |
| `next.config.*`        | Next.js          | react-patterns, frontend-design, seo-patterns |
| `vite.config.*`        | Vite             | react-patterns, frontend-design               |
| `angular.json`         | Angular          | typescript-patterns, frontend-design          |
| `nuxt.config.*`        | Nuxt.js          | frontend-design, seo-patterns                 |
| `tailwind.config.*`    | Tailwind CSS     | tailwind-patterns                             |
| `prisma/schema.prisma` | Prisma           | database-design, postgres-patterns            |
| `drizzle.config.*`     | Drizzle          | database-design                               |
| `docker-compose.*`     | Docker           | docker-patterns                               |
| `Dockerfile`           | Docker           | docker-patterns                               |
| `k8s/`, `kubernetes/`  | Kubernetes       | kubernetes-patterns                           |
| `.github/workflows/`   | GitHub Actions   | github-actions                                |
| `.gitlab-ci.yml`       | GitLab CI        | gitlab-ci-patterns                            |
| `terraform/`, `*.tf`   | Terraform        | terraform-patterns                            |
| `socket.io`, `ws`      | WebSocket (deps) | realtime-patterns                             |
| `bullmq`, `bee-queue`  | Queue (deps)     | queue-patterns                                |

### Dependency Analysis (package.json)

| Dependency Pattern      | Enable Skills                       |
| ----------------------- | ----------------------------------- |
| `react`, `react-dom`    | react-patterns                      |
| `next`                  | react-patterns, seo-patterns        |
| `@tanstack/react-query` | react-patterns                      |
| `graphql`, `@apollo`    | graphql-patterns                    |
| `redis`, `ioredis`      | redis-patterns                      |
| `pg`, `postgres`        | postgres-patterns                   |
| `socket.io*`            | realtime-patterns                   |
| `bullmq`, `bee-queue`   | queue-patterns                      |
| `passport`, `@auth`     | auth-patterns                       |
| `openai`, `langchain`   | ai-rag-patterns, prompt-engineering |
| `playwright`            | e2e-testing                         |
| `cypress`               | e2e-testing                         |
| `jest`, `vitest`        | testing-patterns                    |
| `eslint`, `prettier`    | clean-code                          |

---

## 📋 Workflow Steps

### Phase 1: Analysis

```plaintext
1. Scan workspace root for config files
2. Parse package managers (package.json, pubspec.yaml, etc.)
3. Detect framework markers
4. Analyze dependencies
5. Build techstack profile
```

### Phase 2: Recommendation

```plaintext
1. Map techstack → required skills/agents
2. Identify unused skills (candidates for disable)
3. Identify missing skills (candidates for enable)
4. Generate recommendation table
```

### Phase 3: User Confirmation

AI will ask the user:

```markdown
## 🔍 Workspace Analysis Complete

**Detected Techstack:**

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Prisma + PostgreSQL
- Redis

**Recommended Skills (Enable):**
| Skill | Reason |
|-------|--------|
| react-patterns | Next.js detected |
| tailwind-patterns | tailwind.config.js found |
| postgres-patterns | Prisma with PostgreSQL |
| redis-patterns | ioredis in dependencies |

**Recommended to Disable:**
| Skill | Reason |
|-------|--------|
| flutter-patterns | No pubspec.yaml |
| react-native-patterns | No mobile setup |
| queue-patterns | No queue dependencies |

**Questions:**

1. Do you want to apply these changes?
2. Are there any techstacks you plan to add in the future? (e.g., mobile, CI/CD)
3. Are there any skills you want to force enable/disable?
```

### Phase 4: Apply & Persist

```plaintext
1. Update .agent/workspace-profile.json
2. (Optional) Update ARCHITECTURE.md skills section
3. Confirm changes to user
```

---

## 📄 Workspace Profile Format

```json
{
  "version": "1.0",
  "generatedAt": "2026-02-05T12:00:00Z",
  "techstack": {
    "languages": ["typescript", "python"],
    "frameworks": ["nextjs", "tailwindcss"],
    "databases": ["postgresql"],
    "tools": ["docker", "github-actions"]
  },
  "skills": {
    "enabled": [
      "clean-code",
      "react-patterns",
      "typescript-patterns",
      "tailwind-patterns",
      "database-design",
      "postgres-patterns",
      "docker-patterns",
      "github-actions"
    ],
    "disabled": [
      "flutter-patterns",
      "react-native-patterns",
      "mobile-design",
      "queue-patterns",
      "gitlab-ci-patterns"
    ],
    "userOverrides": {
      "force-enabled": ["ai-rag-patterns"],
      "force-disabled": []
    }
  },
  "agents": {
    "disabled": ["mobile-developer", "queue-specialist"]
  },
  "futureTechstack": ["react-native", "kubernetes"]
}
```

---

## 🚫 Never Disable (Core Skills)

These skills are ALWAYS enabled regardless of techstack:

- `clean-code`
- `brainstorming`
- `plan-writing`
- `systematic-debugging`
- `testing-patterns`
- `security-fundamentals`

---

## 🔧 Manual Override

User can override any recommendation:

```markdown
/filter --force-enable ai-rag-patterns
/filter --force-disable mobile-design
/filter --reset # Reset to default (enable all)
```

---

## 📊 Integration Points

### With GEMINI.md / CLAUDE.md

Rule files should check `workspace-profile.json` when loading skills:

```markdown
## Skill Loading Protocol

1. Check if `.agent/workspace-profile.json` exists
2. If exists, respect enabled/disabled lists
3. Core skills always loaded regardless of profile
```

### With Orchestrator

Orchestrator agent should respect skill filtering when routing tasks.

---

## ⚠️ Limitations

1. **Static analysis only** - Does not execute code to detect
2. **Config-based** - Relies on config files, may miss dynamic setups
3. **Monorepo** - Needs improvement to handle multiple packages

---
