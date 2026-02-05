---
name: api-patterns
description: API design principles and decision-making. Use when designing APIs, choosing between REST/GraphQL/tRPC, or implementing versioning, pagination, error handling. Covers response formats, authentication patterns, and rate limiting.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# API Patterns - Design Principles & Decision Making

> **Philosophy:** Choose the right API style for the context. Learn to THINK, not copy fixed patterns.

---

## API Style Decision Tree

```
What are your requirements?
│
├─ Public API + Multiple clients?
│  └─ → REST (broad compatibility, caching)
│
├─ Complex UI + Variable data needs?
│  └─ → GraphQL (client-driven queries)
│
├─ TypeScript monorepo + Internal API?
│  └─ → tRPC (end-to-end type safety)
│
├─ Real-time updates needed?
│  └─ → WebSocket + REST/GraphQL
│
└─ Simple CRUD + Standard patterns?
   └─ → REST (simplest, well-understood)
```

---

## REST Best Practices

### Resource Naming

| ✅ Do               | ❌ Don't           |
| ------------------- | ------------------ |
| `GET /users`        | `GET /getUsers`    |
| `GET /users/:id`    | `GET /user?id=123` |
| `POST /users`       | `POST /createUser` |
| `DELETE /users/:id` | `POST /deleteUser` |
| `/users/:id/orders` | `/getUserOrders`   |

### HTTP Methods

| Method   | Purpose          | Idempotent |
| -------- | ---------------- | ---------- |
| `GET`    | Read resource    | ✅ Yes     |
| `POST`   | Create resource  | ❌ No      |
| `PUT`    | Replace resource | ✅ Yes     |
| `PATCH`  | Partial update   | ❌ No      |
| `DELETE` | Remove resource  | ✅ Yes     |

### HTTP Status Codes

| Code  | Meaning           | Use Case                 |
| ----- | ----------------- | ------------------------ |
| `200` | OK                | Successful GET/PUT/PATCH |
| `201` | Created           | Successful POST          |
| `204` | No Content        | Successful DELETE        |
| `400` | Bad Request       | Invalid input            |
| `401` | Unauthorized      | Missing/invalid auth     |
| `403` | Forbidden         | No permission            |
| `404` | Not Found         | Resource doesn't exist   |
| `409` | Conflict          | Duplicate/state conflict |
| `422` | Unprocessable     | Validation failed        |
| `429` | Too Many Requests | Rate limited             |
| `500` | Server Error      | Internal error           |

---

## Response Format

### Standard Success Response

```json
{
  "data": {},
  "meta": {
    "requestId": "abc-123",
    "timestamp": 1707100000
  }
}
```

### Standard Error Response

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 was not found",
    "details": {
      "userId": "123"
    }
  },
  "meta": {
    "requestId": "abc-123",
    "timestamp": 1707100000
  }
}
```

### Error Code Naming

| Pattern                   | Example                             |
| ------------------------- | ----------------------------------- |
| `RESOURCE_NOT_FOUND`      | `USER_NOT_FOUND`, `ORDER_NOT_FOUND` |
| `RESOURCE_ALREADY_EXISTS` | `EMAIL_ALREADY_EXISTS`              |
| `INVALID_FIELD`           | `INVALID_EMAIL`, `INVALID_PHONE`    |
| `PERMISSION_DENIED`       | `PERMISSION_DENIED`                 |
| `RATE_LIMITED`            | `RATE_LIMITED`                      |

---

## Pagination Patterns

### Offset-Based (Simple)

```
GET /users?page=2&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**Pros:** Simple, supports random access
**Cons:** Performance issues with large offsets, unstable with mutations

### Cursor-Based (Recommended for Large Datasets)

```
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTIwfQ",
    "prevCursor": "eyJpZCI6ODB9",
    "hasMore": true
  }
}
```

**Pros:** Stable ordering, efficient for large datasets
**Cons:** No random access, more complex

### Decision Matrix

| Use Case                  | Strategy |
| ------------------------- | -------- |
| Small dataset (<1000)     | Offset   |
| Large dataset (>10000)    | Cursor   |
| Frequently changing data  | Cursor   |
| Random page access needed | Offset   |
| Infinite scroll UI        | Cursor   |
| Table with page numbers   | Offset   |

---

## API Versioning

### Strategies

| Strategy        | Example          | Pros             | Cons                |
| --------------- | ---------------- | ---------------- | ------------------- |
| **URI Path**    | `/v1/users`      | Clear, cacheable | URL pollution       |
| **Header**      | `Api-Version: 1` | Clean URLs       | Hidden from clients |
| **Query Param** | `?version=1`     | Easy to test     | Not RESTful         |

**Recommendation:** Use URI path versioning for clarity.

### Version Lifecycle

```
v1 (current)    → Active, fully supported
v2 (beta)       → In development, may change
v1 (deprecated) → Still works, sunset warning
v1 (retired)    → Returns 410 Gone
```

---

## Authentication Patterns

| Pattern       | Use Case         | Notes                        |
| ------------- | ---------------- | ---------------------------- |
| **JWT**       | Stateless APIs   | Short expiry, refresh tokens |
| **OAuth 2.0** | Third-party auth | Authorization Code flow      |
| **API Key**   | Server-to-server | Rate limit per key           |
| **Session**   | Traditional web  | Requires sticky sessions     |

### JWT Best Practices

- Access token: 15 min expiry
- Refresh token: 7 days expiry
- Store refresh token securely (httpOnly cookie)
- Include minimal claims (user ID, roles)
- Validate signature on every request

---

## Rate Limiting

### Strategies

| Strategy           | Description                           |
| ------------------ | ------------------------------------- |
| **Token Bucket**   | Allows bursts, refills over time      |
| **Sliding Window** | Smooth rate control                   |
| **Fixed Window**   | Simple but allows burst at boundaries |

### Response Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1707105600
Retry-After: 60
```

### Handling 429

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Try again in 60 seconds.",
    "retryAfter": 60
  }
}
```

---

## GraphQL vs REST

| Aspect             | REST                     | GraphQL                    |
| ------------------ | ------------------------ | -------------------------- |
| **Data fetching**  | Multiple endpoints       | Single endpoint            |
| **Over-fetching**  | Common                   | Avoided                    |
| **Under-fetching** | Multiple requests        | Single query               |
| **Caching**        | HTTP caching             | Complex                    |
| **Learning curve** | Low                      | Medium                     |
| **Best for**       | Simple CRUD, public APIs | Complex UIs, variable data |

---

## tRPC Best Practices

When using tRPC (TypeScript-first):

1. **Monorepo structure** - Share types between client/server
2. **Procedure organization** - Group by feature, not CRUD
3. **Input validation** - Use Zod for runtime validation
4. **Error handling** - Use TRPCError for typed errors
5. **Context** - Inject auth/db/etc via context

---

## Anti-Patterns

| ❌ Don't                     | ✅ Do                         |
| ---------------------------- | ----------------------------- |
| Use verbs in REST endpoints  | Use nouns + HTTP methods      |
| Return 200 for errors        | Use appropriate status codes  |
| Expose stack traces          | Return structured error codes |
| Skip rate limiting           | Implement from day 1          |
| Inconsistent response format | Define envelope pattern       |
| Version in request body      | Version in URL path           |
| Return all fields always     | Support field selection       |

---

## API Design Checklist

Before implementing:

- [ ] Identified API consumers (web, mobile, third-party)?
- [ ] Chosen API style (REST/GraphQL/tRPC)?
- [ ] Defined consistent response format?
- [ ] Planned versioning strategy?
- [ ] Designed authentication approach?
- [ ] Implemented rate limiting?
- [ ] Created OpenAPI documentation?
- [ ] Added proper error codes?
- [ ] Implemented pagination for lists?

---

## Related Skills

| Need                   | Skill                   |
| ---------------------- | ----------------------- |
| Backend implementation | `nodejs-best-practices` |
| Database design        | `database-design`       |
| Security hardening     | `security-fundamentals` |
| Testing APIs           | `testing-patterns`      |

---

> **Remember:** The best API is one that's easy to use correctly and hard to use incorrectly. Prioritize developer experience.
