---
name: scan-techstack
description: Analyze workspace to detect technologies, frameworks, and dependencies. Provides structured techstack profile for other skills (filter-skill, filter-agent).
category: common
trigger: manual
---

# Scan Techstack Skill

> Workspace technology detection and profiling.

---

## 🎯 Purpose

Scan Techstack is the **first step** in the filtering workflow. It:

1. **Scans workspace** for config files, package managers, and framework markers
2. **Parses dependencies** from package.json, pubspec.yaml, etc.
3. **Builds techstack profile** as structured output
4. **Provides data** for filter-skill and filter-agent to process

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

| File/Pattern           | Framework      | Category |
| ---------------------- | -------------- | -------- |
| `next.config.*`        | Next.js        | Frontend |
| `vite.config.*`        | Vite           | Frontend |
| `angular.json`         | Angular        | Frontend |
| `nuxt.config.*`        | Nuxt.js        | Frontend |
| `tailwind.config.*`    | Tailwind CSS   | Styling  |
| `prisma/schema.prisma` | Prisma         | Database |
| `drizzle.config.*`     | Drizzle        | Database |
| `docker-compose.*`     | Docker         | DevOps   |
| `Dockerfile`           | Docker         | DevOps   |
| `k8s/`, `kubernetes/`  | Kubernetes     | DevOps   |
| `.github/workflows/`   | GitHub Actions | CI/CD    |
| `.gitlab-ci.yml`       | GitLab CI      | CI/CD    |
| `terraform/`, `*.tf`   | Terraform      | IaC      |

### Dependency Analysis (package.json)

| Dependency Pattern      | Detected Category   |
| ----------------------- | ------------------- |
| `react`, `react-dom`    | React ecosystem     |
| `next`                  | Next.js (SSR/SSG)   |
| `@tanstack/react-query` | React data fetching |
| `graphql`, `@apollo`    | GraphQL             |
| `redis`, `ioredis`      | Redis cache         |
| `pg`, `postgres`        | PostgreSQL          |
| `socket.io*`            | Real-time/WebSocket |
| `bullmq`, `bee-queue`   | Message queues      |
| `passport`, `@auth`     | Authentication      |
| `openai`, `langchain`   | AI/LLM              |
| `playwright`, `cypress` | E2E testing         |
| `jest`, `vitest`        | Unit testing        |

---

## 📋 Output Format

The scan produces a **TechstackProfile** object:

```json
{
  "success": true,
  "analyzedAt": "2026-02-05T12:00:00Z",
  "workspacePath": "/path/to/project",
  "detection": {
    "configFiles": ["package.json", "next.config.js", "tailwind.config.js"],
    "languages": ["typescript", "javascript"],
    "frameworks": ["nextjs", "tailwindcss"],
    "databases": ["postgresql"],
    "tools": ["docker", "github-actions"],
    "dependencies": {
      "npm": ["react", "next", "tailwindcss", "prisma", "@tanstack/react-query"]
    }
  },
  "categories": {
    "frontend": true,
    "backend": true,
    "mobile": false,
    "database": true,
    "devops": true,
    "ai": false,
    "realtime": false,
    "queue": false
  }
}
```

---

## 🔧 Usage

### As Part of /filter Workflow (Recommended)

```bash
/filter
# Step 1: scan-techstack runs automatically
# Step 2: filter-skill uses scan results
# Step 3: filter-agent uses scan results
```

### Standalone (Debug/Verify)

```bash
# Run script directly
python3 .agent/skills/scan-techstack/scripts/techstack_scanner.py .

# AI can also scan manually
/scan-techstack
```

---

## 📊 Category Detection Rules

| Category   | Detected When                                          |
| ---------- | ------------------------------------------------------ |
| `frontend` | React, Vue, Angular, Next.js, Nuxt, Tailwind detected  |
| `backend`  | Express, Fastify, NestJS, FastAPI, or API deps found   |
| `mobile`   | Flutter, React Native, iOS (Podfile), Android (Gradle) |
| `database` | Prisma, Drizzle, pg, mongodb, redis detected           |
| `devops`   | Docker, Kubernetes, Terraform, CI/CD configs found     |
| `ai`       | OpenAI, LangChain, or AI-related deps detected         |
| `realtime` | Socket.IO, WebSocket dependencies found                |
| `queue`    | BullMQ, RabbitMQ, or queue dependencies found          |

---

## ⚠️ Limitations

1. **Static analysis only** - Does not execute code
2. **Config-based** - Relies on config files, may miss dynamic setups
3. **Monorepo support** - Basic support, scans root only
4. **Package manager focus** - Best support for npm/yarn, basic for others

---

## 🔗 Integration

This skill is a **dependency** for:

- `filter-skill` - Uses techstack to recommend skill enable/disable
- `filter-agent` - Uses techstack to recommend agent disable

---
