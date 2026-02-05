---
name: filter-agent
description: Recommend enabling/disabling agents based on detected techstack. Reduces noise from irrelevant agents in the workspace.
category: common
trigger: manual
---

# Filter Agent Skill

> Workspace-aware agent filtering for optimal AI performance.

---

## 🎯 Purpose

Filter Agent analyzes the **techstack profile** (from scan-techstack) and recommends which agents to **disable** based on project needs. This:

1. **Reduces cognitive load** - AI focuses on relevant agents only
2. **Improves accuracy** - No confusion from unrelated agent personas
3. **Optimizes routing** - Orchestrator routes to appropriate specialists

---

## 🤖 Agent Categories

### Tier 1: Master Agents (NEVER DISABLE)

| Agent             | Always Required For              |
| ----------------- | -------------------------------- |
| `orchestrator`    | Multi-agent coordination         |
| `project-planner` | Project planning, task breakdown |
| `debugger`        | Systematic problem solving       |

### Tier 2: Development Specialists

| Agent                 | Enable When                                |
| --------------------- | ------------------------------------------ |
| `frontend-specialist` | Frontend detected (React, Vue, Angular)    |
| `backend-specialist`  | Backend detected (Express, NestJS, API)    |
| `mobile-developer`    | Mobile detected (Flutter, RN, iOS/Android) |
| `database-specialist` | Database detected (Prisma, PostgreSQL)     |
| `devops-engineer`     | DevOps detected (Docker, K8s, CI/CD)       |

### Tier 3: Quality & Security

| Agent                 | Enable When                                 |
| --------------------- | ------------------------------------------- |
| `security-auditor`    | Always enabled for security reviews         |
| `code-reviewer`       | Always enabled for PR reviews               |
| `test-engineer`       | Testing detected (Jest, Vitest, Playwright) |
| `performance-analyst` | Always enabled for optimization             |

### Tier 4: Domain Specialists

| Agent                    | Enable When                                |
| ------------------------ | ------------------------------------------ |
| `realtime-specialist`    | Realtime detected (Socket.IO, WS)          |
| `multi-tenant-architect` | Multi-tenancy patterns detected            |
| `queue-specialist`       | Queue detected (BullMQ, RabbitMQ)          |
| `integration-specialist` | External API integrations detected         |
| `ai-engineer`            | AI detected (OpenAI, LangChain)            |
| `cloud-architect`        | Cloud infra detected (AWS, GCP, Terraform) |
| `data-engineer`          | Data pipeline patterns detected            |

### Tier 5: Support Agents

| Agent                  | Enable When                |
| ---------------------- | -------------------------- |
| `documentation-writer` | Always enabled for docs    |
| `i18n-specialist`      | i18n dependencies detected |
| `ux-researcher`        | Frontend/Mobile detected   |

---

## 📋 Mapping Rules

### Category → Agent Mapping

| Detected Category | Agents to ENABLE                                 |
| ----------------- | ------------------------------------------------ |
| `frontend`        | frontend-specialist, ux-researcher               |
| `backend`         | backend-specialist                               |
| `mobile`          | mobile-developer, ux-researcher                  |
| `database`        | database-specialist                              |
| `devops`          | devops-engineer, cloud-architect                 |
| `ai`              | ai-engineer                                      |
| `realtime`        | realtime-specialist                              |
| `queue`           | queue-specialist                                 |
| `graphql`         | backend-specialist (GraphQL expertise)           |
| `auth`            | security-auditor (always on), backend-specialist |
| `testing`         | test-engineer                                    |

### Never Disable (Core Agents)

These agents are ALWAYS enabled regardless of techstack:

- `orchestrator` - Master coordinator
- `project-planner` - Planning and task management
- `debugger` - Problem solving
- `security-auditor` - Security reviews
- `code-reviewer` - Code quality
- `documentation-writer` - Documentation

---

## 📊 Recommendation Output

```json
{
  "agents": {
    "enabled": [
      "orchestrator",
      "project-planner",
      "debugger",
      "frontend-specialist",
      "backend-specialist",
      "database-specialist",
      "devops-engineer",
      "test-engineer",
      "security-auditor",
      "code-reviewer",
      "documentation-writer"
    ],
    "disabled": [
      "mobile-developer",
      "realtime-specialist",
      "queue-specialist",
      "ai-engineer",
      "multi-tenant-architect",
      "i18n-specialist",
      "data-engineer"
    ],
    "coreAgents": [
      "orchestrator",
      "project-planner",
      "debugger",
      "security-auditor",
      "code-reviewer",
      "documentation-writer"
    ]
  }
}
```

---

## 🔗 Integration

### Input: TechstackProfile

Receives output from `scan-techstack`:

```json
{
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

### Output: AgentProfile

Produces agent recommendations for `profile.json`:

```json
{
  "agents": {
    "disabled": [
      "mobile-developer",
      "realtime-specialist",
      "queue-specialist",
      "ai-engineer"
    ]
  }
}
```

---

## ⚠️ Important Notes

1. **Conservative approach** - When in doubt, keep agent enabled
2. **User override** - User can force enable/disable any agent
3. **Future planning** - If user plans to add mobile, keep mobile-developer enabled
4. **Orchestrator respects profile** - Will skip disabled agents when routing

---
