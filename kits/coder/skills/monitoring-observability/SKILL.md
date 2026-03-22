---
name: monitoring-observability
description: Production monitoring, observability, and SRE patterns. Use when designing monitoring systems, implementing SLI/SLO, configuring alerting, or building observability infrastructure with Prometheus, Grafana, and modern tools.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# Monitoring & Observability - SRE Patterns

## ⚡ Quick Reference

- **3 pillars**: Metrics (trends) · Logs (events) · Traces (distributed request flow)
- **Alert tiers**: Critical (< 5min) · High (< 15min) · Medium (< 1hr) · Low (next day)
- **SLOs**: Define before shipping · P99 latency · Error rate · Availability goals
- **Logs**: Structured JSON always · Include request ID + tenant ID · No PII in logs
- **Health checks**: /health (liveness) + /ready (readiness) · Check DB/Redis/deps
- **Avoid**: Alert fatigue (too many low-value alerts) · Log PII · Monitor without alerting

---


---

## When to Use This Skill

| ✅ Use                           | ❌ Don't Use                    |
| -------------------------------- | ------------------------------- |
| Designing monitoring systems     | Single ad-hoc dashboard         |
| Defining SLI/SLO/SLA             | Application feature development |
| Configuring alerting strategy    | Local development debugging     |
| Building observability pipelines | No access to telemetry data     |
| Incident response workflow       | Static reporting only           |

---

## Core Rules (Non-Negotiable)

1. **Four Golden Signals** - Latency, Traffic, Errors, Saturation
2. **SLO-based alerting** - Alert on symptoms, not causes
3. **No secrets in logs** - Redact sensitive data
4. **Structured logging** - JSON, not unstructured text
5. **Correlation required** - Link metrics, logs, traces

---

## Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────────┐
│                     OBSERVABILITY                            │
├─────────────────┬─────────────────┬─────────────────────────┤
│     METRICS     │      LOGS       │        TRACES           │
│                 │                 │                         │
│  • Aggregated   │  • Discrete     │  • Request-scoped       │
│  • Time-series  │  • Event-based  │  • Distributed          │
│  • Low overhead │  • High detail  │  • Causality chain      │
│                 │                 │                         │
│  Prometheus     │  Loki/ELK       │  Jaeger/Zipkin          │
│  Victoria       │  Splunk         │  X-Ray                  │
│  DataDog        │  CloudWatch     │  OpenTelemetry          │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## Four Golden Signals

| Signal         | What to Measure            | Example Metrics                     |
| -------------- | -------------------------- | ----------------------------------- |
| **Latency**    | Time to serve a request    | `http_request_duration_seconds`     |
| **Traffic**    | Demand on your system      | `http_requests_total`               |
| **Errors**     | Rate of failed requests    | `http_requests_total{status="5xx"}` |
| **Saturation** | Fullness of your resources | `container_memory_usage_bytes`      |

### RED Method (Request-focused)

- **Rate** - Requests per second
- **Errors** - Failed requests per second
- **Duration** - Time per request

### USE Method (Resource-focused)

- **Utilization** - % time resource is busy
- **Saturation** - Queue length / pending work
- **Errors** - Error events count

---

## SLI/SLO/SLA Framework

### Definitions

| Term    | Definition                            | Example                              |
| ------- | ------------------------------------- | ------------------------------------ |
| **SLI** | Measurable indicator of service level | 99th percentile latency < 200ms      |
| **SLO** | Target value for an SLI               | 99% of requests < 200ms over 30 days |
| **SLA** | Contractual commitment with penalties | 99.9% availability or refund         |

### Error Budget

```python
# Error budget calculation
slo = 0.999  # 99.9%
window_days = 30
total_minutes = window_days * 24 * 60

error_budget_minutes = total_minutes * (1 - slo)
# 43.2 minutes of allowed downtime per month
```

### Burn Rate Alerting

```yaml
# Fast burn: 2% budget in 1 hour
- alert: HighErrorRate
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h])) 
      / 
      sum(rate(http_requests_total[1h]))
    ) > 0.001 * 14.4  # 14.4x burn rate
  for: 2m
  labels:
    severity: critical
```

---

## Prometheus Patterns

### Essential Metrics

```yaml
# Counter: Only goes up
http_requests_total{method="GET", status="200"}

# Gauge: Can go up or down
current_connections
memory_usage_bytes

# Histogram: Buckets for distribution
http_request_duration_seconds_bucket{le="0.1"}
http_request_duration_seconds_bucket{le="0.5"}
http_request_duration_seconds_bucket{le="1"}

# Summary: Pre-calculated quantiles
http_request_duration_seconds{quantile="0.99"}
```

### PromQL Patterns

```promql
# Rate of change (per-second)
rate(http_requests_total[5m])

# Increase over time window
increase(http_requests_total[1h])

# 99th percentile from histogram
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
100 * (
  rate(http_requests_total{status=~"5.."}[5m])
  /
  rate(http_requests_total[5m])
)

# Top 5 by label
topk(5, sum by (endpoint) (rate(http_requests_total[5m])))

# Aggregation across instances
sum without(instance) (rate(http_requests_total[5m]))

# Prediction (linear regression)
predict_linear(disk_free_bytes[1h], 3600 * 4)
```

### Recording Rules

```yaml
groups:
  - name: sli_recording_rules
    rules:
      - record: job:http_request_latency_seconds:p99
        expr: histogram_quantile(0.99, sum by (job, le) (rate(http_request_duration_seconds_bucket[5m])))

      - record: job:http_error_rate:ratio
        expr: |
          sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum by (job) (rate(http_requests_total[5m]))
```

---

## Alerting Strategy

### Alert Priority Levels

| Level        | Response Time | Channel          | Example                     |
| ------------ | ------------- | ---------------- | --------------------------- |
| **Critical** | Immediate     | PagerDuty + Call | Service down, data loss     |
| **Warning**  | 15-30 min     | Slack            | High latency, disk 80%      |
| **Info**     | Next business | Email/Ticket     | Certificate expiring in 30d |

### Alerting Best Practices

```yaml
groups:
  - name: slo_alerts
    rules:
      # ✅ Good: Alert on symptoms (SLO breach)
      - alert: HighLatencySLOBreach
        expr: |
          job:http_request_latency_seconds:p99 > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency exceeds 500ms SLO"
          runbook_url: "https://wiki/runbooks/high-latency"

      # ❌ Bad: Alert on cause (CPU high)
      # - alert: HighCPU
      #   expr: node_cpu_usage > 80
      #   # CPU can be high without user impact
```

### Reducing Alert Noise

| Problem          | Solution                             |
| ---------------- | ------------------------------------ |
| Flapping alerts  | Increase `for` duration              |
| Too many alerts  | Alert on SLOs, not individual causes |
| Duplicate alerts | Use `group_by` and aggregation       |
| Weekend pages    | Time-based routing, error budgets    |
| Alert storms     | Implement alerting hierarchy         |

---

## Structured Logging

### Log Levels

| Level     | Use Case                              | Example                       |
| --------- | ------------------------------------- | ----------------------------- |
| **ERROR** | Unhandled failures requiring action   | Database connection failed    |
| **WARN**  | Concerning but handled situations     | Retry succeeded on attempt 3  |
| **INFO**  | Business-significant events           | User registered, order placed |
| **DEBUG** | Technical details for troubleshooting | Query executed in 50ms        |

### Structured Log Format

```typescript
const log = {
  timestamp: "2024-01-15T10:30:00Z",
  level: "INFO",
  service: "order-service",
  traceId: "abc123",
  spanId: "def456",
  userId: "user_789",
  event: "order.created",
  orderId: "order_123",
  total: 99.99,
  items: 3,
  latencyMs: 45,
};
```

### Log Correlation Pattern

```typescript
// Propagate trace context through all logs
app.use((req, res, next) => {
  req.logger = logger.child({
    traceId: req.headers["x-trace-id"] || uuid(),
    spanId: uuid(),
    requestId: req.id,
    userId: req.user?.id,
  });
  next();
});
```

---

## Distributed Tracing

### OpenTelemetry Setup

```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { JaegerExporter } from "@opentelemetry/exporter-jaeger";
import { Resource } from "@opentelemetry/resources";

const sdk = new NodeSDK({
  resource: new Resource({
    "service.name": "order-service",
    "service.version": "1.0.0",
  }),
  traceExporter: new JaegerExporter({
    endpoint: "http://jaeger:14268/api/traces",
  }),
});

sdk.start();
```

### Span Attributes

```typescript
import { trace } from "@opentelemetry/api";

const tracer = trace.getTracer("order-service");

async function processOrder(orderId: string) {
  return tracer.startActiveSpan("processOrder", async (span) => {
    span.setAttribute("order.id", orderId);
    span.setAttribute("order.total", 99.99);

    try {
      // ... business logic
      span.setStatus({ code: SpanStatusCode.OK });
    } catch (error) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error.message,
      });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

---

## Grafana Dashboard Patterns

### Dashboard Structure

```
├── Overview (Business KPIs)
│   ├── Revenue / Orders
│   ├── Active Users
│   └── Error Rate Summary
│
├── Service Health (Per Service)
│   ├── Four Golden Signals
│   ├── SLI/SLO Status
│   └── Resource Utilization
│
├── Infrastructure
│   ├── Node Metrics
│   ├── Container Stats
│   └── Database Performance
│
└── Debugging
    ├── Trace Explorer
    ├── Log Viewer
    └── Error Breakdown
```

### Variable Templates

```yaml
# Environment selector
- name: environment
  type: query
  query: label_values(up, environment)

# Service filter
- name: service
  type: query
  query: label_values(http_requests_total{environment="$environment"}, service)
```

---

## Incident Response Workflow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Detect    │───▷│   Triage    │───▷│   Mitigate  │
│   Alert     │    │   Severity  │    │   Rollback  │
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                                            ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Review    │◁───│   Resolve   │◁───│  Communicate│
│  Postmortem │    │   Fix       │    │   Status    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Runbook Template

```markdown
# Alert: [Alert Name]

## Impact

- What services are affected?
- What is the user impact?

## Quick Diagnosis

1. Check dashboard: [link]
2. Check recent deployments: [link]
3. Check upstream dependencies

## Mitigation Steps

1. If caused by deployment → Rollback
2. If caused by traffic → Scale up / rate limit
3. If caused by dependency → Failover

## Escalation

- On-call: @team-oncall
- Escalation: @team-lead
```

---

## Anti-Patterns

| ❌ Don't                        | ✅ Do                               |
| ------------------------------- | ----------------------------------- |
| Alert on causes (CPU, memory)   | Alert on symptoms (latency, errors) |
| Log everything at INFO          | Use appropriate log levels          |
| Unstructured log messages       | JSON structured logging             |
| Alert without runbook           | Every alert has a runbook           |
| Collect metrics without purpose | Define SLIs first, then instrument  |
| Secret values in logs           | Redact sensitive data               |
| High-cardinality labels         | Bounded label values                |

---

## Production Checklist

Before production:

- [ ] Four Golden Signals instrumented?
- [ ] SLIs/SLOs defined per service?
- [ ] Error budget tracking enabled?
- [ ] Structured logging implemented?
- [ ] Trace context propagating?
- [ ] Alerting hierarchy defined?
- [ ] Runbooks for all critical alerts?
- [ ] On-call rotation configured?

---

## Related Skills

| Need                | Skill                   |
| ------------------- | ----------------------- |
| Kubernetes ops      | `kubernetes-patterns`   |
| CI/CD pipelines     | `github-actions`        |
| Performance tuning  | `performance-profiling` |
| Security monitoring | `security-fundamentals` |

---

> **Remember:** Good observability lets you answer questions you haven't thought of yet. Build for unknown-unknowns, not just known issues.
