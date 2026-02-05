---
description: Analyze workspace and enable/disable skills/agents based on techstack
---

# /filter - Workspace Skill & Agent Filtering

## Trigger

User calls `/filter` or requests "filter skills", "optimize skills for this project"

## Agent

No specific agent required - this workflow uses common skills.

## Prerequisites

- Currently in a workspace with code

## Critical Rules

1. **ALWAYS ASK** - Always ask user confirmation before applying changes
2. **NEVER DISABLE CORE** - Never disable core skills/agents
3. **PERSIST RESULTS** - Save results to `.agent/profile.json`
4. **ASK FUTURE STACK** - Ask user about planned future techstack additions

---

## Workflow Overview

```
/filter
  ├── Step 1: scan-techstack → Detect technologies
  ├── Step 2: filter-skill → Recommend skill changes
  ├── Step 3: filter-agent → Recommend agent changes
  ├── Step 4: Present to User → Ask confirmation
  └── Step 5: Save Profile → Persist to profile.json
```

---

## Workflow Steps

### Step 1: Scan Techstack

```
1. Read scan-techstack SKILL.md to understand detection criteria
2. Scan workspace for config files:
   - package.json, pubspec.yaml, pyproject.toml, Cargo.toml, go.mod
   - next.config.*, vite.config.*, angular.json, nuxt.config.*
   - Dockerfile, docker-compose.*, k8s/, kubernetes/
   - .github/workflows/, .gitlab-ci.yml
   - prisma/, drizzle.config.*, terraform/
3. Parse dependencies if package manager exists
4. Build techstack profile with categories:
   - frontend, backend, mobile, database, devops, ai, realtime, queue
```

**Output:** TechstackProfile object

### Step 2: Filter Skills

```
1. Read filter-skill SKILL.md to understand mapping rules
2. Use TechstackProfile categories to determine required skills
3. Map detected frameworks → additional skills
4. Identify skills to ENABLE (needed for project)
5. Identify skills to DISABLE (not needed)
6. Ensure core skills are NEVER in disabled list
```

**Output:** SkillRecommendations object

### Step 3: Filter Agents

```
1. Read filter-agent SKILL.md to understand agent mapping
2. Use TechstackProfile categories to determine required agents
3. Identify agents to DISABLE (irrelevant to project)
4. Ensure core agents are NEVER in disabled list:
   - orchestrator, project-planner, debugger
   - security-auditor, code-reviewer, documentation-writer
```

**Output:** AgentRecommendations object

### Step 4: Present to User

Display in this format:

```markdown
## 🔍 Workspace Analysis Complete

### Detected Techstack

| Category  | Technology              |
| --------- | ----------------------- |
| Language  | TypeScript, Python      |
| Framework | Next.js 14 (App Router) |
| Styling   | Tailwind CSS v4         |
| Database  | PostgreSQL (Prisma)     |
| Cache     | Redis                   |
| CI/CD     | GitHub Actions          |

---

### 📚 Skill Recommendations

#### ✅ Skills to ENABLE:

| Skill             | Reason                   |
| ----------------- | ------------------------ |
| react-patterns    | Next.js detected         |
| tailwind-patterns | tailwind.config.js found |
| postgres-patterns | Prisma + PostgreSQL      |

#### ❌ Skills to DISABLE:

| Skill            | Reason                   |
| ---------------- | ------------------------ |
| flutter-patterns | No pubspec.yaml found    |
| mobile-design    | No mobile setup detected |

#### 🔒 Core Skills (always ON):

- clean-code, testing-patterns, security-fundamentals, brainstorming, plan-writing

---

### 🤖 Agent Recommendations

#### ✅ Agents to KEEP:

| Agent               | Reason             |
| ------------------- | ------------------ |
| frontend-specialist | Next.js detected   |
| backend-specialist  | API logic detected |
| devops-engineer     | Docker/CI detected |

#### ❌ Agents to DISABLE:

| Agent               | Reason                 |
| ------------------- | ---------------------- |
| mobile-developer    | No mobile detected     |
| realtime-specialist | No WebSocket detected  |
| queue-specialist    | No queue deps detected |

#### 🔒 Core Agents (always ON):

- orchestrator, project-planner, debugger, security-auditor, code-reviewer

---

### ❓ Confirmation Questions:

1. **Do you agree with the changes above?** (yes/no/customize)

2. **Are there any techstacks you plan to add in the future?**
   (e.g., mobile app, Kubernetes, different CI/CD...)

3. **Are there any skills/agents you want to force enable or disable?**
   (e.g., keep ai-rag-patterns even though not currently used)
```

### Step 5: Process User Response

```
Based on user answer:

If YES:
  → Apply all recommended changes
  → Save to profile.json

If NO / CUSTOMIZE:
  → Ask which changes to skip/modify
  → Apply only approved changes
  → Save to profile.json

If user mentions FUTURE techstack:
  → Add to futureTechstack array
  → Keep relevant skills/agents enabled (don't disable)
```

### Step 6: Save Profile

Create/Update `.agent/profile.json`:

```json
{
  "version": "1.0",
  "generatedAt": "ISO timestamp",
  "analyzedBy": "filter-workflow v1.0",
  "techstack": {
    "languages": ["typescript"],
    "frameworks": ["nextjs", "tailwindcss"],
    "databases": ["postgresql"],
    "tools": ["docker", "github-actions"]
  },
  "skills": {
    "enabled": ["react-patterns", "tailwind-patterns", "postgres-patterns", ...],
    "disabled": ["flutter-patterns", "mobile-design", ...],
    "userOverrides": {
      "force-enabled": [],
      "force-disabled": []
    }
  },
  "agents": {
    "disabled": ["mobile-developer", "realtime-specialist", "queue-specialist"]
  },
  "futureTechstack": ["react-native", "kubernetes"]
}
```

### Step 7: Confirm

```markdown
## ✅ Workspace Profile Saved!

**File:** `.agent/profile.json`

**Summary:**

- Skills enabled: 15
- Skills disabled: 8
- Agents disabled: 3
- Future techstack tracked: 2

**Next steps:**

- Profile will be automatically loaded in subsequent sessions
- Run `/filter --reset` to re-enable all skills/agents
- Run `/filter` again when project adds new techstack
```

---

## Output Format

Final result is the `profile.json` file saved to disk.

---

## Exit Conditions

- User confirms and profile is saved successfully
- User cancels mid-process (no save)
- Error during analysis (report error, no save)

---

## Command Variants

```bash
/filter              # Full analysis and recommendation
/filter --reset      # Reset to default (enable all)
/filter --force-enable <skill>   # Force enable specific skill
/filter --force-disable <skill>  # Force disable specific skill
/filter --dry-run    # Show recommendations without saving
```

---

## Examples

### Example 1: Next.js + Tailwind Project

```
User: /filter

AI: [Step 1: scan-techstack...]
    [Step 2: filter-skill...]
    [Step 3: filter-agent...]

Detected: Next.js 14, TypeScript, Tailwind CSS, Prisma, PostgreSQL

Skills to ENABLE: react-patterns, tailwind-patterns, postgres-patterns
Skills to DISABLE: flutter-patterns, mobile-design, queue-patterns

Agents to DISABLE: mobile-developer, realtime-specialist, queue-specialist

User: yes, but in the future I might add mobile app

AI: [Save profile with futureTechstack: ["react-native"]]
    [Keep mobile-developer enabled for future use]
```

### Example 2: Python ML Project

```
User: /filter

AI: [Analyze workspace...]

Detected: Python 3.11, Poetry, FastAPI, PostgreSQL, OpenAI

Skills to ENABLE: api-patterns, postgres-patterns, ai-rag-patterns
Skills to DISABLE: react-patterns, flutter-patterns, tailwind-patterns

Agents to ENABLE: ai-engineer, backend-specialist
Agents to DISABLE: frontend-specialist, mobile-developer

User: customize, I also need docker

AI: [Add docker-patterns to enabled]
    [Keep devops-engineer enabled]
    [Apply with user customization]
```

---
