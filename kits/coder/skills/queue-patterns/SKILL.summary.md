---
name: queue-patterns
summary: true
description: "Message queue and background job patterns. For planning/quick ref — load SKILL.md for BullMQ/RabbitMQ code."
---

# Queue Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when implementing queue workers or retry logic.

## Technology Selection
- **Node.js + Redis** → BullMQ
- **Python** → Celery / ARQ
- **Serverless** → AWS SQS
- **Multi-language routing** → RabbitMQ
- **High-throughput streaming** → Kafka

## Non-Negotiable Rules
- **Payload = IDs only**, fetch fresh data in worker (never large objects)
- **idempotencyKey** in every job — same job 2x = same result
- **tenantId** in every job (multi-tenant)
- **correlationId** for request tracing
- **Retry**: exponential backoff · max 3-5 attempts · DLQ after max retries
- **DLQ monitored**: alert on DLQ growth, never let jobs silently disappear
- **Errors bubble up**: never swallow errors in worker → let queue retry

## Job States
`WAITING → ACTIVE → COMPLETED | FAILED → RETRY → DLQ`

## Error Classification
- Transient (network, timeout) → retry with backoff
- Permanent (validation, auth) → move to DLQ immediately
- Rate limit (429) → retry with longer delay

## Anti-Patterns
- Catching & ignoring errors in worker
- No timeout on external API calls
- Single queue for all job types (use priority queues)
- No idempotency check → duplicate processing

> Load full SKILL.md for: BullMQ config code, idempotent handler pattern, graceful shutdown, concurrency patterns, implementation checklist
