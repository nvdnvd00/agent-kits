---
name: documentation-templates
description: Documentation templates and patterns. README, API docs, ADRs, code comments, and technical writing. Use when writing project documentation, API references, or architecture decisions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Documentation Templates

> Good documentation is the difference between a project that gets adopted and one that gets abandoned.

---

## Core Principles

1. **Write for your audience** - Different docs for different readers
2. **Show, don't tell** - Examples over explanations
3. **Keep it current** - Outdated docs are worse than no docs
4. **Start with why** - Context before details
5. **Make it scannable** - Headers, lists, code blocks

---

## 📖 README Template

```markdown
# Project Name

> One-line description of what this does.

[![Build Status](badge-url)](link)
[![npm version](badge-url)](link)
[![License](badge-url)](link)

## ✨ Features

- **Feature 1** - Brief description
- **Feature 2** - Brief description
- **Feature 3** - Brief description

## 🚀 Quick Start

\`\`\`bash

# Install

npm install your-package

# Run

npm start
\`\`\`

## 📦 Installation

\`\`\`bash

# npm

npm install your-package

# pnpm (recommended)

pnpm add your-package

# yarn

yarn add your-package
\`\`\`

## 🔧 Usage

### Basic Example

\`\`\`typescript
import { something } from 'your-package';

const result = something();
console.log(result);
\`\`\`

### Advanced Example

\`\`\`typescript
// More complex usage...
\`\`\`

## ⚙️ Configuration

| Option    | Type     | Default | Description      |
| --------- | -------- | ------- | ---------------- |
| `option1` | `string` | `""`    | Description here |
| `option2` | `number` | `10`    | Description here |

## 📚 Documentation

- [Full Documentation](link)
- [API Reference](link)
- [Examples](link)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

[MIT](LICENSE) © [Your Name]
```

---

## 📋 API Documentation

### Endpoint Documentation

```markdown
## Create User

Creates a new user account.

### Request

`POST /api/v1/users`

#### Headers

| Header          | Required | Description        |
| --------------- | -------- | ------------------ |
| `Authorization` | Yes      | Bearer token       |
| `Content-Type`  | Yes      | `application/json` |

#### Body

\`\`\`json
{
"email": "user@example.com",
"name": "John Doe",
"role": "user"
}
\`\`\`

| Field   | Type     | Required | Description         |
| ------- | -------- | -------- | ------------------- |
| `email` | `string` | Yes      | Valid email address |
| `name`  | `string` | Yes      | 2-100 characters    |
| `role`  | `string` | No       | Default: `"user"`   |

### Response

#### Success (201 Created)

\`\`\`json
{
"id": "user_abc123",
"email": "user@example.com",
"name": "John Doe",
"role": "user",
"createdAt": "2025-01-15T10:30:00Z"
}
\`\`\`

#### Errors

| Status | Code               | Description              |
| ------ | ------------------ | ------------------------ |
| 400    | `VALIDATION_ERROR` | Invalid input data       |
| 409    | `EMAIL_EXISTS`     | Email already registered |
| 401    | `UNAUTHORIZED`     | Invalid or missing token |

### Example

\`\`\`bash
curl -X POST https://api.example.com/v1/users \
 -H "Authorization: Bearer token123" \
 -H "Content-Type: application/json" \
 -d '{"email": "user@example.com", "name": "John Doe"}'
\`\`\`
```

---

## 🏗️ Architecture Decision Record (ADR)

```markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status

Accepted

## Context

We need to choose a primary database for the application. Key requirements:

- Strong consistency for financial transactions
- JSON support for flexible metadata
- Scalability to 10M+ records
- Team familiarity

## Decision

We will use **PostgreSQL 16** as our primary database.

## Alternatives Considered

### MySQL 8

- ✅ Team familiar
- ❌ Weaker JSON support
- ❌ Less flexible indexing

### MongoDB

- ✅ Flexible schema
- ❌ Eventual consistency issues
- ❌ Less mature for transactions

## Consequences

### Positive

- Excellent JSON support with JSONB
- Row-level security for multi-tenancy
- Strong ecosystem (extensions, tools)

### Negative

- More complex scaling than NoSQL
- Requires careful index management

### Risks

- Connection pooling needed at scale
- Mitigation: Use PgBouncer

## Decision Date

2025-01-15

## Decision Makers

- @lead-developer
- @database-specialist
```

---

## 📝 Code Comments

### Function Documentation (JSDoc)

````typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @example
 * ```ts
 * const total = calculateTotal(100, 0.1, 20);
 * // Returns: 88 (100 - 20 = 80, 80 * 1.1 = 88)
 * ```
 *
 * @param basePrice - The original price before adjustments
 * @param taxRate - Tax rate as decimal (0.1 = 10%)
 * @param discount - Flat discount amount to subtract
 * @returns The final calculated price
 * @throws {Error} If basePrice is negative
 */
function calculateTotal(
  basePrice: number,
  taxRate: number,
  discount: number = 0,
): number {
  if (basePrice < 0) {
    throw new Error("Base price cannot be negative");
  }
  const afterDiscount = basePrice - discount;
  return afterDiscount * (1 + taxRate);
}
````

### Module Header

```typescript
/**
 * @module UserService
 * @description Handles user authentication, registration, and profile management.
 *
 * ## Architecture
 * - Uses Repository pattern for data access
 * - Events emitted for user lifecycle (created, updated, deleted)
 * - Passwords hashed with bcrypt (cost factor 12)
 *
 * ## Dependencies
 * - UserRepository: Database operations
 * - EmailService: Verification emails
 * - EventBus: Lifecycle events
 *
 * @see {@link UserRepository} for data layer
 * @see {@link AuthMiddleware} for request authentication
 */
```

### Complex Logic Comments

```typescript
// WHY: We use a two-phase approach here because:
// 1. First pass filters invalid entries without expensive validation
// 2. Second pass performs full validation only on candidates
// This reduces processing time by ~60% for large datasets
const candidates = items.filter(isCandidate);
const validated = candidates.filter(fullValidation);
```

---

## 📊 Changelog (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- New feature X for better Y

### Changed

- Updated dependency Z to v2.0

## [1.2.0] - 2025-01-15

### Added

- User profile API endpoints
- Email verification flow
- Rate limiting on auth endpoints

### Changed

- Improved error messages for validation failures
- Updated TypeScript to 5.3

### Fixed

- Race condition in session refresh
- Memory leak in WebSocket handler

### Security

- Updated bcrypt to patch CVE-2025-xxxx

## [1.1.0] - 2025-01-01

### Added

- Initial release with core features
```

---

## 📁 Common Doc Structures

### docs/ Folder

```
docs/
├── getting-started.md    # Quick start guide
├── installation.md       # Detailed installation
├── configuration.md      # Config options
├── api/                  # API reference
│   ├── overview.md
│   ├── authentication.md
│   └── endpoints/
├── guides/               # How-to guides
│   ├── deployment.md
│   └── migration.md
├── architecture/         # ADRs
│   ├── README.md
│   └── decisions/
└── contributing.md       # Contribution guide
```

---

## ✅ Documentation Checklist

### README

- [ ] Clear project description
- [ ] Quick start (< 5 steps)
- [ ] Installation instructions
- [ ] Basic usage example
- [ ] Configuration options
- [ ] Links to full docs

### API Docs

- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error codes explained
- [ ] Authentication shown
- [ ] Rate limits noted

### Code

- [ ] Public APIs have JSDoc
- [ ] Complex logic explained
- [ ] Edge cases noted
- [ ] Examples in docstrings

---

## ❌ Anti-Patterns

| ❌ Don't                        | ✅ Do                           |
| ------------------------------- | ------------------------------- |
| Document implementation details | Document behavior and contracts |
| Write docs after release        | Write docs during development   |
| Skip error documentation        | Document all error cases        |
| Use outdated examples           | Test examples in CI             |
| Wall of text without structure  | Use headers, lists, code blocks |
| Assume reader knows context     | Explain the "why" first         |

---

## 🔗 Related Skills

| Need         | Skill              |
| ------------ | ------------------ |
| API design   | `api-patterns`     |
| Clean code   | `clean-code`       |
| Architecture | `mermaid-diagrams` |

---

> **Remember:** The best documentation is the documentation that gets read. Make it scannable, keep it current, and always include working examples.
