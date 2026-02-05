---
name: database-design
description: Database design principles and decision-making. Use when designing schemas, choosing databases, selecting ORMs, or optimizing queries. Covers schema design, indexing strategy, ORM selection, migrations.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# Database Design - Principles & Decision Making

> **Philosophy:** Choose the right database and design for the context. Learn to THINK, not copy SQL patterns.

---

## Database Selection Decision Tree

```
What are your requirements?
│
├─ Simple app / Embedded / Edge?
│  └─ → SQLite / Turso / LibSQL
│
├─ Full relational / Complex queries?
│  └─ → PostgreSQL (self-hosted or managed)
│
├─ Serverless / Edge-first?
│  └─ → Neon / PlanetScale / Turso
│
├─ Document-oriented / Flexible schema?
│  └─ → MongoDB / Firestore
│
├─ Real-time updates required?
│  └─ → Firebase / Supabase Realtime
│
├─ Time-series data?
│  └─ → TimescaleDB / InfluxDB
│
└─ Graph relationships?
   └─ → Neo4j / ArangoDB
```

---

## Schema Design Principles

### Normalization Levels

| Level            | Description                        | Use Case              |
| ---------------- | ---------------------------------- | --------------------- |
| **1NF**          | Atomic values, no repeating groups | Always                |
| **2NF**          | 1NF + no partial dependencies      | Standard apps         |
| **3NF**          | 2NF + no transitive dependencies   | Most applications     |
| **BCNF**         | Stronger 3NF                       | Complex schemas       |
| **Denormalized** | Intentional redundancy             | Read-heavy, analytics |

### When to Denormalize

| Scenario                      | Consider Denormalization |
| ----------------------------- | ------------------------ |
| Frequent JOINs on same tables | ✅ Yes                   |
| Read-heavy workload           | ✅ Yes                   |
| Real-time analytics           | ✅ Yes                   |
| Write-heavy workload          | ❌ No                    |
| Data integrity critical       | ❌ No                    |

---

## Primary Key Selection

| Strategy           | Pros               | Cons             | Best For        |
| ------------------ | ------------------ | ---------------- | --------------- |
| **Auto-increment** | Simple, sequential | Not distributed  | Single DB       |
| **UUID v4**        | Globally unique    | Random, 36 chars | Distributed     |
| **ULID**           | Sortable, unique   | 26 chars         | Time-ordered    |
| **UUID v7**        | Sortable, unique   | Newer standard   | Modern apps     |
| **Composite**      | Natural keys       | Complex JOINs    | Junction tables |

**Recommendation:** Use UUID v7 or ULID for new projects (time-sortable + unique).

---

## Indexing Strategy

### Index Types

| Type          | Use Case                   | Example                    |
| ------------- | -------------------------- | -------------------------- |
| **B-Tree**    | Equality, range queries    | `WHERE status = 'active'`  |
| **Hash**      | Exact match only           | `WHERE id = 123`           |
| **GIN**       | Full-text, arrays, JSONB   | `WHERE tags @> ARRAY['a']` |
| **GiST**      | Geometric, range types     | `WHERE location <@ box`    |
| **Composite** | Multi-column queries       | `WHERE a = 1 AND b = 2`    |
| **Partial**   | Subset of rows             | `WHERE deleted_at IS NULL` |
| **Covering**  | Include all SELECT columns | Avoid table lookup         |

### Indexing Rules

| ✅ Index                 | ❌ Don't Index               |
| ------------------------ | ---------------------------- |
| WHERE clause columns     | Low cardinality (bool, enum) |
| JOIN condition columns   | Frequently updated columns   |
| ORDER BY columns         | Small tables (<1000 rows)    |
| Foreign keys             | Columns rarely queried       |
| High cardinality columns | Already indexed via PK       |

### Composite Index Order

```sql
-- Query: WHERE a = 1 AND b = 2 ORDER BY c
-- Index should be: (a, b, c)

-- Rule: Equality → Range → Sort
CREATE INDEX idx_example ON table (a, b, c);
```

---

## ORM Selection

| ORM            | Language   | Type Safety | Best For                |
| -------------- | ---------- | ----------- | ----------------------- |
| **Drizzle**    | TypeScript | ⭐⭐⭐      | Type-first, lightweight |
| **Prisma**     | TypeScript | ⭐⭐⭐      | Full-featured, DX focus |
| **Kysely**     | TypeScript | ⭐⭐⭐      | SQL-first, type-safe    |
| **TypeORM**    | TypeScript | ⭐⭐        | Enterprise, decorators  |
| **SQLAlchemy** | Python     | ⭐⭐⭐      | Full-featured, flexible |
| **GORM**       | Go         | ⭐⭐        | Go standard             |
| **Eloquent**   | PHP        | ⭐⭐        | Laravel ecosystem       |

### ORM Decision Tree

```
TypeScript project?
├─ Yes → Need raw SQL control?
│  ├─ Yes → Kysely or Drizzle
│  └─ No → Prisma
│
└─ No → Use language-native ORM
   ├─ Python → SQLAlchemy
   ├─ Go → GORM
   └─ PHP → Eloquent
```

---

## Query Optimization

### N+1 Problem

```typescript
// ❌ N+1 Problem
const users = await db.query("SELECT * FROM users");
for (const user of users) {
  user.posts = await db.query("SELECT * FROM posts WHERE user_id = ?", user.id);
}

// ✅ Eager Loading
const users = await db.query(`
  SELECT users.*, posts.*
  FROM users
  LEFT JOIN posts ON posts.user_id = users.id
`);
```

### EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Look for:
-- ❌ Seq Scan (full table scan)
-- ✅ Index Scan (using index)
-- ❌ High "actual time"
-- ✅ Low "actual time"
```

---

## Migration Best Practices

### Safe Migrations

| Operation     | Risk   | Safe Approach                                   |
| ------------- | ------ | ----------------------------------------------- |
| Add column    | Low    | Add nullable first, backfill, then set NOT NULL |
| Drop column   | High   | Stop reading first, deploy, then drop           |
| Rename column | High   | Add new, sync, drop old (multi-step)            |
| Add index     | Medium | CREATE INDEX CONCURRENTLY                       |
| Change type   | High   | Add new column, migrate, swap                   |

### Migration Checklist

- [ ] Tested on production-like data?
- [ ] Backward compatible?
- [ ] Rollback plan exists?
- [ ] No locks on large tables?
- [ ] Index created concurrently?

---

## Data Types Best Practices

| Data       | ✅ Use          | ❌ Avoid                |
| ---------- | --------------- | ----------------------- |
| Money      | `DECIMAL(19,4)` | `FLOAT`, `DOUBLE`       |
| Timestamps | `TIMESTAMPTZ`   | `TIMESTAMP` (no TZ)     |
| Short text | `VARCHAR(n)`    | `TEXT` for small fields |
| Long text  | `TEXT`          | `VARCHAR(10000)`        |
| Boolean    | `BOOLEAN`       | `INT`, `CHAR(1)`        |
| UUID       | `UUID` type     | `VARCHAR(36)`           |
| JSON       | `JSONB`         | `JSON` (no indexing)    |

---

## Anti-Patterns

| ❌ Don't                             | ✅ Do                    |
| ------------------------------------ | ------------------------ |
| Default to PostgreSQL for everything | Choose based on needs    |
| Use `SELECT *` in production         | Select specific columns  |
| Skip indexing                        | Index WHERE/JOIN columns |
| Store structured data as JSON        | Use proper columns       |
| Ignore N+1 queries                   | Use eager loading        |
| Run migrations without testing       | Test on prod-like data   |
| Store dates as strings               | Use proper DATE types    |
| No foreign key constraints           | Define relationships     |

---

## Database Design Checklist

Before implementation:

- [ ] Identified write vs read patterns?
- [ ] Chosen appropriate database type?
- [ ] Designed normalized schema (3NF)?
- [ ] Identified denormalization needs?
- [ ] Selected primary key strategy?
- [ ] Planned indexing strategy?
- [ ] Chosen ORM for project?
- [ ] Defined migration strategy?

---

## Related Skills

| Need              | Skill                   |
| ----------------- | ----------------------- |
| API design        | `api-patterns`          |
| Backend patterns  | `nodejs-best-practices` |
| Query performance | `performance-profiling` |
| Security          | `security-fundamentals` |

---

> **Remember:** The best database design is one that matches your access patterns. Design for how data is used, not just how it's stored.
