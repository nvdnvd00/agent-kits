---
name: auth-patterns
description: Authentication and authorization principles. Use when implementing JWT, OAuth2, session management, RBAC, or securing APIs. Covers token flows, password security, access control patterns.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Auth Patterns - Security-First Access Control

> **Philosophy:** Authentication answers "Who are you?" Authorization answers "What can you do?" Both must be **server-validated**, never trust the client.

---

## Core Principles

| Principle            | Rule                                                      |
| -------------------- | --------------------------------------------------------- |
| **Server-side**      | All auth checks happen on server, never just client       |
| **Defense in depth** | Multiple layers: HTTPS + tokens + validation + rate limit |
| **Least privilege**  | Grant minimum permissions needed                          |
| **Secure defaults**  | Default deny, explicitly grant access                     |
| **Audit everything** | Log auth events for security monitoring                   |

---

## Authentication Strategy Selection

| Strategy        | Use When                                   | Trade-offs                      |
| --------------- | ------------------------------------------ | ------------------------------- |
| **JWT**         | Stateless APIs, microservices, mobile apps | Token size, can't revoke easily |
| **Session**     | Traditional web apps, SSR                  | Stateful, needs session store   |
| **OAuth2/OIDC** | Social login, SSO, third-party auth        | Complex, external dependency    |
| **API Keys**    | Service-to-service, public APIs            | No user context, rotation       |

---

## JWT Token Flow

### Token Structure

```
Header.Payload.Signature
```

| Part          | Contains               | Purpose                |
| ------------- | ---------------------- | ---------------------- |
| **Header**    | Algorithm, type        | How to verify          |
| **Payload**   | userId, role, exp, iat | Claims about user      |
| **Signature** | HMAC or RSA signature  | Integrity verification |

### Access + Refresh Pattern

```typescript
// Short-lived access token: 15 minutes
const accessToken = jwt.sign({ userId, email, role }, process.env.JWT_SECRET, {
  expiresIn: "15m",
});

// Long-lived refresh token: 7 days
const refreshToken = jwt.sign({ userId }, process.env.JWT_REFRESH_SECRET, {
  expiresIn: "7d",
});
```

| Token Type  | Lifetime | Storage                  | Purpose              |
| ----------- | -------- | ------------------------ | -------------------- |
| **Access**  | 15 min   | Memory / httpOnly cookie | API authorization    |
| **Refresh** | 7 days   | httpOnly cookie + DB     | Get new access token |

---

## Authorization Patterns

### RBAC (Role-Based)

```typescript
enum Role {
  USER = "user",
  MODERATOR = "moderator",
  ADMIN = "admin",
}

// Middleware
function requireRole(...roles: Role[]) {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}

// Usage
app.delete("/users/:id", authenticate, requireRole(Role.ADMIN), handler);
```

### Permission-Based (Fine-grained)

| Permission Pattern | Example        | Description                 |
| ------------------ | -------------- | --------------------------- |
| `resource:action`  | `users:read`   | Can read users              |
| `resource:*`       | `posts:*`      | All actions on posts        |
| `*:*`              | Admin wildcard | Full access (use sparingly) |

### Resource Ownership

```typescript
// Check: user owns this resource OR is admin
async function requireOwnership(req, res, next) {
  const resource = await db.posts.findById(req.params.id);

  if (!resource) return res.status(404).json({ error: "Not found" });

  if (resource.userId !== req.user.id && req.user.role !== "admin") {
    return res.status(403).json({ error: "Not your resource" });
  }

  next();
}
```

---

## Password Security

| Rule                    | Implementation                             |
| ----------------------- | ------------------------------------------ |
| **Hash with bcrypt**    | Salt rounds: 12+                           |
| **Min 12 characters**   | + uppercase + lowercase + number + special |
| **Rate limit attempts** | 5 attempts per 15 min                      |
| **Never log passwords** | Not even errors                            |
| **Secure reset flow**   | Time-limited token via email               |

### Password Flow

```typescript
// Hash on registration
const hash = await bcrypt.hash(password, 12);

// Verify on login
const valid = await bcrypt.compare(password, hash);
```

---

## Cookie Security

| Flag         | Value      | Purpose                       |
| ------------ | ---------- | ----------------------------- |
| **httpOnly** | `true`     | Not accessible via JavaScript |
| **secure**   | `true`     | HTTPS only (production)       |
| **sameSite** | `'strict'` | CSRF protection               |
| **maxAge**   | 86400000   | Expiration (24h in ms)        |

```typescript
res.cookie("token", accessToken, {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "strict",
  maxAge: 24 * 60 * 60 * 1000,
});
```

---

## OAuth2 Simplified

| Flow                   | Use Case                           |
| ---------------------- | ---------------------------------- |
| **Authorization Code** | Web apps with backend              |
| **PKCE**               | SPAs, mobile apps (public clients) |
| **Client Credentials** | Service-to-service                 |

### Basic OAuth2 Flow

```
1. User clicks "Login with Google"
2. Redirect to Google with client_id + redirect_uri
3. User authorizes
4. Google redirects back with code
5. Backend exchanges code for tokens
6. Backend creates/finds user, issues own JWT
```

---

## Decision Trees

### Which Auth Strategy?

```
Building a SPA or mobile app?
├── Yes → JWT with refresh tokens
└── No → Server-rendered web app?
    ├── Yes → Session-based (Redis store)
    └── No → API for other services?
        ├── Yes → API Keys or OAuth2
        └── No → Re-evaluate requirements
```

### Where to Store Tokens?

```
Need access from JavaScript?
├── No → httpOnly cookie (preferred)
└── Yes → Really need it?
    ├── No → httpOnly cookie
    └── Yes (API calls from JS) → Memory only
        ⚠️ Never localStorage (XSS vulnerable)
```

---

## Anti-Patterns (DON'T)

| ❌ Anti-Pattern                  | ✅ Correct Approach            |
| -------------------------------- | ------------------------------ |
| Store JWT in localStorage        | httpOnly cookie or memory      |
| Plain text passwords in DB       | bcrypt hash with salt          |
| Long-lived access tokens (24h+)  | 15 min access + 7d refresh     |
| Client-only auth checks          | Server validates every request |
| Same secret for access & refresh | Separate secrets               |
| No rate limiting on login        | 5 attempts / 15 min            |
| JWT without expiration           | Always set `exp` claim         |
| Hardcoded secrets in code        | Environment variables          |

---

## Security Checklist

| Category       | Check                                 |
| -------------- | ------------------------------------- |
| **Transport**  | HTTPS everywhere, HSTS enabled        |
| **Passwords**  | bcrypt 12+, strong policy enforced    |
| **Tokens**     | Short-lived, httpOnly, secure cookies |
| **Rate Limit** | Login, registration, password reset   |
| **Headers**    | CSP, X-Frame-Options, X-Content-Type  |
| **Logging**    | Auth events logged, no sensitive data |
| **CORS**       | Strict origin whitelist               |

---

## 🔴 Self-Check Before Completing

| Check                      | Question                       |
| -------------------------- | ------------------------------ |
| ✅ **Server validated?**   | All auth happens server-side?  |
| ✅ **Tokens secure?**      | httpOnly, secure, short-lived? |
| ✅ **Passwords hashed?**   | bcrypt with 12+ rounds?        |
| ✅ **Rate limited?**       | Login endpoint protected?      |
| ✅ **HTTPS?**              | All traffic encrypted?         |
| ✅ **No secrets in code?** | Environment variables only?    |

---

## Related Skills

| Need              | Skill                   |
| ----------------- | ----------------------- |
| API design        | `api-patterns`          |
| Security auditing | `security-fundamentals` |
| Database design   | `database-design`       |

---

> **Remember:** Security is not a feature - it's a requirement. The cost of getting auth wrong is data breaches, legal liability, and lost trust. When in doubt, use battle-tested libraries.
