---
name: performance-profiling
description: Performance profiling principles and decision-making. Use when diagnosing slow code, optimizing response times, analyzing Core Web Vitals, or establishing performance budgets. Covers measurement, analysis, and optimization techniques.
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# Performance Profiling - Measure First, Optimize Second

## ⚡ Quick Reference

- **Measure first**: Profile before optimizing · No gut feelings · `console.time()` / Chrome DevTools / clinic.js
- **Core Web Vitals**: LCP < 2.5s · FID/INP < 200ms · CLS < 0.1 · Check with Lighthouse
- **Frontend**: Lazy load images/routes · Eliminate render-blocking resources · Bundle splitting · `preconnect` for external
- **Backend**: EXPLAIN ANALYZE for slow queries · Connection pooling · Response caching (Redis) · Pagination
- **Node.js**: Event loop not blocked · Avoid sync fs in hot paths · `--prof` for CPU profiling
- **Priority**: Fix worst P99 first · Cache before compute · Network before CPU

---


---

## 🎯 Core Principle: Data-Driven Optimization

```
❌ WRONG: "This looks slow, let me refactor it to be faster"
✅ CORRECT: "I measured this takes 850ms, my target is 200ms, profiling shows 70% in DB query"
```

**Performance Optimization Workflow:**

```
1. BASELINE  → Measure current state
2. PROFILE   → Find the bottleneck
3. ANALYZE   → Understand root cause
4. OPTIMIZE  → Fix the specific issue
5. VALIDATE  → Verify improvement
6. MONITOR   → Prevent regression
```

---

## 📊 What to Measure

### Web Performance: Core Web Vitals

| Metric                              | What It Measures | Good    | Needs Work | Poor    |
| ----------------------------------- | ---------------- | ------- | ---------- | ------- |
| **LCP** (Largest Contentful Paint)  | Loading          | ≤ 2.5s  | 2.5-4.0s   | > 4.0s  |
| **INP** (Interaction to Next Paint) | Responsiveness   | ≤ 200ms | 200-500ms  | > 500ms |
| **CLS** (Cumulative Layout Shift)   | Visual Stability | ≤ 0.1   | 0.1-0.25   | > 0.25  |

### Backend Performance

| Metric                  | Target  | Critical |
| ----------------------- | ------- | -------- |
| API Response Time (p50) | < 100ms | > 500ms  |
| API Response Time (p95) | < 300ms | > 1s     |
| API Response Time (p99) | < 1s    | > 3s     |
| Database Query          | < 50ms  | > 200ms  |
| Background Job          | < 30s   | > 5min   |
| Memory Usage            | < 80%   | > 95%    |
| CPU Usage               | < 70%   | > 90%    |

### Decision: Which Metric to Prioritize?

```
User-facing latency?
├── Yes → Focus on p95/p99 latency first
└── No (batch job) → Focus on throughput and resource usage

High traffic volume?
├── Yes → Optimize p50 for most impact
└── No → Optimize p99 to catch edge cases

User perceives slowness?
├── Yes → Measure Time to Interactive (TTI)
└── No → Check if perceived speed is the real issue
```

---

## 🔍 Profiling Decision Tree

### Frontend Performance

```
Page loads slowly?
├── Check LCP element
│   ├── Large image? → Compress, use WebP, lazy load
│   ├── Web font? → Preload, use font-display: swap
│   └── Server slow? → Check TTFB (Time to First Byte)
│
├── Check blocking resources
│   ├── Large JS bundle? → Code split, tree shake
│   ├── Render-blocking CSS? → Inline critical CSS
│   └── Third-party scripts? → Defer, async load
│
└── Check waterfalls in DevTools Network tab
```

### Backend Performance

```
API is slow?
├── Where is time spent?
│   ├── Database query → Check query plan, add indexes
│   ├── External API → Add caching, circuit breaker
│   ├── CPU processing → Profile code, optimize algorithm
│   └── Memory allocation → Check for leaks, reduce allocations
│
├── Is it consistent or intermittent?
│   ├── Consistent → Systemic issue (algorithm, query)
│   └── Intermittent → Check for lock contention, GC pauses
│
└── Does it scale?
    ├── No → O(n²) algorithm? N+1 queries?
    └── Yes → Infrastructure bottleneck?
```

---

## 🛠️ Profiling Tools

### Frontend

| Tool                        | Purpose                   | When to Use                          |
| --------------------------- | ------------------------- | ------------------------------------ |
| Chrome DevTools Performance | Recording-based profiling | Investigating specific interactions  |
| Lighthouse                  | Automated audits          | Quick health check                   |
| WebPageTest                 | Real-world testing        | Testing from different locations     |
| PageSpeed Insights          | Field + Lab data          | SEO + real user metrics              |
| Chrome UX Report            | Real user data            | Understanding actual user experience |

### Backend (Node.js)

| Tool                   | Purpose                 | When to Use                |
| ---------------------- | ----------------------- | -------------------------- |
| `clinic.js`            | Comprehensive profiling | First investigation        |
| `node --prof`          | V8 CPU profiler         | Deep CPU analysis          |
| `--inspect` + DevTools | Interactive debugging   | Memory leaks, async issues |
| `0x`                   | Flame graphs            | Visualizing CPU time       |
| `autocannon` / `k6`    | Load testing            | Stress testing endpoints   |

### Database

| Tool                 | Purpose              | When to Use               |
| -------------------- | -------------------- | ------------------------- |
| `EXPLAIN ANALYZE`    | Query execution plan | Slow query investigation  |
| `pg_stat_statements` | Query statistics     | Finding slow queries      |
| MongoDB Profiler     | Operation profiling  | Slow operation detection  |
| Redis `SLOWLOG`      | Slow command log     | Identifying slow commands |

---

## ⚡ Common Bottlenecks & Solutions

### N+1 Queries

**Detection:**

```
10 users requested → 1 query for users + 10 queries for profiles
Pattern: Query count scales with data size
```

**Solution:**

```typescript
// ❌ N+1 Problem
const users = await User.findAll();
for (const user of users) {
  user.profile = await Profile.findOne({ userId: user.id });
}

// ✅ Eager Loading
const users = await User.findAll({
  include: [{ model: Profile }],
});

// ✅ Batching
const users = await User.findAll();
const profiles = await Profile.findAll({
  where: { userId: users.map((u) => u.id) },
});
```

### Missing Database Indexes

**Detection:**

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
-- Look for: Seq Scan (bad) vs Index Scan (good)
```

**Solution:**

```sql
-- Add index on frequently filtered columns
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index for common query patterns
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### Large Bundle Size

**Detection:**

```bash
# Analyze bundle composition
npx webpack-bundle-analyzer dist/stats.json
```

**Solutions:**
| Problem | Solution |
| ------- | -------- |
| Large library | Use lighter alternative (date-fns vs moment) |
| Unused exports | Enable tree shaking |
| One big bundle | Code split by route |
| Duplicate dependencies | Dedupe in package manager |

### Memory Leaks

**Detection:**

- Memory usage increases over time
- Heap dumps show growing object counts
- OutOfMemory errors in production

**Common Causes:**
| Cause | Solution |
| ----- | -------- |
| Event listeners not removed | Cleanup in useEffect/componentWillUnmount |
| Growing global arrays/maps | Use WeakMap/WeakSet or bounded caches |
| Closures holding references | Break reference chains |
| Uncleared timers | clearTimeout/clearInterval |

---

## 📈 Optimization Patterns

### Caching Strategy

| Data Type        | Cache Location | TTL Strategy                  |
| ---------------- | -------------- | ----------------------------- |
| Static assets    | CDN            | Long (1 year) + cache busting |
| API responses    | Redis          | Short (5-60 min)              |
| Computed values  | In-memory      | Based on computation cost     |
| Database queries | Query cache    | Invalidate on write           |
| User sessions    | Redis          | Based on session requirements |

### Lazy Loading

```typescript
// ✅ Lazy load components
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// ✅ Lazy load images
<img loading="lazy" src="below-fold.jpg" />

// ✅ Lazy load data
const data = useSWR(isVisible ? '/api/data' : null);
```

### Debouncing & Throttling

| Technique | Use Case                  | Example                   |
| --------- | ------------------------- | ------------------------- |
| Debounce  | Wait until activity stops | Search input autocomplete |
| Throttle  | Limit frequency           | Scroll handlers, resize   |

```typescript
// Debounce: Execute after 300ms of no calls
const debouncedSearch = debounce(search, 300);

// Throttle: Execute at most once per 100ms
const throttledScroll = throttle(handleScroll, 100);
```

---

## 🚨 Anti-Patterns

| ❌ Don't                          | ✅ Do                                      |
| --------------------------------- | ------------------------------------------ |
| Optimize without measuring        | Profile first, then optimize               |
| Premature optimization            | Focus on correctness, then performance     |
| Optimize cold paths               | Focus on hot paths (frequently executed)   |
| Micro-optimize trivial code       | Target the biggest bottleneck              |
| Cache everything                  | Cache strategically, consider invalidation |
| Load everything upfront           | Lazy load non-critical resources           |
| Block main thread with heavy work | Use web workers, async processing          |
| Ignore p99 latency                | p99 affects real users, not just averages  |

---

## 📋 Performance Budget Template

```markdown
## Performance Budget: [Project Name]

### Core Web Vitals

- LCP: < 2.5s
- INP: < 200ms
- CLS: < 0.1

### Resource Budgets

- Total page weight: < 500KB (compressed)
- JavaScript: < 200KB (compressed)
- CSS: < 50KB (compressed)
- Images: < 200KB total (above the fold)

### API Performance

- p50 latency: < 100ms
- p95 latency: < 300ms
- p99 latency: < 1s

### Monitoring

- Alert if LCP > 3s for > 5% of users
- Alert if error rate > 1%
- Alert if API p95 > 500ms
```

---

## 🔗 Related Skills

| Need                  | Skill                  |
| --------------------- | ---------------------- |
| Frontend optimization | `react-best-practices` |
| Database optimization | `database-design`      |
| Testing performance   | `testing-patterns`     |
| Clean efficient code  | `clean-code`           |

---

> **Remember:** The fastest code is the code that doesn't run. Eliminate unnecessary work before micro-optimizing.
