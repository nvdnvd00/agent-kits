---
name: clean-code
description: Pragmatic coding standards - concise, direct, no over-engineering. Use when writing any code, reviewing code, or establishing project conventions. Covers naming, function design, code structure, and AI coding style.
allowed-tools: Read, Write, Edit
version: 2.0
priority: CRITICAL
---

# Clean Code - Pragmatic AI Coding Standards

## ⚡ Quick Reference

- **SRP + DRY + KISS**: 1 function = 1 thing · no duplication · simplest solution
- **Naming**: `verb+noun` functions · `noun` variables · `is/has` booleans · no abbreviations
- **Functions**: ≤20 lines · ≤3 params · return early · no side effects hidden
- **No over-engineering**: No abstractions without 3+ uses · No premature optimization
- **Error handling**: Never silent catch · always typed errors · fail fast

---

---

## Core Principles

- **SRP**: Single Responsibility - each function/class does ONE thing
- **DRY**: Don't Repeat Yourself - extract duplicates, reuse
- **KISS**: Keep It Simple - simplest solution that works
- **YAGNI**: You Aren't Gonna Need It - don't build unused features
- **Boy Scout**: Leave code cleaner than you found it

---

## Naming Rules

- **Variables**: Reveal intent: `userCount` not `n`
- **Functions**: Verb + noun: `getUserById()` not `user()`
- **Booleans**: Question form: `isActive`, `hasPermission`, `canEdit`
- **Constants**: SCREAMING_SNAKE: `MAX_RETRY_COUNT`
- **Classes**: PascalCase nouns: `UserService`, `PaymentGateway`
- **Files**: kebab-case or camelCase based on project convention

> **Rule:** If you need a comment to explain a name, rename it.

---

## Function Rules

- **Small**: Max 20 lines, ideally 5-10
- **One Thing**: Does one thing, does it well
- **One Level**: One level of abstraction per function
- **Few Args**: Max 3 arguments, prefer 0-2
- **No Side Effects**: Don't mutate inputs unexpectedly
- **Pure When Possible**: Same input → same output

---

## Code Structure

- **Guard Clauses**: Early returns for edge cases
- **Flat > Nested**: Avoid deep nesting (max 2 levels)
- **Composition**: Small functions composed together
- **Colocation**: Keep related code close
- **Vertical Slice**: Feature files together, not by layer type

### Guard Clause Example

```typescript
// ❌ Nested
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        // actual logic 3 levels deep
      }
    }
  }
}

// ✅ Guard Clauses
function processUser(user) {
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.hasPermission) return null;

  // actual logic at top level
}
```

---

## AI Coding Style

- User asks for feature: Write it directly
- User reports bug: Fix it, don't explain first
- No clear requirement: Ask, don't assume
- Multiple valid approaches: Pick one, mention alternatives if critical

### Output Quality Rules

- **No Preamble**: Skip "Here's the code..." - just write code
- **No Postamble**: Skip "This code does..." - let code speak
- **Minimal Comments**: Only for complex/non-obvious business logic
- **Complete Code**: No `// ... rest of code` placeholders
- **Test Immediately**: Run/verify code before claiming complete

---

## Error Handling Patterns

- **Return Early**: Validation failures, missing data
- **Throw Specific**: Domain errors, use custom error classes
- **Try/Catch**: External calls, I/O operations
- **Result Type**: Complex operations, functional style

### Error Handling Example

```typescript
// ❌ Generic
throw new Error("Something went wrong");

// ✅ Specific
throw new UserNotFoundError(userId);
throw new InsufficientFundsError(amount, balance);
```

---

## Anti-Patterns (DON'T)

- Comment every line: Delete obvious comments
- Helper for one-liner: Inline the code
- Factory for 2 objects: Direct instantiation
- utils.ts with 1 function: Put code where used
- "First we import...": Just write code
- Deep nesting (3+ levels): Guard clauses
- Magic numbers: Named constants
- God functions (50+ lines): Split by responsibility
- Premature optimization: Make it work first
- Helper folder with 20 files: Colocate with features

---

## 🔴 Before Editing ANY File (THINK FIRST!)

**Before changing a file, ask yourself:**

- **What imports this file?**: They might break
- **What does this file import?**: Interface changes
- **What tests cover this?**: Tests might fail
- **Is this a shared component?**: Multiple places affected

**Quick Check:**

```
File to edit: UserService.ts
└── Who imports this? → UserController.ts, AuthController.ts
└── Do they need changes too? → Check function signatures
```

> 🔴 **Rule:** Edit the file + all dependent files in the SAME task.
> 🔴 **Never leave broken imports or missing updates.**

---

## Summary

- Write code directly: Write tutorials
- Let code self-document: Add obvious comments
- Fix bugs immediately: Explain the fix first
- Inline small things: Create unnecessary files
- Name things clearly: Use abbreviations
- Keep functions small: Write 100+ line functions
- Verify code works: Claim done without testing

---

## 🔴 Self-Check Before Completing (MANDATORY)

**Before saying "task complete", verify:**

- ✅ **Goal met?**: Did I do exactly what user asked?
- ✅ **Files edited?**: Did I modify all necessary files?
- ✅ **Code works?**: Did I test/verify the change?
- ✅ **No errors?**: Lint and TypeScript pass?
- ✅ **Nothing forgotten?**: Any edge cases missed?

> 🔴 **Rule:** If ANY check fails, fix it before completing.

---

## Decision Trees

### When to Abstract?

```
Is code duplicated 3+ times?
├── Yes → Extract function/component
└── No → Is code complex AND reusable?
    ├── Yes → Extract with clear interface
    └── No → Keep inline
```

### When to Comment?

```
Is logic non-obvious?
├── No → Don't comment
└── Yes → Is it business logic or algorithm?
    ├── Business logic → Comment the WHY
    └── Algorithm → Link to reference + brief WHY
```

---

## Related Skills

- API design patterns: `api-patterns`
- Testing methodology: `testing-patterns`
- Systematic debugging: `systematic-debugging`
- Database design: `database-design`

---

> **Remember:** The user wants working code, not a programming lesson. Be concise, be direct, be effective.
