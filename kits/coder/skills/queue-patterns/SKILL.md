---
name: queue-patterns
description: Message queue and background job processing patterns. Use when designing job queues, implementing retry strategies, building worker pools, or handling dead letter queues. Covers BullMQ, RabbitMQ, and distributed job scheduling.
version: 1.0.0
tags: [architecture, queue, jobs, async, reliability]
---

# Queue Patterns - Background Job Processing Skill

## ⚡ Quick Reference

- **System selection**: Node.js → BullMQ · Python → Celery · Serverless → SQS · Multi-lang → RabbitMQ · Streaming → Kafka
- **Job design**: Small payload (IDs only) · Idempotency key · Include tenant_id/correlation_id · Set timeout
- **Retry**: Exponential backoff · Max 3-5 attempts · Dead Letter Queue after max retries · DLQ monitored
- **Idempotency**: Running same job 2x = same result · Check before write · Deduplication key
- **Concurrency**: Bounded limits · Rate limit external API calls · Separate queues by priority (fast/normal/bulk)
- **Monitoring**: Queue depth · Processing time · DLQ count · Stalled jobs alerts

---


---

## 📑 Navigation

- [Philosophy](#-philosophy)
- [Queue Selection](#-queue-selection)
- [Job Design](#-job-design)
- [Retry Strategies](#-retry-strategies)
- [Decision Frameworks](#-decision-frameworks)
- [Anti-Patterns](#-anti-patterns)
- [Checklist](#-implementation-checklist)

---

## 💡 Philosophy

> **"A queue is a promise: jobs go in, results come out, nothing is lost."**

- **Jobs Are Sacred**: Every job must complete, fail explicitly, or move to DLQ
- **Idempotency by Design**: Same job running twice = same outcome
- **Reliability Over Speed**: Slow and correct beats fast and lossy
- **Observability Mandatory**: Every job traceable from start to end
- **Fail Closed**: Unknown errors → retry, not ignore

---

## 🔧 QUEUE SELECTION

### Technology Comparison

| System       | Language | Persistence | Best For                         | Complexity |
| ------------ | -------- | ----------- | -------------------------------- | ---------- |
| **BullMQ**   | Node.js  | Redis       | Feature-rich, delays, priorities | Low        |
| **RabbitMQ** | Multi    | Disk        | Routing, multi-language          | Medium     |
| **AWS SQS**  | Any      | Managed     | Serverless, Lambda               | Low        |
| **Kafka**    | Any      | Disk        | High throughput, streaming       | High       |
| **Celery**   | Python   | Redis/AMQP  | Distributed Python tasks         | Medium     |

### Selection Decision Tree

```
START
  │
  ▼
┌────────────────────┐
│ What's the stack?  │
└────────────────────┘
  │
  ├── Node.js + Redis → BullMQ
  ├── Python → Celery or ARQ
  ├── Serverless → SQS + Lambda
  ├── Multi-language → RabbitMQ
  └── High throughput/streaming → Kafka
```

### Redis Persistence for BullMQ

| Mode         | Durability | Performance | When to Use             |
| ------------ | ---------- | ----------- | ----------------------- |
| **RDB only** | Low        | High        | Dev/test only           |
| **AOF**      | High       | Medium      | Production default      |
| **AOF+RDB**  | Highest    | Lower       | Critical/financial jobs |

---

## 📦 JOB DESIGN

### Job Payload Best Practices

```typescript
// ❌ BAD: Large objects in payload
queue.add("processOrder", {
  order: {
    /* full order object with 100+ fields */
  },
  customer: {
    /* full customer object */
  },
});

// ✅ GOOD: IDs only, fetch fresh in worker
queue.add("processOrder", {
  orderId: "order-123",
  customerId: "cust-456",
  tenantId: "tenant-789", // Multi-tenant context
  idempotencyKey: "order-123-v1", // Deduplication
  correlationId: "req-uuid-abc", // Tracing
});
```

### Required Job Context (Multi-tenant)

| Field            | Purpose                         | Required    |
| ---------------- | ------------------------------- | ----------- |
| `tenantId`       | Tenant context for multi-tenant | Yes         |
| `idempotencyKey` | Prevent duplicate processing    | Yes         |
| `correlationId`  | Request tracing                 | Yes         |
| `userId`         | Audit trail                     | Recommended |
| `priority`       | Queue prioritization            | Optional    |

### Job Lifecycle States

```
WAITING → ACTIVE → COMPLETED
            │
            ├──▶ FAILED → RETRY → (back to WAITING)
            │         │
            │         └──▶ MAX RETRIES → DEAD LETTER
            │
            └──▶ STALLED → AUTO-RETRY (worker crashed)
```

---

## 🔄 RETRY STRATEGIES

### Retry Pattern Comparison

| Strategy         | Formula                     | Use Case                | Example                 |
| ---------------- | --------------------------- | ----------------------- | ----------------------- |
| **Fixed**        | `delay`                     | Simple transient errors | `5s, 5s, 5s`            |
| **Exponential**  | `base * 2^attempt`          | API rate limits         | `1s, 2s, 4s, 8s`        |
| **Exp + Jitter** | `base * 2^n + random(0, 1)` | Distributed systems     | Prevent thundering herd |
| **Linear**       | `base * attempt`            | Gradual backoff         | `5s, 10s, 15s, 20s`     |

### BullMQ Retry Configuration

```typescript
// Recommended configuration
{
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 1000, // 1s base
  },
  removeOnComplete: {
    age: 3600,    // Keep completed jobs for 1 hour
    count: 1000   // Keep max 1000 completed jobs
  },
  removeOnFail: false // Keep failed for debugging
}
```

### Retry Decision Matrix

| Error Type                       | Detection           | Action                    |
| -------------------------------- | ------------------- | ------------------------- |
| **Transient** (network, timeout) | 5xx, ETIMEDOUT      | Retry with backoff        |
| **Permanent** (validation, auth) | 4xx                 | Move to DLQ immediately   |
| **Resource** (rate limit)        | 429                 | Retry with longer backoff |
| **Unknown**                      | Unhandled exception | Retry (assume transient)  |

---

## 🧭 DECISION FRAMEWORKS

### Queue Architecture Decisions

- Fast priority jobs: Separate priority queue
- Delayed execution: Scheduled jobs with `delay`
- Rate limiting external API: Limiter group in BullMQ
- Strict ordering: FIFO with job grouping
- Large batch processing: Parent-child jobs (chunking)
- Multi-tenant isolation: Queue per tenant OR tenant prefix

### Concurrency Patterns

| Pattern            | Configuration                            | Use Case                   |
| ------------------ | ---------------------------------------- | -------------------------- |
| **Fixed Pool**     | `concurrency: 10`                        | Predictable load           |
| **Rate Limited**   | `limiter: { max: 100, duration: 60000 }` | External API limits        |
| **Priority Queue** | Multiple queues with different workers   | VIP customers              |
| **FIFO per Key**   | Job grouping by key                      | Order-sensitive operations |

### Dead Letter Queue (DLQ) Strategy

```
Job fails → Retry 1 → Retry 2 ... → Max retries
                                        │
                                        ▼
                               ┌────────────────┐
                               │  Dead Letter   │
                               │    Queue       │
                               │                │
                               │  • Inspect     │
                               │  • Fix issue   │
                               │  • Replay      │
                               └────────────────┘
```

**DLQ Operations:**

1. **Monitor**: Alert on DLQ growth
2. **Inspect**: View failed job payload and error
3. **Diagnose**: Identify root cause
4. **Fix**: Deploy fix for the bug
5. **Replay**: Reprocess jobs from DLQ

---

## ⚡ WORKER PATTERNS

### Idempotent Handler Pattern

```typescript
async function processJob(job: Job) {
  const { orderId, idempotencyKey } = job.data;

  // Check if already processed
  const existing = await db.findByIdempotencyKey(idempotencyKey);
  if (existing) {
    logger.info("Job already processed, skipping", { idempotencyKey });
    return existing.result; // Return cached result
  }

  // Process the job
  const result = await doActualWork(orderId);

  // Store result with idempotency key
  await db.saveWithIdempotencyKey(idempotencyKey, result);

  return result;
}
```

### Graceful Shutdown Pattern

```typescript
const worker = new Worker("my-queue", handler);

process.on("SIGTERM", async () => {
  logger.info("SIGTERM received, closing worker...");

  // Stop accepting new jobs
  await worker.close();

  // Wait for current jobs to complete (with timeout)
  await worker.waitUntilReady();

  logger.info("Worker closed gracefully");
  process.exit(0);
});
```

### Worker Pool Sizing

| Job Type              | Duration | Suggested Concurrency   |
| --------------------- | -------- | ----------------------- |
| CPU-bound             | > 1s     | 1-2 per CPU core        |
| I/O-bound (API calls) | < 1s     | 10-50                   |
| Mixed                 | Variable | 5-10 with rate limiting |

---

## ❌ ANTI-PATTERNS

### Critical Mistakes

| Anti-Pattern              | Risk                                | Correct Approach                     |
| ------------------------- | ----------------------------------- | ------------------------------------ |
| **Large payloads**        | Memory bloat, serialization issues  | Store IDs, fetch fresh in worker     |
| **No retry config**       | Transient failures become permanent | Always configure exponential backoff |
| **Ignoring DLQ**          | Failed jobs disappear silently      | Monitor and alert on DLQ             |
| **No idempotency**        | Duplicate processing corrupts data  | Use idempotency key pattern          |
| **Unbounded concurrency** | Resource exhaustion                 | Set appropriate limits               |
| **Fire and forget**       | No visibility into failures         | Track completion, handle failures    |
| **Single queue for all**  | Priority jobs blocked by bulk       | Separate queues by type/priority     |
| **Swallowing errors**     | Silent failures                     | Throw errors, let queue handle retry |

### Code Smells

```typescript
// ❌ SMELL: Catching and ignoring errors
try {
  await processJob(job);
} catch (error) {
  console.log("Job failed, continuing..."); // NEVER
}

// ✅ CORRECT: Let queue handle retry
async function processJob(job: Job) {
  // Just do the work - errors bubble up to queue
  await doWork(job.data);
  // Queue will retry on failure
}

// ❌ SMELL: No timeout
const result = await externalApi.call(data); // Could hang forever

// ✅ CORRECT: Always timeout
const result = await Promise.race([
  externalApi.call(data),
  timeout(30000, new Error("External API timeout")),
]);
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Job Definition

- [ ] Payload contains only IDs (not full objects)
- [ ] Idempotency key included
- [ ] Tenant context included (multi-tenant)
- [ ] Correlation ID for tracing
- [ ] Appropriate timeout configured

### Retry Configuration

- [ ] Exponential backoff enabled
- [ ] Max attempts set (typically 3-5)
- [ ] Remove on complete configured (with limits)
- [ ] Remove on fail = false (keep for debugging)
- [ ] DLQ handling defined

### Worker Implementation

- [ ] Handler is idempotent
- [ ] Graceful shutdown implemented
- [ ] Concurrency limits set
- [ ] Error handling lets errors bubble up
- [ ] Logging includes job ID and correlation ID

### Monitoring

- [ ] Queue depth metric exposed
- [ ] Processing time metric exposed
- [ ] DLQ size alerting configured
- [ ] Failed job rate alerting
- [ ] Worker health checks

---

## 📚 References

- [BullMQ Documentation](https://docs.bullmq.io/)
- [RabbitMQ Best Practices](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)
- [Idempotency Patterns](https://blog.bytebytego.com/p/idempotency-patterns)
- [Dead Letter Queue Design](https://aws.amazon.com/blogs/compute/implementing-dead-letter-queues-for-amazon-sqs/)

---

> **Remember:** Queues are the backbone of async systems. A dropped job is a broken promise. Design for failure: every job should either complete, explicitly fail to DLQ, or be retried. No job should silently disappear.
