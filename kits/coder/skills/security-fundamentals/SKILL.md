---
name: security-fundamentals
description: Security coding principles and decision-making. Use when reviewing code for vulnerabilities, implementing validation/sanitization, designing authentication, or analyzing threats. Covers OWASP 2025, input handling, secure architecture patterns.
allowed-tools: Read, Edit, Glob, Grep
---

# Security Fundamentals - Thinking Like an Attacker

## ⚡ Quick Reference

- **Zero Trust**: Validate all inputs · No trust by location · Fail secure (deny on error)
- **OWASP Top 10**: Access Control · Security Misconfig · Supply Chain · Crypto Failures · Injection · Auth Failures
- **Input**: Validate type+length+format · Parameterized queries (no string concat) · Sanitize HTML output
- **Auth**: bcrypt/Argon2 for passwords · JWT 15min expiry · httpOnly cookies for refresh · Rate limit login
- **Secrets**: Never in code/logs · `.env` for local · Vault/SecretsManager for prod · Rotate regularly
- **HTTPS**: TLS 1.2+ only · HSTS header · CSP header · No mixed content

---

---

## 🎯 Core Principle: Zero Trust

```
❌ WRONG: "This input comes from our backend, so it's safe"
✅ CORRECT: "All input is untrusted until explicitly validated"
```

Every data source is potentially compromised:

- User forms → Direct attack vector
- API responses → Server could be compromised
- Database reads → Data could be poisoned
- File uploads → Executable content
- Environment variables → Misconfiguration

---

## 🔒 Security Decision Framework

### When to Apply Security Measures

| Data Type        | Validation         | Sanitization      | Encoding  | Rate Limit |
| ---------------- | ------------------ | ----------------- | --------- | ---------- |
| User form input  | ✅ ALWAYS          | ✅ ALWAYS         | ✅ Output | Consider   |
| API request body | ✅ ALWAYS          | ✅ ALWAYS         | ✅ Output | ✅ ALWAYS  |
| URL parameters   | ✅ ALWAYS          | ✅ ALWAYS         | ✅ Output | ✅ ALWAYS  |
| File uploads     | ✅ ALWAYS          | N/A               | N/A       | ✅ ALWAYS  |
| Database reads   | Verify integrity   | ✅ Before display | ✅ Output | N/A        |
| Third-party APIs | ✅ Response schema | ✅ ALWAYS         | ✅ Output | N/A        |

---

## 📋 OWASP Top 10 - 2025 Reference

### Quick Decision: Which vulnerability applies?

| Symptom                  | Likely Vulnerability        | First Action              |
| ------------------------ | --------------------------- | ------------------------- |
| User input in SQL        | SQL Injection (A03)         | Use parameterized queries |
| User input in HTML       | XSS (A03)                   | Encode output, CSP        |
| User input in file paths | Path Traversal              | Validate, use allowlist   |
| Secrets in code          | Sensitive Data (A02)        | Move to env vars          |
| No auth on endpoint      | Broken Access (A01)         | Add auth + authz checks   |
| Old dependencies         | Vulnerable Components (A06) | Audit + update            |
| User-controlled redirect | SSRF / Open Redirect        | Validate destination      |

### A01: Broken Access Control

**Decision Tree:**

```
Is user authenticated?
├── No → Deny access (401)
└── Yes → Is user authorized for THIS resource?
    ├── No → Deny access (403)
    └── Yes → Also check:
        ├── Resource belongs to user's tenant?
        ├── Action allowed on this resource state?
        └── Rate limit exceeded?
```

**Implementation Pattern:**

```typescript
// ✅ CORRECT: Always verify ownership
async getResource(userId: string, resourceId: string) {
  const resource = await this.repo.findById(resourceId);

  if (!resource) throw new NotFoundException();
  if (resource.ownerId !== userId) throw new ForbiddenException();

  return resource;
}

// ❌ WRONG: Trust resourceId from request
async getResource(resourceId: string) {
  return this.repo.findById(resourceId); // IDOR vulnerability!
}
```

### A03: Injection

**Input Handling Decision:**

| Context    | Technique             | Example                                  |
| ---------- | --------------------- | ---------------------------------------- |
| SQL        | Parameterized queries | `WHERE id = $1` not `WHERE id = '${id}'` |
| NoSQL      | Sanitize operators    | Remove `$where`, `$gt`, etc.             |
| OS Command | Avoid if possible     | Use APIs instead of `exec()`             |
| LDAP       | Escape special chars  | Escape `*`, `(`, `)`, `\`                |
| HTML       | Encode output         | `&lt;` not `<`                           |
| JavaScript | Never eval user input | No `eval()`, `new Function()`            |

**Validation Strategy:**

```
Syntactic Validation     Semantic Validation
(Format is correct)  →   (Value makes sense)

- Email regex match      - Email domain exists
- Date format valid      - Date is in future
- Phone digits only      - Phone length correct
- URL is well-formed     - URL domain is whitelisted
```

---

## 🛡️ Input Validation Patterns

### Allow-List vs Block-List

```
❌ Block-list (Deny known bad)
  - "Block <script> tags"
  - Attackers find bypass: "><script>, <scr<script>ipt>

✅ Allow-list (Allow known good)
  - "Accept only [a-zA-Z0-9 ] for username"
  - Unknown patterns automatically rejected
```

### Validation Implementation

```typescript
// Define explicit rules (Allow-list approach)
const usernameSchema = z
  .string()
  .min(3, "Too short")
  .max(20, "Too long")
  .regex(/^[a-zA-Z0-9_]+$/, "Invalid characters");

// Validate as early as possible
function createUser(input: unknown) {
  const validated = usernameSchema.parse(input.username); // Throws if invalid
  // Now `validated` is safe to use
}
```

### Common Validation Rules

| Field Type | Validation Rules                           |
| ---------- | ------------------------------------------ |
| Username   | ^[a-zA-Z0-9_]{3,20}$                       |
| Email      | RFC 5322 regex + domain check              |
| Password   | Min 12 chars, complexity rules             |
| Phone      | Digits only, length 10-15                  |
| UUID       | ^[0-9a-f]{8}-... pattern                   |
| URL        | Scheme allowlist (https), domain allowlist |
| File       | Extension allowlist, magic bytes, max size |
| Date       | ISO 8601, reasonable range                 |
| Number     | Min/max bounds, integer vs float           |
| Free text  | Max length, no control chars               |

---

## 🧹 Sanitization Patterns

### When to Sanitize

```
Validation → Accept or Reject
Sanitization → Clean and Transform

Use sanitization when:
- You must accept rich content (HTML emails)
- Transforming data format (trim whitespace)
- Removing known-dangerous patterns

Do NOT use sanitization as primary defense:
- "Sanitize SQL" → Use prepared statements instead
- "Sanitize for XSS" → Encode output instead
```

### HTML Sanitization

```typescript
// Using DOMPurify for user-generated HTML
import DOMPurify from "dompurify";

const dirtyHTML = userInput;
const cleanHTML = DOMPurify.sanitize(dirtyHTML, {
  ALLOWED_TAGS: ["p", "b", "i", "a", "ul", "li"],
  ALLOWED_ATTR: ["href"],
  ALLOW_DATA_ATTR: false,
});
```

### Output Encoding

| Context           | Encoding                          |
| ----------------- | --------------------------------- |
| HTML body         | HTML entity encode (`<` → `&lt;`) |
| HTML attribute    | Attribute encode + quote          |
| JavaScript string | JS escape + avoid eval            |
| CSS value         | CSS escape, avoid `url()`         |
| URL parameter     | URL encode (`%20`)                |
| JSON              | JSON.stringify (auto-escapes)     |

---

## 🔐 Authentication Security

### Password Storage

```
❌ Plain text, MD5, SHA1, SHA256 (fast = bad)
✅ bcrypt, scrypt, Argon2 (slow = good)

Cost factor: ~100ms per hash (adjust for hardware)
```

### Session Security

| Aspect       | Requirement                         |
| ------------ | ----------------------------------- |
| Session ID   | Cryptographically random, 128+ bits |
| Storage      | HttpOnly cookie (not localStorage)  |
| Transmission | Secure flag (HTTPS only)            |
| Expiration   | Reasonable timeout, absolute + idle |
| Rotation     | New ID after privilege change       |

### JWT Security

```
❌ Algorithm "none" accepted
❌ Weak secret (dictionary words)
❌ Sensitive data in payload (tokens are base64, not encrypted)
❌ Long-lived tokens (days/weeks)

✅ RS256 or ES256 (asymmetric)
✅ Short expiration (15 min) + refresh tokens
✅ Verify issuer, audience, expiration
✅ Store refresh token securely (httpOnly cookie)
```

---

## 🌐 API Security

### Rate Limiting Strategy

| Endpoint Type        | Limit      | Window | Action on Exceed  |
| -------------------- | ---------- | ------ | ----------------- |
| Authentication       | 5 attempts | 15 min | Lock + notify     |
| Password reset       | 3 requests | 1 hour | Delay response    |
| API general          | 100 req    | 1 min  | 429 + Retry-After |
| Expensive operations | 10 req     | 1 hour | Queue + notify    |

### CORS Configuration

```typescript
// ❌ DANGEROUS: Allow all origins
app.use(cors({ origin: "*" }));

// ✅ CORRECT: Explicit allowlist
app.use(
  cors({
    origin: ["https://app.example.com", "https://admin.example.com"],
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
  }),
);
```

### Security Headers

```typescript
const securityHeaders = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self'",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "geolocation=(), microphone=()",
};
```

---

## 🚨 Anti-Patterns

| ❌ Don't                                | ✅ Do                              |
| --------------------------------------- | ---------------------------------- |
| Store passwords in plain text           | Use bcrypt/Argon2 with proper cost |
| Concatenate SQL strings                 | Use parameterized queries          |
| Disable SSL verification                | Fix certificate issues properly    |
| Log sensitive data                      | Mask/redact before logging         |
| Use `eval()` with user input            | Find alternative approach          |
| Trust client-side validation            | Always validate server-side        |
| Commit secrets to repo                  | Use environment variables          |
| Use `*` for CORS origin                 | Explicit domain allowlist          |
| Disable security features "temporarily" | Never—find proper solution         |
| Roll your own crypto                    | Use established libraries          |

---

## 📊 Security Review Checklist

### For Code Review

```markdown
## Security Review: [Feature/PR Name]

### Input Handling

- [ ] All user input validated (type, format, length, range)
- [ ] Validation uses allow-list approach
- [ ] Output properly encoded for context

### Authentication & Authorization

- [ ] Every endpoint has auth check
- [ ] Resource ownership verified (no IDOR)
- [ ] Sensitive actions require re-authentication

### Data Protection

- [ ] No secrets in code or logs
- [ ] Sensitive data encrypted at rest
- [ ] PII handling follows regulations

### API Security

- [ ] Rate limiting in place
- [ ] CORS properly configured
- [ ] Security headers set
```

---

## 🔗 Related Skills

| Need                  | Skill              |
| --------------------- | ------------------ |
| API design patterns   | `api-patterns`     |
| Database security     | `database-design`  |
| Testing for security  | `testing-patterns` |
| Clean code principles | `clean-code`       |

---

## 📚 References

- [OWASP Top 10 2025](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

---

> **Remember:** Security is everyone's responsibility. When in doubt, assume the input is malicious.
