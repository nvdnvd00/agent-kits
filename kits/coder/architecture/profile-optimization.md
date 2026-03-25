# AGT-Kit: Profile-Based Slim Rules

> **Phase 3.1** — Profile-aware optimization. When `.agent/profile.json` exists, use this to determine
> which agents and skills are active, reducing unnecessary loading.

---

## How It Works

1. AI checks for `.agent/profile.json` at session start
2. Reads `agents.disabled[]` and `skills.disabled[]`  
3. Skips loading agent files and skills that are disabled
4. Loads slim summaries for enabled-but-inactive skills

---

## Profile Schema

```json
{
  "version": "1.0",
  "agents": {
    "disabled": ["mobile-developer", "flutter-patterns", "i18n-specialist"]
  },
  "skills": {
    "enabled": ["react-patterns", "typescript-patterns", "api-patterns"],
    "disabled": ["flutter-patterns", "react-native-patterns", "mobile-design", "i18n-localization"]
  },
  "preferences": {
    "skillLoadMode": "summary-first",
    "agentReadMode": "conditional",
    "maxTokenBudget": "medium"
  }
}
```

---

## skillLoadMode Options

| Mode | Behavior | Token Cost |
|---|---|---|
| `summary-first` | Load SKILL.summary.md, upgrade to full only when implementing | Low |
| `full` | Always load SKILL.md (legacy behavior) | High |
| `on-demand` | Never preload, only load when explicitly needed | Lowest |

## agentReadMode Options

| Mode | Behavior |
|---|---|
| `conditional` | Read agent file only on first activation or switch (recommended) |
| `always` | Read every time (legacy) |
| `skip` | Trust context memory, never re-read |

---

## Recommended Profile: Web/Fullstack

```json
{
  "version": "1.0",
  "agents": {
    "disabled": ["mobile-developer", "flutter-patterns", "react-native-patterns"]
  },
  "skills": {
    "enabled": ["react-patterns", "typescript-patterns", "api-patterns", "database-design", "tailwind-patterns"],
    "disabled": ["flutter-patterns", "react-native-patterns", "mobile-design", "aws-patterns", "kubernetes-patterns"]
  },
  "preferences": {
    "skillLoadMode": "summary-first",
    "agentReadMode": "conditional"
  }
}
```

## Recommended Profile: Backend/API

```json
{
  "version": "1.0",
  "agents": {
    "disabled": ["mobile-developer", "frontend-specialist", "ux-researcher"]
  },
  "skills": {
    "enabled": ["api-patterns", "database-design", "auth-patterns", "nodejs-best-practices", "queue-patterns"],
    "disabled": ["react-patterns", "tailwind-patterns", "mobile-design", "flutter-patterns", "react-native-patterns", "seo-patterns"]
  },
  "preferences": {
    "skillLoadMode": "summary-first",
    "agentReadMode": "conditional"
  }
}
```

## Recommended Profile: DevOps/Cloud

```json
{
  "version": "1.0",
  "agents": {
    "disabled": ["frontend-specialist", "mobile-developer", "ux-researcher", "i18n-specialist"]
  },
  "skills": {
    "enabled": ["docker-patterns", "kubernetes-patterns", "terraform-patterns", "aws-patterns", "github-actions", "monitoring-observability"],
    "disabled": ["react-patterns", "tailwind-patterns", "mobile-design", "flutter-patterns", "i18n-localization", "seo-patterns"]
  },
  "preferences": {
    "skillLoadMode": "summary-first",
    "agentReadMode": "conditional"
  }
}
```

---

> To apply a profile: copy one of the templates above to `.agent/profile.json` and customize.
> The AI will respect `skills.disabled` and skip loading those files entirely.
