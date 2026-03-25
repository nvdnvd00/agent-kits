---
name: gitlab-ci-patterns
summary: true
description: "GitLab CI/CD pipeline patterns. For planning/quick ref — load SKILL.md for full YAML configs."
---

# GitLab CI Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when writing `.gitlab-ci.yml` configurations.

## Stage Order
```
lint → test → build → security → deploy
```

## Key Rules
- **Images**: Always pin versions (`node:20-alpine`, NOT `:latest`)
- **Rules**: Use `rules:` keyword, avoid deprecated `only/except`
- **Cache**: `pull-push` for update jobs · `pull` for read-only jobs · key: `$CI_COMMIT_REF_SLUG`
- **Artifacts**: `expire_in` always set · `paths:` for build output · `reports:` for coverage
- **Secrets**: GitLab CI/CD Variables (masked+protected), NEVER in `.gitlab-ci.yml`
- **Docker**: `services: [docker:dind]` + `DOCKER_TLS_CERTDIR: "/certs"` + login before push
- **DAG**: Use `needs:` for parallel jobs within stages (faster than sequential stages)

## Optimization
- `interruptible: true` on default + `interruptible: false` on prod deploys
- Parallel matrix: `parallel: matrix: - NODE_VERSION: ["18","20"]`

## Anti-Patterns
- `only/except` → use `rules:`
- No `expire_in` on artifacts
- Hardcoded URLs → use variables
- Single large job → split into stages

> Load full SKILL.md for: full YAML examples (Node.js pipeline, Docker build, multi-env deploy), caching strategy details, security scanning templates
