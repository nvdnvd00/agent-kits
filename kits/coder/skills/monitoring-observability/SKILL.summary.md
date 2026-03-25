---
name: monitoring-observability
summary: true
description: "SRE monitoring, observability, SLI/SLO patterns. For planning/quick ref — load SKILL.md for Prometheus/Grafana/alerting code."
---

# Monitoring & Observability — Summary

> ⚡ Quick ref. Load full `SKILL.md` when setting up Prometheus, Grafana, or alerting rules.

## 3 Pillars
- **Metrics** (Prometheus): aggregated time-series, trends → Prometheus/VictoriaMetrics/DataDog
- **Logs** (Loki/ELK): discrete events, high detail → structured JSON always
- **Traces** (Jaeger/OTel): distributed request causality chains

## Four Golden Signals (Always Instrument)
1. **Latency** — time to serve request (`http_request_duration_seconds`)
2. **Traffic** — demand (`http_requests_total`)
3. **Errors** — failure rate (`http_requests_total{status=~"5.."}`)
4. **Saturation** — resource fullness (memory/CPU/queue depth)

## SLO Framework
- Define SLI → Set SLO target → Calculate error budget → Alert on burn rate (not causes)
- Alert on **symptoms** (latency/errors breach SLO), NOT causes (CPU high)

## Non-Negotiable Rules
- Structured JSON logging always (no unstructured text)
- NO PII/secrets in logs — redact sensitive fields
- `traceId` + `requestId` in every log entry
- Every alert must have a runbook URL
- /health (liveness) + /ready (readiness) endpoints on every service

## Alert Tiers
- Critical → PagerDuty + call (service down, data loss)
- Warning → Slack 15-30min (latency, disk 80%)
- Info → email/ticket (cert expiring 30d)

> Load full SKILL.md for: PromQL patterns, burn rate alerting, OpenTelemetry setup, Grafana dashboard templates, incident response workflow
