---
name: multi-tenancy
description: Multi-tenant architecture principles and decision-making. Use when designing tenant isolation, data partitioning, context propagation, or building SaaS applications. Covers database strategies, resource isolation, and compliance patterns.
version: 1.0.0
tags: [architecture, saas, isolation, tenancy, compliance]
---

# Multi-Tenancy - SaaS Architecture Skill

> **Purpose:** Enable AI agents to design and implement robust multi-tenant systems with proper isolation, context propagation, and scalability.

---

## 📑 Navigation

- [Philosophy](#-philosophy)
- [Isolation Strategies](#-isolation-strategies)
- [Context Propagation](#-context-propagation)
- [Decision Frameworks](#-decision-frameworks)
- [Anti-Patterns](#-anti-patterns)
- [Checklist](#-implementation-checklist)

---

## 💡 Philosophy

> **"Multi-tenancy is trust architecture—design for distrust, verify always."**

| Principle                  | Implementation                               |
| -------------------------- | -------------------------------------------- |
| **Defense in Depth**       | Multiple isolation layers (app + DB + infra) |
| **Context Everywhere**     | Tenant ID flows through every layer          |
| **Fail Closed**            | Missing tenant context = deny access         |
| **Explicit Over Implicit** | Never infer tenant, always verify            |
| **Audit Everything**       | Log all cross-boundary access                |

---

## 🔄 ISOLATION STRATEGIES

### Database Isolation Spectrum

| Strategy              | Isolation | Cost   | Complexity | When to Use                                 |
| --------------------- | --------- | ------ | ---------- | ------------------------------------------- |
| **Shared DB + RLS**   | Medium    | Low    | Low        | Startups, <100 tenants, cost-sensitive      |
| **Schema-per-Tenant** | High      | Medium | Medium     | 100-1000 tenants, moderate compliance       |
| **DB-per-Tenant**     | Highest   | High   | High       | Enterprise, HIPAA/Financial, data residency |

### Row-Level Security (RLS) Pattern

```sql
-- 1. Enable RLS on tenant tables
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 2. Create isolation policy
CREATE POLICY tenant_isolation ON conversations
  FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- 3. Set context at connection start
SET app.tenant_id = 'tenant-uuid-here';
```

### Schema-per-Tenant Pattern

```
Database: app_db
├── tenant_acme/         # Schema for ACME Corp
│   ├── users
│   ├── conversations
│   └── ...
├── tenant_globex/       # Schema for Globex Inc
│   ├── users
│   ├── conversations
│   └── ...
└── public/              # Shared lookup tables
    ├── plans
    └── features
```

### DB-per-Tenant Pattern

```
Master Database (shared)
├── tenants              # Tenant registry
│   ├── id, name, slug
│   ├── db_connection_string
│   └── redis_db_index
└── plans

Tenant Databases (isolated)
├── acme_db              # Full isolation
├── globex_db            # Full isolation
└── ...
```

---

## 🔀 CONTEXT PROPAGATION

### Request Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│ 1. TENANT RESOLUTION (Middleware)                       │
├─────────────────────────────────────────────────────────┤
│ Extract from: subdomain | header | JWT claim | path     │
│ Validate:     tenant exists & active                    │
│ Cache:        Redis TTL 5-15 mins                       │
│ Attach:       to request-scoped context                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. REQUEST-SCOPED CONTEXT                               │
├─────────────────────────────────────────────────────────┤
│ context = {                                             │
│   tenantId: "acme",                                     │
│   tenantConfig: { features, limits, dbPool },           │
│   userId: "user123",                                    │
│   requestId: "req-uuid"                                 │
│ }                                                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. SERVICE LAYER (Tenant-Aware)                         │
├─────────────────────────────────────────────────────────┤
│ All queries automatically filtered by tenant_id         │
│ Repository base class includes tenant filter            │
└─────────────────────────────────────────────────────────┘
```

### Context Technologies by Platform

| Platform        | Mechanism                     | Pattern                   |
| --------------- | ----------------------------- | ------------------------- |
| **Node.js**     | `AsyncLocalStorage`           | Thread-safe async context |
| **Python**      | `contextvars`                 | Async context manager     |
| **Java/Spring** | `ThreadLocal` + Request scope | Bean scoping              |
| **.NET**        | `AsyncLocal<T>`               | Async flow context        |
| **Go**          | `context.Context`             | Explicit propagation      |

### Background Job Context

```typescript
// ❌ WRONG: Context lost in background job
queue.add("sendEmail", { userId, templateId });

// ✅ CORRECT: Tenant context preserved
queue.add("sendEmail", {
  tenantId, // ALWAYS include
  userId,
  templateId,
  correlationId, // For tracing
});

// Job processor
async function processJob(job) {
  const { tenantId, ...data } = job.data;
  await setTenantContext(tenantId); // Restore context
  // Process with tenant context...
}
```

---

## 🧭 DECISION FRAMEWORKS

### Isolation Level Decision Tree

```
START
  │
  ▼
┌──────────────────────────┐
│ Compliance Requirements? │
│ (HIPAA, PCIDSS, SOC2)    │
└──────────────────────────┘
  │
  ├── Yes → DB-per-Tenant + Dedicated Compute
  │
  ▼
┌──────────────────────────┐
│ Enterprise Customers?    │
│ (Paying for isolation)   │
└──────────────────────────┘
  │
  ├── Yes → Hybrid (Shared for SMB, Dedicated for Enterprise)
  │
  ▼
┌──────────────────────────┐
│ Expected Tenant Count?   │
└──────────────────────────┘
  │
  ├── <100  → Shared DB + RLS
  ├── 100-1000 → Schema-per-Tenant
  └── >1000 → Shared DB + RLS + Good Sharding
```

### Resource Isolation Matrix

| Resource       | Shared Strategy           | Isolated Strategy    |
| -------------- | ------------------------- | -------------------- |
| **Database**   | RLS + tenant_id column    | DB-per-tenant        |
| **Redis**      | Key prefix `{tenant}:`    | DB index per tenant  |
| **S3/Storage** | Prefix `tenants/{id}/`    | Bucket per tenant    |
| **Queue**      | tenant_id in job data     | Queue per tenant     |
| **WebSocket**  | Room prefix `tenant:{id}` | Namespace per tenant |

### Tenant Identification Priority

| Method            | Security | When to Use                      |
| ----------------- | -------- | -------------------------------- |
| **JWT Claim**     | High     | API calls with auth              |
| **Subdomain**     | High     | `acme.app.com`                   |
| **Custom Header** | Medium   | Internal services, microservices |
| **Path Segment**  | Low      | `/api/tenants/{id}/...` (avoid)  |
| **Query Param**   | Very Low | Never use for tenant ID          |

---

## ❌ ANTI-PATTERNS

### Critical Mistakes

| Anti-Pattern                      | Risk                               | Correct Approach                              |
| --------------------------------- | ---------------------------------- | --------------------------------------------- |
| **Trust client tenant ID**        | Data breach                        | Validate from auth token/subdomain            |
| **No RLS on shared tables**       | SQL injection → full DB exposure   | Enable RLS as defense in depth                |
| **Global cache without prefix**   | Cross-tenant data leakage          | Always prefix: `{tenant}:{key}`               |
| **Background job without tenant** | Orphaned operations, wrong context | Include tenant_id in EVERY job                |
| **Single connection pool**        | Noisy neighbor, unclear isolation  | Pool per tenant or connection tagging         |
| **Tenant ID in URL path**         | Tampering risk                     | Subdomain or header (cleaner, safer)          |
| **No audit logging**              | Cannot detect breaches             | Log all cross-boundary access                 |
| **Skipping context in async**     | Context lost in callbacks          | Use AsyncLocalStorage or explicit propagation |

### Code Smells

```typescript
// ❌ SMELL: Direct query without tenant filter
const users = await db.query("SELECT * FROM users");

// ✅ CORRECT: Always include tenant filter
const users = await db.query("SELECT * FROM users WHERE tenant_id = $1", [
  tenantId,
]);

// ❌ SMELL: Trusting user input for tenant
const tenantId = req.query.tenant; // NEVER

// ✅ CORRECT: Extract from verified source
const tenantId = req.headers["x-tenant-id"]; // From gateway
// OR
const tenantId = extractFromJWT(req.auth.token);
// OR
const tenantId = extractFromSubdomain(req.hostname);
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Tenant Resolution

- [ ] Tenant extracted from trusted source (subdomain/header/JWT)
- [ ] Tenant existence validated against master DB
- [ ] Tenant config cached with appropriate TTL (5-15 mins)
- [ ] Invalid/missing tenant returns 404/401 (not 500)
- [ ] Tenant context attached to request early in middleware

### Data Isolation

- [ ] RLS enabled on ALL tenant tables (defense in depth)
- [ ] All repositories include tenant filter by default
- [ ] Database connection tagged with tenant context
- [ ] Cross-tenant queries explicitly blocked at service layer
- [ ] tenant_id column is NOT NULL + indexed

### Context Propagation

- [ ] Request-scoped context mechanism in place
- [ ] Context flows through async boundaries
- [ ] Background jobs include tenant_id + correlation_id
- [ ] WebSocket connections have tenant context
- [ ] Logs include tenant_id for every entry

### Resource Isolation

- [ ] Cache keys prefixed: `{tenant}:{key}`
- [ ] Storage paths include tenant: `tenants/{id}/...`
- [ ] Rate limiting applied per tenant
- [ ] Queue jobs tagged with tenant context
- [ ] Metrics labeled by tenant for monitoring

### Compliance & Security

- [ ] Audit logs for all data access
- [ ] No cross-tenant data exposure in errors
- [ ] Data residency requirements met
- [ ] Tenant offboarding procedure documented
- [ ] Regular penetration testing includes tenant isolation

---

## 📚 References

- [Azure Multi-Tenant Architecture Patterns](https://docs.microsoft.com/en-us/azure/architecture/guide/multitenant/overview)
- [PostgreSQL Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [SaaS Tenant Isolation Strategies](https://aws.amazon.com/blogs/apn/multi-tenant-saas-database-tenancy-patterns/)
- [AsyncLocalStorage (Node.js)](https://nodejs.org/api/async_context.html)

---

> **Remember:** In multi-tenant systems, ONE missed tenant filter = ALL customer data exposed. Verify tenant context at every boundary, filter everywhere, and audit continuously.
