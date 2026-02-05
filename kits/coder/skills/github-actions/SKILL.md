---
name: github-actions
description: GitHub Actions CI/CD principles and workflow patterns. Use when setting up automated testing, building Docker images, deploying to production, or creating reusable workflows. Covers matrix builds, caching, secrets, and security scanning.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# GitHub Actions - CI/CD Automation

> **Philosophy:** CI/CD should be **fast, reliable, and secure**. Every push should trigger automated validation. Every deploy should be reproducible.

---

## Core Principles

| Principle         | Rule                                                  |
| ----------------- | ----------------------------------------------------- |
| **Automate**      | If it can be automated, automate it                   |
| **Fast feedback** | Tests should run in minutes, not hours                |
| **Reproducible**  | Same commit = same result, always                     |
| **Secure**        | Secrets in vault, least privilege, scan dependencies  |
| **Fail fast**     | Stop pipeline on first failure, don't waste resources |

---

## Workflow Triggers

| Trigger               | Use Case           | Syntax                  |
| --------------------- | ------------------ | ----------------------- |
| **push**              | Run on every push  | `on: push`              |
| **pull_request**      | PR validation      | `on: pull_request`      |
| **workflow_dispatch** | Manual trigger     | `on: workflow_dispatch` |
| **schedule**          | Cron jobs          | `on: schedule`          |
| **release**           | On release publish | `on: release`           |

### Common Trigger Patterns

```yaml
on:
  push:
    branches: [main, develop]
    paths-ignore:
      - "**.md"
      - "docs/**"
  pull_request:
    branches: [main]
```

---

## Essential Workflow Patterns

### 1. Test Workflow (Node.js)

```yaml
name: Test
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
```

### 2. Docker Build & Push

```yaml
name: Docker Build
on:
  push:
    branches: [main]
    tags: ["v*"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 3. Deploy with Approval

```yaml
name: Deploy
on:
  push:
    tags: ["v*"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com

    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying ${{ github.ref_name }}"
          # Your deploy commands here
```

---

## Caching Strategies

| Package Manager | Cache Action                   |
| --------------- | ------------------------------ |
| **pnpm**        | `cache: 'pnpm'` in setup-node  |
| **npm**         | `cache: 'npm'` in setup-node   |
| **pip**         | `cache: 'pip'` in setup-python |
| **Docker**      | `cache-from/to: type=gha`      |

### Custom Cache

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/puppeteer
      node_modules/.cache
    key: ${{ runner.os }}-cache-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-cache-
```

---

## Matrix Builds

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false # Don't cancel other jobs on failure
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18

    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

---

## Reusable Workflows

### Define Reusable Workflow

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci
      - run: npm test
```

### Call Reusable Workflow

```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "20"
    secrets: inherit
```

---

## Security Best Practices

| Practice                        | Implementation                 |
| ------------------------------- | ------------------------------ |
| **Pin action versions**         | `@v4` not `@latest` or `@main` |
| **Least privilege permissions** | Set `permissions:` explicitly  |
| **Use secrets**                 | `${{ secrets.MY_SECRET }}`     |
| **Scan dependencies**           | Trivy, Snyk, Dependabot        |
| **Review third-party actions**  | Check source before using      |

### Security Scanning Job

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: "fs"
        format: "sarif"
        output: "trivy.sarif"
    - uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: "trivy.sarif"
```

---

## Decision Trees

### Which Runner?

```
Need specific hardware (GPU, ARM)?
├── Yes → Self-hosted runner
└── No → Need macOS/Windows?
    ├── Yes → Larger hosted runners
    └── No → ubuntu-latest (cheapest/fastest)
```

### When to Use Matrix?

```
Need to test multiple versions/platforms?
├── Yes → Matrix with fail-fast: false
└── No → Single job
    └── Supporting many platforms?
        └── Yes → Matrix with exclude
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern                      | ✅ Correct Approach                  |
| ------------------------------------ | ------------------------------------ |
| `@latest` or `@main` for actions     | Pin specific version `@v4`           |
| No caching                           | Cache dependencies and builds        |
| Secrets in workflow files            | Use repository/environment secrets   |
| Single job does everything           | Split into focused jobs              |
| No `permissions:` block              | Explicit least-privilege permissions |
| Hardcoded versions                   | Use matrix or variables              |
| Skip tests on main branch            | Always test, especially on main      |
| `continue-on-error: true` everywhere | Only where truly necessary           |

---

## Common Issues & Fixes

| Issue                    | Cause                     | Fix                                  |
| ------------------------ | ------------------------- | ------------------------------------ |
| **Slow builds**          | No caching                | Add cache for deps and builds        |
| **Flaky tests**          | Race conditions, timeouts | Increase timeout, fix test isolation |
| **Permission denied**    | Missing permissions       | Add `permissions:` block             |
| **Cache miss**           | Wrong cache key           | Use `hashFiles()` for lock files     |
| **Secret not available** | Not in environment        | Check environment/repository secrets |

---

## 🔴 Self-Check Before Completing

| Check                   | Question                              |
| ----------------------- | ------------------------------------- |
| ✅ **Actions pinned?**  | Using `@v4` not `@latest`?            |
| ✅ **Caching enabled?** | Dependencies and builds cached?       |
| ✅ **Secrets secure?**  | Using `secrets.X`, not hardcoded?     |
| ✅ **Permissions set?** | Explicit `permissions:` block?        |
| ✅ **Tests run?**       | Critical paths tested in CI?          |
| ✅ **Paths filtered?**  | Skipping runs for irrelevant changes? |

---

## Related Skills

| Need                 | Skill                   |
| -------------------- | ----------------------- |
| Docker builds        | `docker-patterns`       |
| Kubernetes deploy    | `kubernetes-patterns`   |
| Security scanning    | `security-fundamentals` |
| Deployment workflows | `deployment-procedures` |

---

> **Remember:** A good CI/CD pipeline is invisible - it just works. Developers should trust it completely and never need to "re-run to see if it passes this time."
