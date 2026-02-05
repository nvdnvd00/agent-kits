---
name: redis-patterns
description: Redis caching, pub/sub, sessions, and data structure patterns. Use when implementing caching layers, real-time features, rate limiting, session management, or distributed locking with Redis.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# Redis Patterns - Caching & Real-Time

> **Philosophy:** Redis is not just a cache—it's a data structure server. Use the right structure for the right problem.

---

## When to Use This Skill

| ✅ Use                 | ❌ Don't Use                 |
| ---------------------- | ---------------------------- |
| Caching strategies     | Primary database design      |
| Session management     | Complex querying             |
| Rate limiting          | Relational data              |
| Pub/Sub messaging      | Durable storage requirements |
| Distributed locking    | ACID transactions            |
| Real-time leaderboards | Large document storage       |
| Queue/Job patterns     | Complex aggregations         |

---

## Core Rules (Non-Negotiable)

1. **TTL everything** - Set expiration on all cache keys
2. **Namespace keys** - Use prefixes: `{app}:{entity}:{id}`
3. **Atomic operations** - Use built-in commands over multi-step
4. **Memory monitoring** - Track memory usage with policies
5. **Connection pooling** - Reuse connections, don't create per request

---

## Data Structure Decision Tree

```
What's your use case?
│
├─ Simple key-value cache?
│  └─ → STRING with TTL
│
├─ Object/document cache?
│  └─ → HASH (field-level access)
│
├─ Unique collection (tags, flags)?
│  └─ → SET
│
├─ Ordered data (leaderboards, timelines)?
│  └─ → SORTED SET (ZSET)
│
├─ Queue/stack (FIFO, LIFO)?
│  └─ → LIST (LPUSH/RPOP or RPUSH/LPOP)
│
├─ Real-time messaging?
│  └─ → Pub/Sub or Streams
│
└─ Counting/existence checking?
   └─ → HyperLogLog (cardinality) or Bloom Filter
```

---

## Caching Patterns

### Cache-Aside (Lazy Loading)

```typescript
async function getUser(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;

  // Check cache first
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Cache miss: fetch from DB
  const user = await db.users.findById(userId);

  // Store in cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(user)); // 1 hour

  return user;
}
```

### Write-Through

```typescript
async function updateUser(userId: string, data: Partial<User>): Promise<User> {
  // Update DB first
  const user = await db.users.update(userId, data);

  // Update cache immediately
  const cacheKey = `user:${userId}`;
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```

### Write-Behind (Async)

```typescript
async function updateUserAsync(
  userId: string,
  data: Partial<User>,
): Promise<void> {
  const cacheKey = `user:${userId}`;

  // Update cache immediately
  await redis.hset(cacheKey, data);

  // Queue DB update
  await redis.lpush("db:updates:user", JSON.stringify({ userId, data }));
}

// Background worker processes queue
```

### Cache Invalidation

```typescript
// Pattern: Event-driven invalidation
async function onUserUpdated(userId: string): Promise<void> {
  await redis.del(`user:${userId}`);
  await redis.del(`user:${userId}:profile`);
  await redis.del(`user:${userId}:posts`);
}

// Pattern: Tag-based invalidation
async function invalidateByTag(tag: string): Promise<void> {
  const keys = await redis.smembers(`tag:${tag}`);
  if (keys.length > 0) {
    await redis.del(...keys);
    await redis.del(`tag:${tag}`);
  }
}
```

---

## Session Management

```typescript
// Session storage with HASH
const sessionKey = `session:${sessionId}`;

// Create session
await redis.hset(sessionKey, {
  userId: user.id,
  email: user.email,
  role: user.role,
  createdAt: Date.now(),
});
await redis.expire(sessionKey, 86400); // 24 hours

// Get session
const session = await redis.hgetall(sessionKey);

// Extend session on activity
await redis.expire(sessionKey, 86400);

// Destroy session
await redis.del(sessionKey);

// Force logout all sessions for user
const sessionKeys = await redis.keys(`session:*:${userId}`);
await redis.del(...sessionKeys);
```

---

## Rate Limiting

### Fixed Window

```typescript
async function checkRateLimit(
  key: string,
  limit: number,
  windowSec: number,
): Promise<boolean> {
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, windowSec);
  }

  return current <= limit;
}

// Usage: 100 requests per minute
const allowed = await checkRateLimit(`ratelimit:${userId}:api`, 100, 60);
```

### Sliding Window (More Accurate)

```typescript
async function slidingWindowRateLimit(
  key: string,
  limit: number,
  windowMs: number,
): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - windowMs;

  // Remove old entries
  await redis.zremrangebyscore(key, "-inf", windowStart);

  // Count current window
  const count = await redis.zcard(key);

  if (count >= limit) return false;

  // Add current request
  await redis.zadd(key, now, `${now}:${Math.random()}`);
  await redis.expire(key, Math.ceil(windowMs / 1000));

  return true;
}
```

### Token Bucket

```typescript
async function tokenBucket(
  key: string,
  capacity: number,
  refillRate: number, // tokens per second
): Promise<boolean> {
  const now = Date.now();
  const data = await redis.hgetall(key);

  let tokens = parseFloat(data.tokens) || capacity;
  let lastRefill = parseInt(data.lastRefill) || now;

  // Refill tokens based on time elapsed
  const elapsed = (now - lastRefill) / 1000;
  tokens = Math.min(capacity, tokens + elapsed * refillRate);

  if (tokens < 1) return false;

  // Consume token
  await redis.hset(key, {
    tokens: tokens - 1,
    lastRefill: now,
  });
  await redis.expire(key, 3600);

  return true;
}
```

---

## Distributed Locking

### Simple Lock (Redlock Pattern)

```typescript
async function acquireLock(key: string, ttlMs: number): Promise<string | null> {
  const lockKey = `lock:${key}`;
  const lockValue = crypto.randomUUID();

  const acquired = await redis.set(lockKey, lockValue, "PX", ttlMs, "NX");

  return acquired ? lockValue : null;
}

async function releaseLock(key: string, lockValue: string): Promise<boolean> {
  const lockKey = `lock:${key}`;

  // Lua script for atomic check-and-delete
  const script = `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `;

  const result = await redis.eval(script, 1, lockKey, lockValue);
  return result === 1;
}

// Usage
const lock = await acquireLock("process:order:123", 30000);
if (lock) {
  try {
    await processOrder(123);
  } finally {
    await releaseLock("process:order:123", lock);
  }
}
```

---

## Pub/Sub Messaging

```typescript
// Publisher
async function publishEvent(channel: string, event: object): Promise<void> {
  await redis.publish(channel, JSON.stringify(event));
}

// Subscriber
const subscriber = redis.duplicate();
await subscriber.subscribe("orders", "payments");

subscriber.on("message", (channel, message) => {
  const event = JSON.parse(message);
  console.log(`[${channel}]`, event);
});

// Publish examples
await publishEvent("orders", { type: "created", orderId: "123" });
await publishEvent("payments", { type: "completed", paymentId: "456" });
```

### Redis Streams (Persistent)

```typescript
// Add to stream
await redis.xadd(
  "events",
  "*",
  "type",
  "order.created",
  "data",
  JSON.stringify(order),
);

// Consumer group
await redis.xgroup("CREATE", "events", "workers", "0", "MKSTREAM");

// Read as consumer
const entries = await redis.xreadgroup(
  "GROUP",
  "workers",
  "worker-1",
  "COUNT",
  10,
  "BLOCK",
  5000,
  "STREAMS",
  "events",
  ">",
);

// Acknowledge processed
await redis.xack("events", "workers", entryId);
```

---

## Leaderboard Pattern

```typescript
// Add/Update score
await redis.zadd("leaderboard:weekly", score, `user:${userId}`);

// Get rank (0-indexed)
const rank = await redis.zrevrank("leaderboard:weekly", `user:${userId}`);

// Get top 10
const top10 = await redis.zrevrange("leaderboard:weekly", 0, 9, "WITHSCORES");

// Get score
const score = await redis.zscore("leaderboard:weekly", `user:${userId}`);

// Get nearby ranks
const myRank = await redis.zrevrank("leaderboard:weekly", `user:${userId}`);
const nearby = await redis.zrevrange(
  "leaderboard:weekly",
  Math.max(0, myRank - 5),
  myRank + 5,
  "WITHSCORES",
);

// Weekly reset (TTL on key creation)
await redis.expire("leaderboard:weekly", 604800); // 7 days
```

---

## Memory Management

### Eviction Policies

| Policy           | Use Case                      |
| ---------------- | ----------------------------- |
| `noeviction`     | Fail writes when memory full  |
| `allkeys-lru`    | General caching (recommended) |
| `volatile-lru`   | Only evict keys with TTL      |
| `allkeys-lfu`    | Frequency-based eviction      |
| `allkeys-random` | Random eviction               |

### Memory Optimization

```bash
# Check memory usage
redis-cli INFO memory

# Analyze key sizes
redis-cli --bigkeys

# Memory usage for specific key
MEMORY USAGE mykey
```

```typescript
// Use HASH for objects (more compact than JSON strings)
// ❌ Less efficient
await redis.set("user:123", JSON.stringify(user));

// ✅ More efficient
await redis.hset("user:123", user);
```

---

## Key Naming Convention

```
{app}:{entity}:{id}:{subkey}

Examples:
- myapp:user:123              - User data
- myapp:user:123:session      - User session
- myapp:cache:products:456    - Cached product
- myapp:ratelimit:ip:1.2.3.4  - Rate limit counter
- myapp:lock:order:789        - Distributed lock
- myapp:queue:emails          - Email queue
- myapp:leaderboard:weekly    - Weekly leaderboard
```

---

## Anti-Patterns

| ❌ Don't                        | ✅ Do                                 |
| ------------------------------- | ------------------------------------- |
| Store without TTL               | Always set expiration                 |
| Use KEYS in production          | Use SCAN for iteration                |
| Large values (>1MB)             | Split or use different storage        |
| Create connection per request   | Use connection pooling                |
| Use as primary database         | Use as cache/session/queue layer      |
| Block with BLPOP in main thread | Dedicated subscriber connections      |
| Store complex relational data   | Use proper database for relations     |
| Ignore memory limits            | Configure maxmemory + eviction policy |

---

## Production Checklist

Before deployment:

- [ ] Connection pooling configured?
- [ ] Memory limits set (maxmemory)?
- [ ] Eviction policy appropriate?
- [ ] TTL on all cache keys?
- [ ] Key namespacing consistent?
- [ ] Persistence configured (if needed)?
- [ ] Replica for high availability?
- [ ] Monitoring/alerting in place?

---

## Related Skills

| Need                  | Skill                   |
| --------------------- | ----------------------- |
| Message queues        | `queue-patterns`        |
| Database caching      | `database-design`       |
| Real-time patterns    | `realtime-patterns`     |
| Performance profiling | `performance-profiling` |

---

> **Remember:** Redis shines when you use the right data structure for your problem. Don't force every use case into strings—explore sets, sorted sets, and hashes.
