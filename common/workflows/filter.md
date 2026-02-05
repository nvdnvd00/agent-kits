---
description: Analyze workspace and enable/disable skills/agents based on techstack
---

# /filter - Workspace Skill Filtering

## Trigger

User calls `/filter` or requests "filter skills", "optimize skills for this project"

## Agent

No specific agent required - this skill is standalone.

## Prerequisites

- Currently in a workspace with code

## Critical Rules

1. **ALWAYS ASK** - Always ask user confirmation before applying changes
2. **NEVER DISABLE CORE** - Never disable core skills (clean-code, testing-patterns, etc.)
3. **PERSIST RESULTS** - Save results to `.agent/workspace-profile.json`
4. **ASK FUTURE STACK** - Ask user about planned future techstack additions

---

## Workflow Steps

### Step 1: Analyze Workspace

```
1. Read filter-skill SKILL.md to understand detection criteria
2. Scan workspace for config files:
   - package.json, pubspec.yaml, pyproject.toml, Cargo.toml, go.mod
   - next.config.*, vite.config.*, angular.json, nuxt.config.*
   - Dockerfile, docker-compose.*, k8s/, kubernetes/
   - .github/workflows/, .gitlab-ci.yml
   - prisma/, drizzle.config.*, terraform/
3. Parse dependencies if package manager exists
4. Build techstack profile
```

### Step 2: Generate Recommendations

```
1. Load skill definitions from ARCHITECTURE.md
2. Map detected techstack → required skills
3. Identify skills to ENABLE (missing but needed)
4. Identify skills to DISABLE (present but not needed)
5. Build recommendation table
```

### Step 3: Present to User

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

### Recommended Changes

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

### Confirmation Questions:

1. **Do you agree with the changes above?** (yes/no/customize)

2. **Are there any techstacks you plan to add in the future?**
   (e.g., mobile app, Kubernetes, different CI/CD...)

3. **Are there any skills you want to force enable or disable?**
   (e.g., keep ai-rag-patterns even though not currently used)
```

### Step 4: Process User Response

```
Based on user answer:

If YES:
  → Apply all recommended changes
  → Save to workspace-profile.json

If NO / CUSTOMIZE:
  → Ask which changes to skip/modify
  → Apply only approved changes
  → Save to workspace-profile.json

If user mentions FUTURE techstack:
  → Add to futureTechstack array
  → Keep relevant skills enabled (don't disable)
```

### Step 5: Save Profile

Create/Update `.agent/workspace-profile.json`:

```json
{
  "version": "1.0",
  "generatedAt": "ISO timestamp",
  "analyzedBy": "filter-skill v1.0",
  "techstack": { ... },
  "skills": {
    "enabled": [...],
    "disabled": [...],
    "userOverrides": { ... }
  },
  "agents": {
    "disabled": [...]
  },
  "futureTechstack": [...]
}
```

### Step 6: Confirm

```markdown
## ✅ Workspace Profile Saved!

**File:** `.agent/workspace-profile.json`

**Summary:**

- Skills enabled: 15
- Skills disabled: 8
- Agents disabled: 2
- Future techstack tracked: 2

**Next steps:**

- Profile will be automatically loaded in subsequent sessions
- Run `/filter --reset` to re-enable all skills
- Run `/filter` again when project adds new techstack
```

---

## Output Format

Final result is the `workspace-profile.json` file saved to disk.

---

## Exit Conditions

- User confirms and profile is saved successfully
- User cancels mid-process (no save)
- Error during analysis (report error, no save)

---

## Examples

### Example 1: Next.js + Tailwind Project

```
User: /filter

AI: [Analyze workspace...]

Detected: Next.js 14, TypeScript, Tailwind CSS, Prisma, PostgreSQL

Recommend ENABLE: react-patterns, tailwind-patterns, postgres-patterns
Recommend DISABLE: flutter-patterns, mobile-design, queue-patterns

User: yes, future I might add mobile app

AI: [Save profile with futureTechstack: ["react-native"]]
    [Keep mobile-design enabled for future use]
```

### Example 2: Python ML Project

```
User: /filter

AI: [Analyze workspace...]

Detected: Python 3.11, Poetry, FastAPI, PostgreSQL, OpenAI

Recommend ENABLE: api-patterns, postgres-patterns, ai-rag-patterns
Recommend DISABLE: react-patterns, flutter-patterns, tailwind-patterns, mobile-design

User: customize, keep testing-patterns and docker-patterns

AI: [Apply with user customization]
```

---
