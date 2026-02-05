---
name: docker-patterns
description: Docker containerization principles and decision-making. Use when writing Dockerfiles, optimizing image size, configuring Docker Compose, securing containers, or troubleshooting container issues. Covers multi-stage builds, security hardening, orchestration patterns.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: HIGH
---

# Docker Patterns - Container Excellence

> **Philosophy:** Containers should be **small, secure, and consistent** across all environments. Optimize for production from day one.

---

## Core Principles

| Principle        | Rule                                                  |
| ---------------- | ----------------------------------------------------- |
| **Immutable**    | Build once, run anywhere - no runtime modifications   |
| **Minimal**      | Only include what's needed - smaller = faster + safer |
| **Secure**       | Non-root by default, no secrets in layers             |
| **Reproducible** | Pin versions, multi-stage for consistent builds       |
| **Observable**   | Health checks, structured logs, metrics endpoints     |

---

## Image Base Selection

| Use Case                  | Recommended Base          | Size   |
| ------------------------- | ------------------------- | ------ |
| **Node.js production**    | `node:20-alpine`          | ~50MB  |
| **Minimal static binary** | `scratch` or `distroless` | <10MB  |
| **Python production**     | `python:3.12-slim`        | ~45MB  |
| **General purpose**       | `alpine:3.19`             | ~5MB   |
| **Debugging needed**      | `*-slim` variants         | ~100MB |

> 🔴 **Avoid:** Full `node:20`, `python:3.12`, `ubuntu:latest` in production.

---

## Multi-Stage Build Pattern

```dockerfile
# Stage 1: Dependencies (cached aggressively)
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build (includes dev dependencies)
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 3: Runtime (minimal)
FROM node:20-alpine AS runtime
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
WORKDIR /app
COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --from=build --chown=app:app /app/dist ./dist
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

---

## Layer Optimization Rules

| Rule                          | Why                                      |
| ----------------------------- | ---------------------------------------- |
| **COPY package.json first**   | Deps layer cached until deps change      |
| **Combine RUN commands**      | Fewer layers = smaller image             |
| **Clean in same RUN**         | `npm ci && npm cache clean` not separate |
| **Order by change frequency** | Least changing → Most changing           |
| **.dockerignore complete**    | Exclude node_modules, .git, logs         |

---

## Security Hardening Checklist

| Security Rule                | Implementation                      |
| ---------------------------- | ----------------------------------- |
| **Non-root user**            | `adduser` + `USER 1001`             |
| **Pin base image versions**  | `node:20.10.0-alpine`, not `latest` |
| **No secrets in Dockerfile** | Use build secrets or runtime env    |
| **Minimal packages**         | No vim, curl unless needed          |
| **Read-only filesystem**     | `--read-only` runtime flag          |
| **Scan for vulnerabilities** | `docker scout`, `trivy`             |

### Build Secrets Pattern (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    # Use API_KEY - it won't be in final layer
```

---

## Docker Compose Patterns

### Production-Ready Service

```yaml
services:
  app:
    build:
      context: .
      target: runtime
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s

networks:
  backend:
    driver: bridge

volumes:
  postgres_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## Decision Trees

### When to Use Multi-Stage?

```
Is build output smaller than source?
├── Yes → Use multi-stage (most apps)
└── No → Single stage might be OK
    └── Still need build tools at runtime?
        ├── Yes → Single stage
        └── No → Multi-stage anyway for security
```

### Which Base Image?

```
Need shell for debugging?
├── Yes → alpine or slim variants
└── No → Do you need libc?
    ├── Yes → distroless
    └── No → scratch (Go, Rust static binaries)
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern                | ✅ Correct Approach                       |
| ------------------------------ | ----------------------------------------- |
| `FROM node:latest`             | `FROM node:20.10.0-alpine`                |
| `RUN npm install` (not ci)     | `RUN npm ci --only=production`            |
| Running as root                | Create user, `USER 1001`                  |
| Secrets in ENV                 | Build secrets or external secrets manager |
| `COPY . .` before package.json | Copy package.json first for caching       |
| Separate RUN for cleanup       | Clean in same RUN command                 |
| No .dockerignore               | Comprehensive .dockerignore               |
| No health checks               | HEALTHCHECK instruction                   |
| 1GB+ images                    | Multi-stage + alpine base                 |

---

## Common Issues & Fixes

| Issue                      | Cause                    | Fix                                     |
| -------------------------- | ------------------------ | --------------------------------------- |
| **Slow builds**            | Cache invalidation       | COPY package.json before source         |
| **Large images**           | Build tools in prod      | Multi-stage, distroless                 |
| **Permission errors**      | Root ownership           | `--chown` in COPY, proper USER          |
| **Container won't start**  | CMD syntax error         | Use exec form `["node", "app.js"]`      |
| **Can't connect services** | Network misconfiguration | Custom networks, service names as hosts |
| **Data lost on restart**   | No volume                | Named volumes for persistence           |

---

## 🔴 Self-Check Before Completing

| Check                   | Question                                   |
| ----------------------- | ------------------------------------------ |
| ✅ **Multi-stage?**     | Is build separated from runtime?           |
| ✅ **Non-root?**        | Container runs as non-root user?           |
| ✅ **Pinned versions?** | Base image and deps have explicit version? |
| ✅ **Health check?**    | HEALTHCHECK or compose healthcheck?        |
| ✅ **Secrets safe?**    | No secrets in layers or ENV?               |
| ✅ **Image size?**      | Under 500MB for typical apps?              |
| ✅ **.dockerignore?**   | Excludes node_modules, .git, logs?         |

---

## Related Skills

| Need                  | Skill                     |
| --------------------- | ------------------------- |
| CI/CD pipelines       | `github-actions` (future) |
| Kubernetes deployment | `kubernetes-patterns`     |
| Server management     | `server-management`       |
| Deployment workflows  | `deployment-procedures`   |

---

> **Remember:** A well-built container is invisible infrastructure. If you're debugging container issues in production, something went wrong at build time.
