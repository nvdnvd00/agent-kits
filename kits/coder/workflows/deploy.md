---
description: Deployment command for production releases. Pre-flight checks and deployment execution.
---

# /deploy - Production Deployment Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "deploy", "release", "ship", "triển khai", or `/deploy`

## Agent

Route to `devops-engineer` agent

---

## Sub-commands

| Command              | Description                    |
| -------------------- | ------------------------------ |
| `/deploy`            | Interactive deployment wizard  |
| `/deploy check`      | Run pre-deployment checks only |
| `/deploy preview`    | Deploy to preview/staging      |
| `/deploy production` | Deploy to production           |
| `/deploy rollback`   | Rollback to previous version   |

---

## 🔴 Critical Rules

1. **Pre-flight Checks** - Never deploy without passing all checks
2. **No Hardcoded Secrets** - All secrets in environment variables
3. **Health Check After Deploy** - Verify application is running
4. **Rollback Plan Ready** - Always have a way back

---

## Workflow

### Phase 1: Pre-Deployment Checks

Run all checks before deployment:

```markdown
## 🚀 Pre-Deploy Checklist

### Code Quality

- [ ] No TypeScript errors (`pnpm tsc --noEmit`)
- [ ] ESLint passing (`pnpm lint`)
- [ ] All tests passing (`pnpm test`)

### Security

- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Dependencies audited (`pnpm audit`)

### Performance

- [ ] Bundle size acceptable
- [ ] No console.log statements
- [ ] Images optimized

### Documentation

- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs current
```

If any check fails, stop and fix before proceeding.

### Phase 2: Build Application

Build for production:

```bash
# Build the application
pnpm build

# Verify build output
ls -la dist/
```

Check for build errors or warnings.

### Phase 3: Deploy

Deploy to target platform:

```markdown
## Deployment Execution

### Platform: [Detected/Specified]

### Environment: [preview/production]

### Version: [Auto-generated or specified]
```

Platform-specific commands:

| Platform | Command                | Auto-detect        |
| -------- | ---------------------- | ------------------ |
| Vercel   | `vercel --prod`        | Next.js            |
| Railway  | `railway up`           | Node.js            |
| Fly.io   | `fly deploy`           | Dockerfile         |
| Docker   | `docker compose up -d` | docker-compose.yml |
| AWS      | `aws s3 sync`          | AWS CLI            |

### Phase 4: Health Check

Verify deployment success:

```markdown
## Health Check

### Endpoints

- [ ] Main URL responding (200 OK)
- [ ] API health endpoint (`/api/health`)
- [ ] Database connected

### Services

- [ ] All containers running
- [ ] No error logs in last 5 minutes
- [ ] Memory/CPU within limits
```

### Phase 5: Report

Present deployment summary:

```markdown
## 🚀 Deployment Complete

### Summary

| Item        | Value      |
| ----------- | ---------- |
| Version     | v1.2.3     |
| Environment | production |
| Duration    | 47 seconds |
| Platform    | Vercel     |

### URLs

- 🌐 **Production:** https://app.example.com
- 📊 **Dashboard:** https://vercel.com/project

### What Changed

- Added user profile feature
- Fixed login bug
- Updated dependencies

### Health Check

✅ API responding (200 OK)
✅ Database connected
✅ All services healthy

### Rollback

If issues occur, run: `/deploy rollback`
```

---

## Deployment Flow Diagram

```
┌─────────────────┐
│  /deploy        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pre-flight     │
│  checks         │
└────────┬────────┘
         │
    Pass? ──No──► Fix issues
         │
        Yes
         │
         ▼
┌─────────────────┐
│  Build          │
│  application    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deploy to      │
│  platform       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Health check   │
│  & verify       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ Complete    │
└─────────────────┘
```

---

## Rollback Procedure

If deployment fails or issues are detected:

````markdown
## 🔄 Rollback Procedure

### Step 1: Identify Issue

- What symptom?
- When did it start?
- Which version?

### Step 2: Execute Rollback

```bash
# Vercel
vercel rollback

# Railway
railway rollback

# Docker
docker compose down
docker compose -f docker-compose.previous.yml up -d
```
````

### Step 3: Verify Rollback

- [ ] Previous version running
- [ ] Health checks passing
- [ ] User-facing error resolved

### Step 4: Document

- Record what failed
- Create fix plan
- Schedule proper deployment

```

---

## Exit Conditions

- ✅ **Success:** Deployed, health check passing, URLs accessible
- ❌ **Failure:** Build failed, deployment error, health check failed
- ⚠️ **Warning:** Deployed but with warnings (deprecations, high memory)

---

## Usage Examples

```

/deploy
/deploy check
/deploy preview
/deploy production
/deploy rollback

```

```
