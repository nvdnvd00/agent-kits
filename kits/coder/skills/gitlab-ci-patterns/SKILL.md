---
name: gitlab-ci-patterns
description: GitLab CI/CD principles and pipeline patterns. Use when setting up GitLab CI, designing multi-stage pipelines, configuring GitLab Runners, or implementing GitOps with GitLab. Covers caching, artifacts, security scanning, and deployment strategies.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# GitLab CI - CI/CD Automation

> **Philosophy:** Pipelines should be **fast, reliable, and reproducible**. Every merge request should trigger automated validation. Every deployment should be traceable and reversible.

---

## Core Principles

| Principle         | Rule                                                 |
| ----------------- | ---------------------------------------------------- |
| **DRY**           | Use templates, includes, and extends to avoid repeat |
| **Fast Feedback** | Tests should run in minutes, not hours               |
| **Stage Order**   | Build → Test → Security → Deploy                     |
| **Fail Fast**     | Stop pipeline on first failure, save resources       |
| **Cache Smart**   | Cache dependencies, not build outputs                |

---

## Pipeline Triggers

| Trigger           | Use Case             | Syntax                      |
| ----------------- | -------------------- | --------------------------- |
| **push**          | Every push to branch | `only: [branches]`          |
| **merge_request** | MR validation        | `only: [merge_requests]`    |
| **schedule**      | Cron jobs            | Project → CI/CD → Schedules |
| **tag**           | Release builds       | `only: [tags]`              |
| **manual**        | Human approval       | `when: manual`              |
| **api/trigger**   | External trigger     | Pipeline trigger tokens     |

### Common Rules Patterns

```yaml
.default-rules:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
```

---

## Essential Pipeline Patterns

### 1. Standard Node.js Pipeline

```yaml
stages:
  - build
  - test
  - deploy

variables:
  NODE_VERSION: "20"
  PNPM_VERSION: "9"

default:
  image: node:${NODE_VERSION}
  before_script:
    - corepack enable
    - corepack prepare pnpm@${PNPM_VERSION} --activate
    - pnpm install --frozen-lockfile

build:
  stage: build
  script:
    - pnpm build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .pnpm-store/
    policy: pull-push

test:
  stage: test
  script:
    - pnpm lint
    - pnpm test --coverage
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull

deploy:
  stage: deploy
  script:
    - echo "Deploying $CI_COMMIT_SHA"
  only:
    - main
  environment:
    name: production
    url: https://app.example.com
```

### 2. Docker Build & Push

```yaml
build-docker:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_HOST: tcp://docker:2376
    DOCKER_TLS_CERTDIR: "/certs"
    DOCKER_DRIVER: overlay2
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build
      --cache-from $CI_REGISTRY_IMAGE:latest
      --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      --tag $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - tags
```

### 3. Multi-Environment Deployment

```yaml
.deploy_template: &deploy_template
  image: bitnami/kubectl:latest
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default

deploy:staging:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f k8s/ -n staging
    - kubectl rollout status deployment/app -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f k8s/ -n production
    - kubectl rollout status deployment/app -n production
  environment:
    name: production
    url: https://app.example.com
  when: manual
  only:
    - main
```

---

## Caching Strategies

| Strategy            | Cache Key                                          | Use Case                   |
| ------------------- | -------------------------------------------------- | -------------------------- |
| **Per-branch**      | `${CI_COMMIT_REF_SLUG}`                            | Feature branch isolation   |
| **Per-job**         | `${CI_JOB_NAME}`                                   | Job-specific cache         |
| **Global**          | `global-cache`                                     | Shared across all branches |
| **Lock-file based** | `$CI_COMMIT_REF_SLUG-$CI_JOB_NAME-$CI_PIPELINE_ID` | Exact deps match           |

### Cache Best Practices

```yaml
# Pull-push: Job that updates cache
build:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .pnpm-store/
    policy: pull-push # Updates cache after job

# Pull-only: Jobs that only read cache
test:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull # Never updates cache

# Fallback keys for cache miss
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
  fallback_keys:
    - main # Fall back to main branch cache
```

---

## Artifacts vs Cache

| Aspect         | Cache                    | Artifacts                      |
| -------------- | ------------------------ | ------------------------------ |
| **Purpose**    | Speed up pipelines       | Pass data between jobs/stages  |
| **Visibility** | Not in UI                | Downloadable from UI           |
| **Lifetime**   | LRU eviction             | Configurable `expire_in`       |
| **Use case**   | `node_modules`, `.cache` | `dist/`, reports, test results |

---

## Security Scanning (Built-in Templates)

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

# Custom Trivy scan (more control)
trivy-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image
      --exit-code 1
      --severity HIGH,CRITICAL
      $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  allow_failure: true
```

---

## Variables & Secrets

### Variable Scopes

| Type           | Scope              | How to Set                    |
| -------------- | ------------------ | ----------------------------- |
| **Predefined** | Automatic          | `CI_COMMIT_SHA`, `CI_JOB_ID`  |
| **Project**    | All pipelines      | Settings → CI/CD → Variables  |
| **Group**      | All group projects | Group Settings → CI/CD        |
| **Protected**  | Protected branches | Variable → Protected checkbox |
| **Masked**     | Hidden in logs     | Variable → Masked checkbox    |
| **File**       | Write to temp file | Variable → Type: File         |

### Secure Secrets Pattern

```yaml
deploy:
  script:
    - echo "Deploying..."
  variables:
    # Reference variables, never hardcode
    API_KEY: $PRODUCTION_API_KEY # From CI/CD settings
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      variables:
        DEPLOY_ENV: production
    - if: $CI_COMMIT_BRANCH == "develop"
      variables:
        DEPLOY_ENV: staging
```

---

## Pipeline Optimization

### Parallel Jobs (Matrix)

```yaml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        OS: ["debian", "alpine"]
  image: node:${NODE_VERSION}-${OS}
  script:
    - npm test
```

### DAG (Directed Acyclic Graph)

```yaml
# Define explicit dependencies (faster than stage-based)
build:frontend:
  stage: build
  script: npm run build:frontend

build:backend:
  stage: build
  script: npm run build:backend

test:frontend:
  stage: test
  needs: [build:frontend] # Only waits for frontend build
  script: npm run test:frontend

test:backend:
  stage: test
  needs: [build:backend] # Only waits for backend build
  script: npm run test:backend

deploy:
  stage: deploy
  needs: [test:frontend, test:backend]
  script: echo "Deploy"
```

### Interruptible Pipelines

```yaml
# Cancel running pipelines when new commit pushed
default:
  interruptible: true

# Never interrupt critical jobs
prod-deploy:
  interruptible: false
```

---

## GitLab Runner Configuration

### Runner Selection

```yaml
# Use specific runner by tag
build:
  tags:
    - docker
    - linux

# High-performance jobs
heavy-test:
  tags:
    - gpu
    - high-memory
```

### Resource Limits (Kubernetes Runner)

```yaml
variables:
  KUBERNETES_CPU_REQUEST: "500m"
  KUBERNETES_CPU_LIMIT: "2"
  KUBERNETES_MEMORY_REQUEST: "1Gi"
  KUBERNETES_MEMORY_LIMIT: "4Gi"
```

---

## Decision Trees

### Which Cache Policy?

```
Does this job UPDATE dependencies?
├── Yes → policy: pull-push
└── No → policy: pull
    └── Is cache critical for job?
        ├── Yes → Add fallback_keys
        └── No → policy: pull
```

### When to Use `needs` vs Stages?

```
Are jobs independent within a stage?
├── Yes → Use needs (DAG) for parallelism
└── No → Traditional stages are fine
    └── Complex dependencies?
        └── Yes → DAG with explicit needs
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern                    | ✅ Correct Approach                 |
| ---------------------------------- | ----------------------------------- |
| `image: node:latest`               | Pin version: `node:20-alpine`       |
| No caching                         | Cache `node_modules`, `.cache` dirs |
| Secrets in `.gitlab-ci.yml`        | Use CI/CD variables (masked)        |
| Single job does everything         | Split into stages                   |
| No `expire_in` for artifacts       | Set expiration to save storage      |
| `allow_failure: true` everywhere   | Only for non-critical jobs          |
| Hardcoded URLs/versions            | Use variables                       |
| `only` without `except` or `rules` | Prefer `rules:` for clarity         |

---

## Common Issues & Fixes

| Issue                      | Cause                             | Fix                                      |
| -------------------------- | --------------------------------- | ---------------------------------------- |
| **Cache miss every time**  | Wrong cache key                   | Use `${CI_COMMIT_REF_SLUG}`              |
| **Artifacts not found**    | Job not in `needs`/`dependencies` | Add explicit dependency                  |
| **Slow Docker builds**     | No layer caching                  | Use `--cache-from` previous image        |
| **Runner timeout**         | Job exceeds limit                 | Increase timeout or optimize job         |
| **Protected variable N/A** | Not on protected branch           | Unprotect variable or use correct branch |

---

## 🔴 Self-Check Before Completing

| Check                    | Question                                 |
| ------------------------ | ---------------------------------------- |
| ✅ **Images pinned?**    | Using specific versions, not `:latest`?  |
| ✅ **Cache configured?** | Dependencies cached with correct policy? |
| ✅ **Secrets secure?**   | Using CI/CD variables, not hardcoded?    |
| ✅ **Artifacts expire?** | `expire_in` set to reasonable duration?  |
| ✅ **Security scans?**   | SAST/Dependency scanning enabled?        |
| ✅ **Rules clear?**      | Using `rules:` instead of `only/except`? |

---

## Related Skills

| Need              | Skill                   |
| ----------------- | ----------------------- |
| GitHub Actions    | `github-actions`        |
| Docker builds     | `docker-patterns`       |
| Kubernetes deploy | `kubernetes-patterns`   |
| Security scanning | `security-fundamentals` |
| Terraform in CI   | `terraform-patterns`    |

---

## GitLab vs GitHub Actions

| Feature         | GitLab CI                    | GitHub Actions               |
| --------------- | ---------------------------- | ---------------------------- |
| **Config file** | `.gitlab-ci.yml`             | `.github/workflows/*.yml`    |
| **Trigger**     | `rules:`, `only:`, `except:` | `on:` events                 |
| **Caching**     | Built-in `cache:` keyword    | `actions/cache@v4`           |
| **Artifacts**   | `artifacts:` keyword         | `actions/upload-artifact`    |
| **Secrets**     | CI/CD Variables              | Repository Secrets           |
| **Templates**   | `include:` templates         | Reusable workflows           |
| **Runners**     | Shared or self-hosted        | GitHub-hosted or self-hosted |
| **DAG**         | `needs:` keyword             | `needs:` in jobs             |

---

> **Remember:** A well-designed GitLab CI pipeline is invisible to developers - it just works. Push code, get feedback, ship with confidence. The best pipeline is the one you never have to debug.
