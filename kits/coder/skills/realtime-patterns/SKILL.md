---
name: realtime-patterns
description: WebSocket, Socket.IO, and event-driven architecture patterns. Use when building real-time features like chat, notifications, live updates, or collaborative editing. Covers connection management, rooms, scaling, and event design.
allowed-tools: Read, Write, Edit, Bash
---

# Realtime Patterns - Event-Driven Communication Architecture

> **Philosophy:** Real-time isn't just fast—it's instantaneous perceived response. Design for resilience, not just speed.

---

## 🎯 Core Principle: Reliable Real-Time

```
❌ WRONG: Open WebSocket → Send data → Hope it arrives
✅ CORRECT: Open WebSocket → Handle disconnects → Retry → Confirm delivery → Graceful degradation
```

**The Realtime Approach:**

- Connections will fail—plan for reconnection
- Order and delivery matter—design for reliability
- Scale horizontally—don't rely on single server
- Events are the contract—define them clearly

---

## 🔀 Technology Selection

### When to Use What

| Technology             | Best For                           | Trade-offs                     |
| ---------------------- | ---------------------------------- | ------------------------------ |
| **WebSocket**          | Two-way, low-latency communication | Manual reconnection handling   |
| **Socket.IO**          | Browser-friendly with fallbacks    | Slight overhead, easier to use |
| **Server-Sent Events** | Server → Client only (one-way)     | Simpler, no full-duplex        |
| **HTTP Polling**       | Legacy support, simple needs       | Higher latency, more resources |
| **HTTP Long Polling**  | Fallback when others unavailable   | Resource intensive             |
| **Webhooks**           | Server-to-server events            | Requires public endpoint       |

### Decision Tree

```
Need two-way communication?
├─ Yes → Need browser fallbacks?
│        ├─ Yes → Socket.IO
│        └─ No → Raw WebSocket
└─ No → Server → Client only?
         ├─ Yes → Server-Sent Events (SSE)
         └─ No → HTTP Polling / Webhooks
```

---

## 🔌 Connection Management

### Connection Lifecycle

```
CONNECTING → CONNECTED → ACTIVE
    ↑            │           │
    │            ↓           ↓
    └── DISCONNECTED ← RECONNECTING
                ↓
            CLOSED (user action / max retries)
```

### Client-Side Connection State

```typescript
interface ConnectionState {
  status:
    | "connecting"
    | "connected"
    | "reconnecting"
    | "disconnected"
    | "closed";
  lastConnected: Date | null;
  reconnectAttempts: number;
  latency: number | null;
}
```

### Keep-Alive (Heartbeat)

| Aspect           | Recommendation                            |
| ---------------- | ----------------------------------------- |
| **Interval**     | 25-30 seconds (under typical 60s timeout) |
| **Pong Timeout** | 5-10 seconds after ping sent              |
| **On Timeout**   | Trigger reconnection                      |
| **Payload**      | Minimal (empty or timestamp only)         |

```typescript
// Heartbeat pattern
const HEARTBEAT_INTERVAL = 25000;
const PONG_TIMEOUT = 5000;

setInterval(() => {
  socket.emit("ping");

  const timeout = setTimeout(() => {
    console.log("Connection dead, reconnecting...");
    socket.disconnect();
    socket.connect();
  }, PONG_TIMEOUT);

  socket.once("pong", () => clearTimeout(timeout));
}, HEARTBEAT_INTERVAL);
```

---

## 🔄 Reconnection Strategies

### Exponential Backoff with Jitter

```
Attempt 1: Wait 1s
Attempt 2: Wait 2s (+ random 0-500ms)
Attempt 3: Wait 4s (+ random 0-500ms)
Attempt 4: Wait 8s (+ random 0-500ms)
Attempt 5: Wait 16s (+ random 0-500ms)
... capped at 30s max
```

### Reconnection Configuration

| Parameter          | Recommended Value | Purpose                      |
| ------------------ | ----------------- | ---------------------------- |
| **Initial Delay**  | 1000ms            | First retry wait             |
| **Max Delay**      | 30000ms           | Cap on retry wait time       |
| **Max Retries**    | 10-15             | Before showing error to user |
| **Backoff Factor** | 2                 | Multiplier for each attempt  |
| **Jitter**         | 0-500ms random    | Prevent thundering herd      |

### Post-Reconnection Sync

```typescript
socket.on("connect", () => {
  if (wasReconnection) {
    // Re-subscribe to rooms/topics
    socket.emit("rejoin-rooms", { rooms: currentRooms });

    // Request missed events since lastEventId
    socket.emit("sync-events", { since: lastEventId });

    // Or fetch current state via HTTP and apply
    await fetchAndSyncState();
  }
});
```

---

## 🏠 Rooms & Namespaces (Socket.IO)

### Rooms vs Namespaces

| Feature         | Rooms                       | Namespaces                  |
| --------------- | --------------------------- | --------------------------- |
| **Purpose**     | Dynamic grouping of sockets | Logical endpoint separation |
| **Created**     | Dynamically at runtime      | Defined in code             |
| **Client Join** | Server-side only            | Client connects directly    |
| **Use Case**    | Chat rooms, user groups     | Different app modules       |

### Room Patterns

```typescript
// Join room server-side
socket.join(`user:${userId}`);
socket.join(`conversation:${conversationId}`);
socket.join(`tenant:${tenantId}:agents`);

// Emit to room
io.to(`conversation:${conversationId}`).emit("message:new", messageData);

// Leave room
socket.leave(`conversation:${conversationId}`);

// Room naming convention
// Format: entity:id or entity:id:subgroup
// Examples:
//   user:123
//   conversation:456
//   team:789:admins
//   tenant:abc:online-agents
```

### Namespace Patterns

```typescript
// Define namespaces for different features
const chatNsp = io.of("/chat");
const notificationNsp = io.of("/notifications");
const adminNsp = io.of("/admin");

// Each namespace has its own middleware
adminNsp.use(requireAdminAuth);

// Client connects to specific namespace
const adminSocket = io("/admin");
```

---

## 📨 Event Design

### Event Naming Convention

| Pattern                  | Example                | Use Case               |
| ------------------------ | ---------------------- | ---------------------- |
| `resource:action`        | `message:send`         | Client → Server action |
| `resource:action:result` | `message:send:success` | Server response        |
| `resource:event`         | `message:received`     | Server → Client event  |
| `error:resource`         | `error:message`        | Error events           |

### Event Payload Structure

```typescript
// Request (client → server)
interface SocketRequest<T> {
  requestId: string; // For correlation
  timestamp: number; // Unix ms
  payload: T;
}

// Response (server → client)
interface SocketResponse<T> {
  requestId: string; // Correlation with request
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}

// Event (server → client, broadcast)
interface SocketEvent<T> {
  eventId: string; // For deduplication
  timestamp: number;
  type: string; // Event type
  payload: T;
}
```

### Event Acknowledgment

```typescript
// Client sends with callback
socket.emit("message:send", payload, (response) => {
  if (response.success) {
    // Handle success
  } else {
    // Handle error
  }
});

// Server responds via callback
socket.on("message:send", async (payload, callback) => {
  try {
    const result = await processMessage(payload);
    callback({ success: true, data: result });
  } catch (error) {
    callback({
      success: false,
      error: { code: "SEND_FAILED", message: error.message },
    });
  }
});
```

---

## ⚖️ Scaling Patterns

### Horizontal Scaling Architecture

```
                   ┌─────────────────┐
                   │  Load Balancer  │
                   │ (Sticky Session)│
                   └────────┬────────┘
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │Socket.IO │      │Socket.IO │      │Socket.IO │
    │Server 1  │      │Server 2  │      │Server 3  │
    └────┬─────┘      └────┬─────┘      └────┬─────┘
         │                 │                 │
         └────────────┬────┴────┬────────────┘
                      ↓         ↓
                ┌─────────────────────┐
                │   Redis (Pub/Sub)   │
                │   Adapter Layer     │
                └─────────────────────┘
```

### Redis Adapter Setup

```typescript
import { createAdapter } from "@socket.io/redis-adapter";
import { createClient } from "redis";

const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));
```

### Scaling Considerations

| Challenge             | Solution                                  |
| --------------------- | ----------------------------------------- |
| **Sticky Sessions**   | Use consistent hashing or client IP-based |
| **Cross-Server Emit** | Redis Pub/Sub adapter                     |
| **Connection State**  | Store in Redis, not in-memory             |
| **N-Squared Problem** | Sharded Redis adapter (Redis 7.0+)        |
| **Message Order**     | Use sequence numbers or timestamps        |

---

## 🔒 Security

### Authentication Patterns

```typescript
// Token in query string (connection time)
const socket = io({
  auth: {
    token: accessToken,
  },
});

// Server middleware validates
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token;
    const user = await verifyToken(token);
    socket.data.user = user;
    next();
  } catch (error) {
    next(new Error("unauthorized"));
  }
});
```

### Security Checklist

| Concern                | Mitigation                              |
| ---------------------- | --------------------------------------- |
| **Authentication**     | Validate token before accepting socket  |
| **Authorization**      | Check permissions before joining rooms  |
| **Rate Limiting**      | Limit events per second per client      |
| **Payload Validation** | Validate and sanitize all incoming data |
| **Message Size**       | Limit max payload size                  |
| **Origin Check**       | Configure CORS properly                 |

---

## 🛡️ Error Handling

### Error Categories

| Category             | Example                  | Client Action               |
| -------------------- | ------------------------ | --------------------------- |
| **Connection Error** | Network failure          | Reconnect with backoff      |
| **Authentication**   | Token expired            | Refresh token, reconnect    |
| **Authorization**    | Not allowed to join room | Show error, don't retry     |
| **Validation**       | Invalid payload          | Show error, fix input       |
| **Server Error**     | Internal server error    | Retry once, then show error |

### Error Event Structure

```typescript
socket.on("error", (error) => {
  switch (error.code) {
    case "TOKEN_EXPIRED":
      await refreshTokenAndReconnect();
      break;
    case "RATE_LIMITED":
      showNotification("Slow down!");
      break;
    case "ROOM_NOT_FOUND":
      navigateToLobby();
      break;
    default:
      console.error("Socket error:", error);
  }
});
```

---

## 📊 Monitoring & Debugging

### Key Metrics

| Metric                 | What It Tells You             |
| ---------------------- | ----------------------------- |
| **Active Connections** | Current load, scaling needs   |
| **Connection Rate**    | Traffic patterns, spikes      |
| **Reconnection Rate**  | Connection stability issues   |
| **Message Latency**    | System responsiveness         |
| **Messages/Second**    | Throughput, capacity planning |
| **Error Rate**         | System health                 |

### Debugging Tips

```typescript
// Enable debug logs (development only)
localStorage.debug = "socket.io-client:socket";

// Log all events
socket.onAny((eventName, ...args) => {
  console.log(`[Socket] ${eventName}`, args);
});

// Track connection state
socket.io.on("reconnect_attempt", (attempt) => {
  console.log(`Reconnect attempt ${attempt}`);
});

socket.io.on("reconnect_error", (error) => {
  console.error("Reconnect failed:", error);
});
```

---

## 🚨 Anti-Patterns

| ❌ Don't                            | ✅ Do                               |
| ----------------------------------- | ----------------------------------- |
| Send large objects over socket      | Send IDs, fetch data via HTTP       |
| Block in event handlers             | Process async, return quickly       |
| Trust client-sent room names        | Validate and authorize room access  |
| Reconnect immediately on failure    | Use exponential backoff with jitter |
| Store state in single server memory | Use Redis for cross-server state    |
| Ignore connection state             | Track and display to user           |
| Send sensitive data in events       | Encrypt or use HTTPS/WSS only       |
| Process without validation          | Validate all incoming payloads      |

---

## 📋 Implementation Checklist

### Before Going Live

```markdown
## Realtime Feature Checklist

### Connection Management

- [ ] Reconnection with exponential backoff
- [ ] Heartbeat/keep-alive implemented
- [ ] Connection state displayed to user
- [ ] Graceful disconnect handling

### Event Design

- [ ] Events follow naming convention
- [ ] Payloads have requestId/eventId
- [ ] Acknowledgments for critical actions
- [ ] Error events defined and handled

### Scaling

- [ ] Redis adapter configured
- [ ] Sticky sessions in load balancer
- [ ] State stored in Redis (not memory)
- [ ] Room-based broadcasting optimized

### Security

- [ ] Authentication on connection
- [ ] Authorization on room join
- [ ] Rate limiting implemented
- [ ] Payload validation
- [ ] CORS properly configured

### Reliability

- [ ] Missed message sync strategy
- [ ] Deduplication by eventId
- [ ] Fallback to HTTP if needed
- [ ] Graceful degradation
```

---

## 🔗 Related Skills

| Need                      | Skill                   |
| ------------------------- | ----------------------- |
| API design for HTTP calls | `api-patterns`          |
| Performance optimization  | `performance-profiling` |
| Queue/worker patterns     | `queue-patterns`        |
| Database for state        | `database-design`       |

---

> **Remember:** Real-time systems are about perceived responsiveness. A well-handled reconnection is better than a dropped message the user never sees.
