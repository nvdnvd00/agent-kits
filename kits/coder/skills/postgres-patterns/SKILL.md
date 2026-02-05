---
name: postgres-patterns
description: PostgreSQL-specific optimization and advanced features. Use when designing PostgreSQL schemas, optimizing queries, implementing RLS, partitioning, or troubleshooting performance. Database-agnostic concepts are in database-design skill.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# PostgreSQL Patterns - Advanced Optimization

> **Philosophy:** PostgreSQL is not just a database—it's a platform. Master its unique features to build performant, secure systems.

---

## When to Use This Skill

| ✅ Use                          | ❌ Don't Use                 |
| ------------------------------- | ---------------------------- |
| PostgreSQL schema design        | Database-agnostic design     |
| Query optimization with EXPLAIN | Choosing between databases   |
| Row-Level Security (RLS)        | ORM selection                |
| Partitioning strategies         | Non-PostgreSQL databases     |
| PostgreSQL-specific data types  | Basic normalization concepts |
| JSONB, arrays, range types      | N+1 query patterns (use ORM) |

➡️ For general database concepts, see `database-design` skill.

---

## Core Rules (Non-Negotiable)

1. **TIMESTAMPTZ only** - Never use `TIMESTAMP` without timezone
2. **TEXT over VARCHAR** - Use `TEXT` with `CHECK` constraints
3. **IDENTITY over SERIAL** - Use `GENERATED ALWAYS AS IDENTITY`
4. **FK indexes are manual** - PostgreSQL does NOT auto-index foreign keys
5. **EXPLAIN ANALYZE first** - Measure before optimizing

---

## Data Type Selection

### Preferred Types

| Data Type       | ✅ Use                | ❌ Avoid                             |
| --------------- | --------------------- | ------------------------------------ |
| **IDs**         | `BIGINT IDENTITY`     | `SERIAL`, `INTEGER`                  |
| **Distributed** | `UUID` (v7 preferred) | `VARCHAR(36)`                        |
| **Strings**     | `TEXT`                | `VARCHAR(n)`, `CHAR(n)`              |
| **Money**       | `NUMERIC(p,s)`        | `FLOAT`, `DOUBLE PRECISION`, `MONEY` |
| **Timestamps**  | `TIMESTAMPTZ`         | `TIMESTAMP`, `TIMETZ`                |
| **Booleans**    | `BOOLEAN NOT NULL`    | `INTEGER`, `CHAR(1)`                 |
| **JSON**        | `JSONB`               | `JSON` (no indexing)                 |

### Special Types

```sql
-- Arrays: Tags, categories
tags TEXT[] NOT NULL DEFAULT '{}'
CREATE INDEX ON table USING GIN (tags);

-- Range types: Scheduling, versioning
booking_period TSTZRANGE NOT NULL
EXCLUDE USING GIST (room_id WITH =, booking_period WITH &&)

-- Network types
ip_address INET NOT NULL
CREATE INDEX ON table USING GIST (ip_address inet_ops);

-- Full-text search
search_vector TSVECTOR GENERATED ALWAYS AS (
  to_tsvector('english', title || ' ' || content)
) STORED
CREATE INDEX ON table USING GIN (search_vector);
```

---

## Indexing Strategy

### Index Type Decision Tree

```
What query pattern?
│
├─ Equality/Range (=, <, >, BETWEEN)?
│  └─ → B-Tree (default)
│
├─ JSONB containment (@>, ?, ?|)?
│  └─ → GIN (jsonb_ops or jsonb_path_ops)
│
├─ Full-text search (@@)?
│  └─ → GIN on TSVECTOR
│
├─ Array containment (@>, &&)?
│  └─ → GIN
│
├─ Range overlap/containment?
│  └─ → GiST
│
├─ Time-series (huge tables, ordered inserts)?
│  └─ → BRIN (minimal storage)
│
└─ Partial index (subset of rows)?
   └─ → Partial B-Tree with WHERE clause
```

### Index Patterns

```sql
-- Composite: Order matters! (Equality → Range → Sort)
CREATE INDEX ON orders (user_id, status, created_at);

-- Partial: Hot subset indexing
CREATE INDEX ON orders (created_at)
WHERE status = 'pending';

-- Expression: Case-insensitive search
CREATE INDEX ON users (LOWER(email));

-- Covering: Index-only scans
CREATE INDEX ON orders (user_id) INCLUDE (status, total);

-- BRIN: Time-series (1000x smaller than B-tree)
CREATE INDEX ON events USING BRIN (created_at) WITH (pages_per_range = 128);
```

### JSONB Indexing

```sql
-- Default GIN: All operators (@>, ?, ?|, ?&)
CREATE INDEX ON products USING GIN (metadata);

-- jsonb_path_ops: Smaller, faster BUT only @> containment
CREATE INDEX ON products USING GIN (metadata jsonb_path_ops);

-- Extract hot path to B-tree column
ALTER TABLE products ADD COLUMN price NUMERIC
  GENERATED ALWAYS AS ((metadata->>'price')::NUMERIC) STORED;
CREATE INDEX ON products (price);
```

---

## Query Optimization

### EXPLAIN ANALYZE Cheatsheet

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = 123;

-- Key metrics:
-- ✅ Index Scan / Index Only Scan
-- ❌ Seq Scan on large tables (>10k rows)
-- ✅ Low "actual time"
-- ❌ High "shared hit" + "shared read" (I/O bound)
```

### Common Optimizations

| Problem                  | Solution                             |
| ------------------------ | ------------------------------------ |
| Seq Scan on filtered col | Add index on WHERE columns           |
| Slow ORDER BY            | Index matches ORDER BY columns       |
| Low selectivity          | Partial index on common filter       |
| JSONB field queries      | Extract to generated column + B-tree |
| LIKE '%pattern%'         | pg_trgm extension + GIN index        |
| Cross-table queries      | Covering index with INCLUDE          |

### Join Optimization

```sql
-- ❌ Slow: No index on FK
SELECT * FROM orders o
JOIN users u ON u.id = o.user_id;

-- ✅ Fast: Index on FK column
CREATE INDEX ON orders (user_id);
```

---

## Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their documents
CREATE POLICY user_documents ON documents
  FOR ALL
  TO app_users
  USING (user_id = current_setting('app.current_user_id')::BIGINT);

-- Multi-tenant: Tenant isolation
CREATE POLICY tenant_isolation ON orders
  FOR ALL
  USING (tenant_id = current_setting('app.tenant_id')::BIGINT);

-- Force RLS for table owner too
ALTER TABLE documents FORCE ROW LEVEL SECURITY;
```

---

## Partitioning Strategy

### When to Partition

| Criteria       | Threshold        |
| -------------- | ---------------- |
| Table size     | > 100M rows      |
| Query filter   | Always on date   |
| Data lifecycle | Retention policy |
| Maintenance    | Bulk deletes     |

### Partition Types

```sql
-- RANGE: Time-series data
CREATE TABLE events (
  id BIGINT GENERATED ALWAYS AS IDENTITY,
  created_at TIMESTAMPTZ NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- LIST: Regional/categorical data
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  region TEXT NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders
  FOR VALUES IN ('us-east', 'us-west');

-- HASH: Even distribution
CREATE TABLE sessions (
  user_id BIGINT NOT NULL
) PARTITION BY HASH (user_id);

CREATE TABLE sessions_0 PARTITION OF sessions
  FOR VALUES WITH (MODULUS 4, REMAINDER 0);
```

### Partition Gotchas

- **No global UNIQUE** - PK must include partition key
- **No FK from partitioned** - Use triggers instead
- **Query must filter** - Include partition key in WHERE

---

## Upsert Patterns

```sql
-- Basic upsert
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name, updated_at = NOW();

-- Upsert with conditions
INSERT INTO inventory (product_id, quantity)
VALUES (1, 10)
ON CONFLICT (product_id)
DO UPDATE SET quantity = inventory.quantity + EXCLUDED.quantity
WHERE inventory.quantity < 100;

-- Bulk upsert
INSERT INTO products (id, name, price)
SELECT * FROM UNNEST(
  ARRAY[1, 2, 3]::BIGINT[],
  ARRAY['A', 'B', 'C']::TEXT[],
  ARRAY[10.0, 20.0, 30.0]::NUMERIC[]
)
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name, price = EXCLUDED.price;
```

---

## Safe Schema Evolution

| Operation     | Risk   | Safe Approach                                |
| ------------- | ------ | -------------------------------------------- |
| Add column    | Low    | `ADD COLUMN` with DEFAULT (PG11+ is instant) |
| Add NOT NULL  | Medium | Add column → backfill → set NOT NULL         |
| Drop column   | High   | Stop reading → deploy → drop                 |
| Add index     | Medium | `CREATE INDEX CONCURRENTLY`                  |
| Change type   | High   | Add new → migrate → swap → drop old          |
| Rename column | High   | Add alias → migrate code → drop old          |

```sql
-- Safe index creation (no locks)
CREATE INDEX CONCURRENTLY idx_orders_user ON orders (user_id);

-- Safe NOT NULL addition
ALTER TABLE users ADD COLUMN phone TEXT;
UPDATE users SET phone = '' WHERE phone IS NULL;
ALTER TABLE users ALTER COLUMN phone SET NOT NULL;
```

---

## Essential Extensions

| Extension     | Use Case                     | Key Functions                   |
| ------------- | ---------------------------- | ------------------------------- |
| `pgcrypto`    | Password hashing, encryption | `crypt()`, `gen_random_uuid()`  |
| `pg_trgm`     | Fuzzy text search            | `%`, `similarity()`, GIN index  |
| `TimescaleDB` | Time-series data             | Auto-partitioning, compression  |
| `PostGIS`     | Geospatial                   | `ST_Distance()`, `ST_Within()`  |
| `pgvector`    | Vector embeddings            | `<=>`, `<->` operators          |
| `pgaudit`     | Audit logging                | Statement/object-level auditing |

---

## Performance Checklist

Before production:

- [ ] All FK columns indexed?
- [ ] Queries use EXPLAIN ANALYZE?
- [ ] Partial indexes for hot filters?
- [ ] JSONB hot paths extracted?
- [ ] RLS policies tested?
- [ ] Partitioning for large tables?
- [ ] Connection pooling configured?
- [ ] Vacuum/autovacuum tuned?

---

## Anti-Patterns

| ❌ Don't                     | ✅ Do                               |
| ---------------------------- | ----------------------------------- |
| Use TIMESTAMP without TZ     | Use TIMESTAMPTZ                     |
| VARCHAR(n) for variable text | TEXT with CHECK constraints         |
| SERIAL for IDs               | BIGINT GENERATED ALWAYS AS IDENTITY |
| JSON type                    | JSONB (indexable, smaller)          |
| Index every column           | Index query patterns                |
| Ignore EXPLAIN output        | Analyze before optimizing           |
| Store arrays for relations   | Use junction tables                 |
| Mixed-case identifiers       | snake_case (unquoted)               |

---

## Related Skills

| Need              | Skill                   |
| ----------------- | ----------------------- |
| General DB design | `database-design`       |
| API integration   | `api-patterns`          |
| Query performance | `performance-profiling` |
| Security patterns | `security-fundamentals` |

---

> **Remember:** PostgreSQL rewards those who understand its features. EXPLAIN everything, index strategically, and leverage its unique capabilities.
