---
name: kubernetes-patterns
description: Kubernetes orchestration principles and decision-making. Use when deploying to K8s, designing cluster architecture, implementing GitOps, or configuring workloads. Covers manifests, Helm, deployments, services, and production patterns.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: HIGH
---

# Kubernetes Patterns - Cloud-Native Orchestration

> **Philosophy:** Kubernetes is infrastructure as code. Declare what you want, let the system reconcile. **GitOps everything.**

---

## Core Principles

| Principle           | Rule                                                 |
| ------------------- | ---------------------------------------------------- |
| **Declarative**     | Define desired state, not imperative steps           |
| **Immutable**       | Never modify running resources - redeploy instead    |
| **GitOps**          | Git is the source of truth for all manifests         |
| **Least Privilege** | RBAC with minimal permissions, pod security policies |
| **Observable**      | Probes, metrics, logs for every workload             |

---

## Workload Types

| Type            | Use Case                         | Example                    |
| --------------- | -------------------------------- | -------------------------- |
| **Deployment**  | Stateless apps, web servers      | API servers, frontend      |
| **StatefulSet** | Stateful apps needing stable IDs | Databases, message queues  |
| **DaemonSet**   | One pod per node                 | Log collectors, monitoring |
| **Job**         | Run-to-completion tasks          | DB migrations, batch jobs  |
| **CronJob**     | Scheduled tasks                  | Backups, reports           |

---

## Essential Manifest Patterns

### Production Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
        - name: api
          image: myapp/api:v1.0.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
```

### Service + Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
  ports:
    - port: 80
      targetPort: 3000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

---

## Resource Management

| Resource Type | Requests (min)      | Limits (max)              |
| ------------- | ------------------- | ------------------------- |
| **CPU**       | Guaranteed CPU time | CPU throttled if exceeded |
| **Memory**    | Reserved memory     | OOMKilled if exceeded     |

### Sizing Guidelines

| App Type       | CPU Request | Memory Request | CPU Limit   | Memory Limit |
| -------------- | ----------- | -------------- | ----------- | ------------ |
| **API Server** | 100m-200m   | 128Mi-256Mi    | 500m-1000m  | 512Mi-1Gi    |
| **Worker**     | 200m-500m   | 256Mi-512Mi    | 1000m-2000m | 1Gi-2Gi      |
| **Database**   | 500m-1000m  | 1Gi-2Gi        | 2000m-4000m | 4Gi-8Gi      |

> 🔴 **Always set requests!** Without requests, K8s can't schedule efficiently.

---

## Health Probes

| Probe Type         | Purpose             | On Failure                     |
| ------------------ | ------------------- | ------------------------------ |
| **livenessProbe**  | Is container alive? | Container restarted            |
| **readinessProbe** | Ready for traffic?  | Removed from Service endpoints |
| **startupProbe**   | Still starting up?  | Liveness/readiness disabled    |

### Probe Configuration

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10 # Wait before first check
  periodSeconds: 10 # Check every 10s
  timeoutSeconds: 5 # Timeout for check
  failureThreshold: 3 # Restart after 3 failures

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3
```

---

## Configuration Management

| Method               | Use Case                    | When to Use                 |
| -------------------- | --------------------------- | --------------------------- |
| **ConfigMap**        | Non-sensitive config        | App settings, feature flags |
| **Secret**           | Sensitive data              | API keys, passwords         |
| **External Secrets** | Production secrets          | Sync from Vault/AWS/GCP     |
| **Helm Values**      | Environment-specific config | Per-env deployments         |

### Secret Best Practices

```yaml
# Don't store secrets in manifests!
# Use External Secrets Operator:
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: db-credentials
  data:
    - secretKey: url
      remoteRef:
        key: prod/database
```

---

## Helm Patterns

### Chart Structure

```
mychart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default values
├── values-prod.yaml     # Production overrides
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── _helpers.tpl     # Template helpers
```

### Values Pattern

```yaml
# values.yaml (base)
replicaCount: 1
image:
  repository: myapp/api
  tag: latest
resources:
  requests:
    cpu: 100m
    memory: 128Mi

# values-prod.yaml (override)
replicaCount: 3
image:
  tag: v1.0.0
resources:
  requests:
    cpu: 500m
    memory: 512Mi
```

---

## Decision Trees

### Which Workload Type?

```
Need stable network identity/storage?
├── Yes → StatefulSet
└── No → Run on every node?
    ├── Yes → DaemonSet
    └── No → One-time task?
        ├── Yes → Job or CronJob
        └── No → Deployment
```

### Ingress vs LoadBalancer?

```
Multiple services behind one IP?
├── Yes → Ingress with Ingress Controller
└── No → Just one service exposed?
    ├── Yes → LoadBalancer Service
    └── No → Internal only?
        └── Yes → ClusterIP Service
```

---

## GitOps with ArgoCD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/manifests
    targetRevision: main
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern              | ✅ Correct Approach                     |
| ---------------------------- | --------------------------------------- |
| `kubectl apply` from laptop  | GitOps - apply from Git repo            |
| `latest` image tag           | Specific versioned tags                 |
| No resource requests/limits  | Always set requests, usually set limits |
| Running as root              | `runAsNonRoot: true`                    |
| Secrets in ConfigMap         | Use Secrets or External Secrets         |
| No health probes             | livenessProbe + readinessProbe          |
| Single replica in prod       | Minimum 2-3 replicas with PDB           |
| `kubectl edit` in production | Edit in Git, apply via GitOps           |

---

## 🔴 Self-Check Before Deploying

| Check                     | Question                              |
| ------------------------- | ------------------------------------- |
| ✅ **Resources set?**     | requests and limits configured?       |
| ✅ **Probes configured?** | liveness + readiness probes?          |
| ✅ **Non-root?**          | Pod runs as non-root user?            |
| ✅ **Image pinned?**      | Specific tag, not `latest`?           |
| ✅ **Secrets external?**  | No hardcoded secrets in manifests?    |
| ✅ **Replicas > 1?**      | At least 2 replicas for HA?           |
| ✅ **PDB defined?**       | PodDisruptionBudget for availability? |

---

## Related Skills

| Need                 | Skill                     |
| -------------------- | ------------------------- |
| Container images     | `docker-patterns`         |
| CI/CD pipelines      | `github-actions` (future) |
| Server management    | `server-management`       |
| Deployment workflows | `deployment-procedures`   |

---

> **Remember:** Kubernetes is not magic. It amplifies your practices - good and bad. If your deployments are messy, K8s will make them messier at scale. Start with GitOps, proper manifests, and observability.
