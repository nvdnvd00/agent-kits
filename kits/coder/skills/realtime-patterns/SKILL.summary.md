---
name: realtime-patterns
summary: true
description: "WebSocket, Socket.IO, event-driven patterns. For planning/quick ref — load SKILL.md for full patterns."
---

# Realtime Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when implementing connection/scaling/event code.

## Technology Selection
- **2-way + browser compat** → Socket.IO
- **2-way, no fallback needed** → Raw WebSocket
- **Server→Client only** → Server-Sent Events
- **Server-to-server** → Webhooks

## Key Rules
- **Reconnection**: Exponential backoff (1s→2s→4s, max 30s) + jitter always
- **Auth**: JWT in handshake `auth` object (not cookie) · validate on every connection
- **Rooms**: `socket.join(roomId)` · naming: `entity:id` (e.g., `conversation:456`)
- **Scaling**: Redis adapter for multi-instance · sticky sessions OR pub/sub
- **Events**: `resource:action` naming · include `requestId` + `eventId` in payload
- **State sync**: Send missed events on reconnect via sequence numbers

## Anti-Patterns
- Sending large objects over socket (send IDs, fetch via HTTP)
- In-memory state per server (use Redis for cross-server)
- No reconnection handling / immediate reconnect (use backoff)
- Missing payload validation

> Load full SKILL.md for: connection lifecycle code, Redis adapter setup, security patterns, implementation checklist
