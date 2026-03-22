---
name: nodejs-best-practices
description: Node.js development principles. Express/Fastify patterns, async handling, error management, security.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Node.js Best Practices

## ⚡ Quick Reference

- **Async**: Always `async/await` · Never blocking I/O in hot paths · `Promise.all()` for parallel
- **Error handling**: `try/catch` in all async · Unhandled rejection → exit process · Typed custom errors
- **Event loop**: No sync fs/crypto/heavy compute · Offload to worker threads or background jobs
- **Config**: `dotenv` for local · env vars always · validate with `zod` on startup · never commit `.env`
- **Logging**: `pino` (fast, structured JSON) · Correlation IDs · No console.log in production
- **Security**: `helmet` always · `express-rate-limit` · Validate all inputs (zod) · CORS configured strictly

---



## Core Principles

1. **Async by default** - Never block the event loop
2. **Error handling is mandatory** - Catch everything, crash gracefully
3. **Security first** - Validate input, sanitize output
4. **Observability built-in** - Log structured, trace distributed

---

## 🔧 Framework Selection

- **Express**: Simple APIs, custom needs
- **Fastify**: Performance, schema-first
- **NestJS**: Enterprise, DDD, TypeScript
- **Hono**: Edge runtime, lightweight

---

## 📁 Project Structure

```
src/
├── modules/
│   ├── user/
│   │   ├── user.controller.ts
│   │   ├── user.service.ts
│   │   ├── user.repository.ts
│   │   └── user.dto.ts
│   └── auth/
├── common/
│   ├── middleware/
│   ├── guards/
│   └── decorators/
├── config/
├── lib/
└── app.ts
```

---

## ⚡ Async Patterns

### Error Handling Wrapper

```typescript
const asyncHandler =
  (fn: RequestHandler) => (req: Request, res: Response, next: NextFunction) =>
    Promise.resolve(fn(req, res, next)).catch(next);

// Usage
app.get(
  "/users",
  asyncHandler(async (req, res) => {
    const users = await userService.findAll();
    res.json(users);
  }),
);
```

### Promise Concurrency

```typescript
// ✅ Parallel when independent
const [users, posts] = await Promise.all([getUsers(), getPosts()]);

// ✅ Sequential when dependent
const user = await getUser(id);
const posts = await getPostsByUser(user.id);

// ✅ Limit concurrency for bulk
import pLimit from "p-limit";
const limit = pLimit(5);
await Promise.all(items.map((i) => limit(() => process(i))));
```

---

## 🔒 Security

### Input Validation (Zod)

```typescript
import { z } from "zod";

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8).max(100),
});

// Middleware
app.post(
  "/users",
  asyncHandler(async (req, res) => {
    const data = createUserSchema.parse(req.body);
    // data is now typed and validated
  }),
);
```

### Rate Limiting

```typescript
import rateLimit from "express-rate-limit";

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
});

app.use("/api/", limiter);
```

---

## 🛠️ Error Handling

### Error Class

```typescript
class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
  ) {
    super(message);
    Error.captureStackTrace(this, this.constructor);
  }
}

// Usage
throw new AppError(404, "USER_NOT_FOUND", "User not found");
```

### Global Handler

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: { code: err.code, message: err.message },
    });
  }

  console.error(err);
  res.status(500).json({
    error: { code: "INTERNAL_ERROR", message: "Something went wrong" },
  });
});
```

---

## 📊 Observability

### Structured Logging

```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  transport:
    process.env.NODE_ENV === "development"
      ? { target: "pino-pretty" }
      : undefined,
});

// Usage
logger.info({ userId: user.id }, "User created");
logger.error({ err, requestId }, "Request failed");
```

---

## ✅ Checklist

- [ ] Never `throw` in async without catching
- [ ] All inputs validated and sanitized
- [ ] Rate limiting on public endpoints
- [ ] Structured logging configured
- [ ] Health check endpoint
- [ ] Graceful shutdown handling

---

## ❌ Anti-Patterns

- `async` without error handling: Wrap with asyncHandler
- Callback APIs: Promisify or use async libs
- `console.log` in production: Structured logging
- Sync file operations: Use async fs methods
- Throwing strings: Custom Error classes

---

## 🔗 Related Skills

- `api-patterns` - API design
- `auth-patterns` - Authentication
- `testing-patterns` - Testing
- `docker-patterns` - Containerization
