---
name: typescript-patterns
description: TypeScript advanced patterns and type-level programming. Use when writing complex types, designing APIs, optimizing type checking performance, migrating from JavaScript, or debugging type errors. Covers branded types, conditional types, generics, monorepo configuration, and modern tooling decisions.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# TypeScript Patterns

> **Philosophy:** Types are documentation that never lies. Strong types catch bugs at compile time, not runtime.

---

## 📑 Content Map

| File                            | When to Read            |
| ------------------------------- | ----------------------- |
| `references/advanced-types.md`  | Complex type gymnastics |
| `references/error-patterns.md`  | Debugging type errors   |
| `references/migration-guide.md` | JS to TS migration      |

---

## 1. Type-Level Programming Patterns

### Branded Types (Nominal Typing)

```typescript
type Brand<K, T> = K & { __brand: T };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

// ✅ Prevents accidental mixing
function processOrder(orderId: OrderId, userId: UserId) {}

// Usage
const userId = "user-123" as UserId;
const orderId = "order-456" as OrderId;
processOrder(orderId, userId); // ✅ OK
processOrder(userId, orderId); // ❌ Compile error
```

**Use for:** Domain primitives, API boundaries, currency/units, IDs

### Conditional Types

```typescript
// Extract promise result type
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// Deep readonly (recursive)
type DeepReadonly<T> = T extends (...args: any[]) => any
  ? T
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// Pick by value type
type PickByType<T, Value> = {
  [K in keyof T as T[K] extends Value ? K : never]: T[K];
};
```

**Watch for:** Type instantiation depth > 10 levels

### Template Literal Types

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;
// EventName<'click'> = 'onClick'

type PropEventSource<Type> = {
  on<Key extends string & keyof Type>(
    eventName: `${Key}Changed`,
    callback: (newValue: Type[Key]) => void,
  ): void;
};
```

---

## 2. Type Inference Techniques

### `satisfies` Operator (TS 5.0+)

```typescript
// ✅ Constrains while preserving literal types
const config = {
  api: "https://api.example.com",
  timeout: 5000,
  debug: true,
} satisfies Record<string, string | number | boolean>;

// config.api is narrowed to string "https://api.example.com"
// config.timeout is narrowed to 5000, not just number
```

### Const Assertions

```typescript
const routes = ["/home", "/about", "/contact"] as const;
type Route = (typeof routes)[number];
// Route = '/home' | '/about' | '/contact'

const STATUS = {
  PENDING: "pending",
  DONE: "done",
} as const;
type Status = (typeof STATUS)[keyof typeof STATUS];
// Status = 'pending' | 'done'
```

### ReturnType & Parameters

```typescript
function getUser(id: string) {
  return { id, name: "John", email: "john@example.com" };
}

type User = ReturnType<typeof getUser>;
// { id: string; name: string; email: string }

type GetUserParams = Parameters<typeof getUser>;
// [id: string]
```

---

## 3. Strict Configuration (RECOMMENDED)

### Recommended tsconfig

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

| Flag                         | What It Does                                 |
| ---------------------------- | -------------------------------------------- |
| `strict`                     | Enables all strict type checking             |
| `noUncheckedIndexedAccess`   | Array/object access returns `T \| undefined` |
| `noImplicitOverride`         | Require `override` keyword                   |
| `exactOptionalPropertyTypes` | Distinguish `undefined` vs missing           |

---

## 4. Performance Optimization

### Type Checking Performance

```bash
# Diagnose slow type checking
npx tsc --extendedDiagnostics --incremental false | grep -E "Check time|Files:|Lines:|Nodes:"
```

| Problem                       | Solution                    |
| ----------------------------- | --------------------------- |
| Slow type checking            | Enable `skipLibCheck: true` |
| Rebuilding everything         | Enable `incremental: true`  |
| Large codebase                | Use Project References      |
| "Type instantiation too deep" | See fixes below             |

### Fixing "Type instantiation is excessively deep"

1. Replace type intersections (`&`) with interface extends
2. Split large union types (>100 members)
3. Use type aliases to break recursion
4. Limit generic constraint depth

```typescript
// ❌ Bad: Infinite recursion
type InfiniteArray<T> = T | InfiniteArray<T>[];

// ✅ Good: Limited recursion depth
type NestedArray<T, D extends number = 5> = D extends 0
  ? T
  : T | NestedArray<T, Prev[D]>[];

type Prev = [never, 0, 1, 2, 3, 4];
```

---

## 5. Common Error Patterns

### "The inferred type of X cannot be named"

| Cause               | Fix                                  |
| ------------------- | ------------------------------------ |
| Missing type export | Export the required type explicitly  |
| Circular dependency | Use type-only imports: `import type` |
| Complex inference   | Use `ReturnType<typeof fn>`          |

### "Cannot find module"

| Cause                  | Fix                                       |
| ---------------------- | ----------------------------------------- |
| Wrong moduleResolution | Match your bundler (node, bundler)        |
| Missing baseUrl        | Check tsconfig paths alignment            |
| Monorepo setup         | Use workspace protocol (workspace:\*)     |
| Cache issues           | `rm -rf node_modules/.cache .tsbuildinfo` |

### Missing Type Declarations

```typescript
// types/ambient.d.ts
declare module "untyped-package" {
  const value: unknown;
  export default value;
}

// For CJS interop
declare module "cjs-package" {
  const value: unknown;
  export = value;
}
```

---

## 6. Module System Decisions

### ESM-First Approach

| Configuration       | Value                     |
| ------------------- | ------------------------- |
| package.json `type` | `"module"`                |
| moduleResolution    | `"bundler"` or `"node16"` |
| module              | `"esnext"` or `"node16"`  |

### CJS Interop

```typescript
// ✅ Dynamic import for CJS in ESM
const pkg = await import("cjs-package");
const defaultExport = pkg.default || pkg;
```

---

## 7. Monorepo Configuration

### Project References

```json
// Root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" },
    { "path": "./apps/web" }
  ],
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

### Nx vs Turborepo Decision

| Choose        | When                                  |
| ------------- | ------------------------------------- |
| **Turborepo** | Simple structure, speed, <20 packages |
| **Nx**        | Complex deps, visualization, plugins  |

---

## 8. Tooling Decisions

### Biome vs ESLint

| Choose     | When                                     |
| ---------- | ---------------------------------------- |
| **Biome**  | Speed critical, single tool, TS-first    |
| **ESLint** | Need specific rules, Vue/Angular support |

### Type Testing

```typescript
// avatar.test-d.ts (Vitest type testing)
import { expectTypeOf } from "vitest";
import type { Avatar } from "./avatar";

test("Avatar props are correctly typed", () => {
  expectTypeOf<Avatar>().toHaveProperty("size");
  expectTypeOf<Avatar["size"]>().toEqualTypeOf<"sm" | "md" | "lg">();
});
```

**When to test types:** Library APIs, generic functions, type utilities

---

## 9. Best Practices

### Prefer Interface over Type (for objects)

```typescript
// ✅ Better error messages, extends support
interface User {
  id: string;
  name: string;
}

// ✅ Use type for unions, primitives, functions
type Status = "active" | "inactive";
type Handler = (event: Event) => void;
```

### Use Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}

// Discriminated unions for error handling
type Result<T> = { success: true; data: T } | { success: false; error: string };
```

### Exhaustive Switch

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

function handleStatus(status: Status) {
  switch (status) {
    case "active":
      return "Active";
    case "inactive":
      return "Inactive";
    default:
      return assertNever(status); // Catches missing cases
  }
}
```

---

## 10. Anti-Patterns

| ❌ Don't                          | ✅ Do                            |
| --------------------------------- | -------------------------------- |
| `any` everywhere                  | `unknown` with type guards       |
| Excessive type assertions (`as`)  | Proper type inference            |
| Ignoring strict mode              | Enable all strict flags          |
| Complex mapped types in hot paths | Pre-compute, cache types         |
| Index as object key without check | `noUncheckedIndexedAccess: true` |
| Type in separate file from impl   | Co-locate types with code        |
| Over-complicated generics         | Simpler solution first           |

---

## 11. Migration Strategies

### JavaScript to TypeScript

| Phase | Action                                  |
| ----- | --------------------------------------- |
| 1     | Enable `allowJs`, `checkJs` in tsconfig |
| 2     | Rename files `.js` → `.ts` gradually    |
| 3     | Add types file by file                  |
| 4     | Enable strict mode progressively        |

### Useful Tools

| Tool         | Purpose                         |
| ------------ | ------------------------------- |
| `ts-migrate` | Automated migration from Airbnb |
| `typesync`   | Install missing @types          |
| `TypeStat`   | Auto-fix TypeScript types       |

---

## 12. Code Review Checklist

- [ ] No implicit `any` types
- [ ] Return types explicit for public APIs
- [ ] Generic constraints properly defined
- [ ] Discriminated unions for errors
- [ ] Type guards where needed
- [ ] No circular dependencies
- [ ] Consistent import style (absolute/relative)
- [ ] No excessive type assertions

---

## Related Skills

| Need               | Skill                   |
| ------------------ | ----------------------- |
| React + TypeScript | `react-patterns`        |
| API design         | `api-patterns`          |
| Testing            | `testing-patterns`      |
| Performance        | `performance-profiling` |

---

> **Remember:** Good TypeScript code reads like documentation. If the types are confusing, the code is probably confusing too.
