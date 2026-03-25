---
name: multi-tenancy
summary: true
description: "Multi-tenant architecture patterns. For planning/quick ref — load SKILL.md for full isolation and context code."
---

# Multi-Tenancy — Summary

> ⚡ Quick ref. Load full `SKILL.md` when implementing isolation strategy or context propagation.

## Isolation Strategy Selection
| Tenants | Compliance | Strategy |
|---|---|---|
| <100 | None | Shared DB + RLS |
| 100-1000 | Moderate | Schema-per-tenant |
| Enterprise | HIPAA/PCI/SOC2 | DB-per-tenant |

## Non-Negotiable Rules
- **EVERY query filters by `tenant_id`** — no exceptions
- **NEVER trust client-provided tenant ID** — extract from JWT/subdomain/gateway header
- **Cache keys prefixed**: always `tenant:{id}:key`
- **Background jobs**: always include `tenantId` in job data
- **Context flows**: HTTP → Service → Queue → Worker → DB (AsyncLocalStorage in Node.js)
- **RLS as defense-in-depth** — even when app filters by tenant_id
- **Log `tenant_id`** in every log entry

## Tenant Resolution Priority
JWT Claim > Subdomain > Custom Header > (never: query param or URL path)

## Fatal Anti-Patterns
- `SELECT * FROM users` without tenant filter → instant cross-tenant data leak
- Trusting `req.query.tenant` → trivial to spoof
- No Redis key prefix → cache poisoning across tenants
- Background job without tenantId → orphaned/wrong-context operations

> Load full SKILL.md for: RLS SQL patterns, AsyncLocalStorage code, isolation matrix, full implementation checklist
