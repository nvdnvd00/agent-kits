---
name: filter-skill
description: Recommend enabling/disabling skills based on detected techstack. Reduces noise from irrelevant skills in the workspace.
category: common
trigger: manual
workflow: /filter
---

# Filter Skill

> Workspace-aware skill filtering for optimal AI performance.

---

## 🎯 Purpose

Filter Skill analyzes the **techstack profile** (from scan-techstack) and recommends which skills to **enable/disable** based on project needs. This:

1. **Reduces noise** - Only relevant skills are loaded
2. **Improves context** - AI focuses on applicable patterns
3. **Optimizes performance** - Less skill content to process

---

## 🔗 Dependency

This skill requires **scan-techstack** to run first:

```
/filter workflow:
  1. scan-techstack → detect techstack
  2. filter-skill → recommend skills (this skill)
  3. filter-agent → recommend agents
```

---

## 📋 Skill Categories

### Core Skills (NEVER DISABLE)

These skills are ALWAYS enabled regardless of techstack:

| Skill                   | Reason                        |
| ----------------------- | ----------------------------- |
| `clean-code`            | Universal coding standards    |
| `brainstorming`         | Socratic questioning protocol |
| `plan-writing`          | Task breakdown and WBS        |
| `systematic-debugging`  | 4-phase debugging methodology |
| `testing-patterns`      | Testing pyramid, AAA pattern  |
| `security-fundamentals` | OWASP 2025 security basics    |

### Frontend Skills

| Skill                    | Enable When                     |
| ------------------------ | ------------------------------- |
| `react-patterns`         | React/Next.js detected          |
| `typescript-patterns`    | TypeScript detected             |
| `tailwind-patterns`      | Tailwind CSS detected           |
| `frontend-design`        | Any frontend framework          |
| `seo-patterns`           | Next.js, Nuxt.js (SSR) detected |
| `accessibility-patterns` | Frontend detected               |

### Backend Skills

| Skill                   | Enable When                |
| ----------------------- | -------------------------- |
| `api-patterns`          | Backend framework detected |
| `auth-patterns`         | Auth dependencies detected |
| `graphql-patterns`      | GraphQL detected           |
| `nodejs-best-practices` | Node.js detected           |

### Database Skills

| Skill               | Enable When           |
| ------------------- | --------------------- |
| `database-design`   | Any database detected |
| `postgres-patterns` | PostgreSQL detected   |
| `redis-patterns`    | Redis detected        |

### Mobile Skills

| Skill                   | Enable When           |
| ----------------------- | --------------------- |
| `flutter-patterns`      | Flutter/Dart detected |
| `react-native-patterns` | React Native detected |
| `mobile-design`         | Any mobile platform   |

### DevOps Skills

| Skill                      | Enable When                |
| -------------------------- | -------------------------- |
| `docker-patterns`          | Docker detected            |
| `kubernetes-patterns`      | Kubernetes detected        |
| `terraform-patterns`       | Terraform detected         |
| `github-actions`           | GitHub Actions detected    |
| `gitlab-ci-patterns`       | GitLab CI detected         |
| `monitoring-observability` | DevOps/Production detected |

### AI Skills

| Skill                | Enable When                  |
| -------------------- | ---------------------------- |
| `ai-rag-patterns`    | AI/LLM dependencies detected |
| `prompt-engineering` | AI/LLM dependencies detected |

### Realtime & Queue Skills

| Skill               | Enable When                    |
| ------------------- | ------------------------------ |
| `realtime-patterns` | Socket.IO/WebSocket detected   |
| `queue-patterns`    | BullMQ/RabbitMQ detected       |
| `multi-tenancy`     | Multi-tenant patterns detected |

### Support Skills

| Skill                     | Enable When                |
| ------------------------- | -------------------------- |
| `i18n-localization`       | i18n dependencies detected |
| `documentation-templates` | Always available           |
| `mermaid-diagrams`        | Always available           |

---

## 📊 Recommendation Output

```json
{
  "skills": {
    "enabled": [
      "clean-code",
      "testing-patterns",
      "security-fundamentals",
      "react-patterns",
      "typescript-patterns",
      "tailwind-patterns",
      "frontend-design",
      "api-patterns",
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
      "realtime-patterns",
      "ai-rag-patterns",
      "kubernetes-patterns"
    ],
    "coreSkills": [
      "clean-code",
      "brainstorming",
      "plan-writing",
      "systematic-debugging",
      "testing-patterns",
      "security-fundamentals"
    ]
  }
}
```

---

## 🔧 Mapping Rules

### Category → Skill Mapping

| Detected Category | Skills to ENABLE                                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| `frontend`        | react-patterns, typescript-patterns, frontend-design, tailwind-patterns, seo-patterns, accessibility-patterns |
| `backend`         | api-patterns, nodejs-best-practices, auth-patterns                                                            |
| `mobile`          | flutter-patterns OR react-native-patterns, mobile-design                                                      |
| `database`        | database-design, postgres-patterns OR redis-patterns                                                          |
| `devops`          | docker-patterns, kubernetes-patterns, github-actions, monitoring-observability                                |
| `ai`              | ai-rag-patterns, prompt-engineering                                                                           |
| `realtime`        | realtime-patterns                                                                                             |
| `queue`           | queue-patterns                                                                                                |
| `graphql`         | graphql-patterns                                                                                              |

### Framework → Additional Skills

| Framework     | Additional Skills                  |
| ------------- | ---------------------------------- |
| `nextjs`      | seo-patterns, react-patterns       |
| `tailwindcss` | tailwind-patterns                  |
| `prisma`      | database-design, postgres-patterns |
| `socketio`    | realtime-patterns                  |
| `gitlab-ci`   | gitlab-ci-patterns                 |
| `terraform`   | terraform-patterns                 |

---

## ⚠️ Important Notes

1. **Core skills always ON** - Never disable core skills
2. **Conservative approach** - When in doubt, keep skill enabled
3. **User override** - User can force enable/disable any skill
4. **Future planning** - Check user's future techstack plans before disabling

---

## 📄 Persistence

Results are saved to `.agent/profile.json`:

```json
{
  "version": "1.0",
  "generatedAt": "2026-02-05T12:00:00Z",
  "analyzedBy": "filter-skill v1.0",
  "skills": {
    "enabled": [...],
    "disabled": [...],
    "userOverrides": {
      "force-enabled": [],
      "force-disabled": []
    }
  }
}
```

---
