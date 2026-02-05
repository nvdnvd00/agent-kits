---
name: react-patterns
description: React and Next.js performance optimization and design patterns. Use when building React components, optimizing performance, eliminating waterfalls, reducing bundle size, or implementing server/client-side optimizations. Covers hooks, composition, state management, React 19 features, and Vercel best practices.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# React Patterns

> **Philosophy:** Measure first, optimize second. React is about composition - build small, combine thoughtfully.

---

## 📑 Content Map

| File                            | When to Read                  |
| ------------------------------- | ----------------------------- |
| `references/hook-patterns.md`   | Advanced custom hooks         |
| `references/performance.md`     | Deep performance optimization |
| `references/nextjs-patterns.md` | Next.js App Router specific   |

---

## 1. Component Design Principles

### Component Types

| Type               | Use                   | State             | Example                  |
| ------------------ | --------------------- | ----------------- | ------------------------ |
| **Server**         | Data fetching, static | None              | Page layouts, data grids |
| **Client**         | Interactivity         | useState, effects | Forms, modals, dropdowns |
| **Presentational** | UI display            | Props only        | Button, Card, Avatar     |
| **Container**      | Logic/state           | Heavy state       | UserProfileContainer     |

### Design Rules

| Rule                         | Rationale                        |
| ---------------------------- | -------------------------------- |
| One responsibility           | Easier testing, reuse            |
| Props down, events up        | Predictable data flow            |
| Composition over inheritance | Flexibility, avoid prop drilling |
| Small, focused components    | Better tree shaking, readability |

---

## 2. Hook Patterns

### When to Extract Custom Hooks

| Pattern           | Extract When                           |
| ----------------- | -------------------------------------- |
| `useLocalStorage` | Same storage logic needed              |
| `useDebounce`     | Multiple debounced values              |
| `useFetch`        | Repeated fetch patterns                |
| `useForm`         | Complex form state                     |
| `useClickOutside` | Multiple modal/dropdown components     |
| `usePrevious`     | Need previous value in multiple places |

### Hook Rules (CRITICAL)

| Rule                    | Violation Consequence            |
| ----------------------- | -------------------------------- |
| Top level only          | Inconsistent state               |
| Same order every render | React loses track of state       |
| Prefix with "use"       | Lint error, convention violation |
| Clean up effects        | Memory leaks, stale closures     |

### React 19 New Hooks

| Hook             | Purpose                  | Example Use Case               |
| ---------------- | ------------------------ | ------------------------------ |
| `useActionState` | Form submission state    | Server Actions with pending UI |
| `useOptimistic`  | Optimistic UI updates    | Like button, comment posting   |
| `use`            | Read resources in render | Reading promises, context      |
| `useFormStatus`  | Form submission status   | Submit button loading state    |

---

## 3. State Management Selection

### Decision Tree

```
State scope?
│
├── Single component → useState
│
├── Parent-child (1-2 levels) → Lift state up
│
├── Subtree (3+ levels) → Context
│
├── Server state → React Query / SWR
│
└── Complex global → Zustand / Redux Toolkit
```

### State Placement Guide

| Scope            | Solution          | When to Use               |
| ---------------- | ----------------- | ------------------------- |
| Single component | `useState`        | Form inputs, toggles      |
| Parent-child     | Props + callbacks | Controlled components     |
| Subtree          | Context           | Theme, auth, locale       |
| Server state     | React Query       | API data, caching         |
| Complex global   | Zustand           | Cart, filters, multi-step |

---

## 4. Performance Optimization (Priority Order)

### 🔴 CRITICAL: Eliminating Waterfalls

| Pattern             | Problem                      | Solution                            |
| ------------------- | ---------------------------- | ----------------------------------- |
| `async-defer-await` | Blocking unrelated code      | Move await into branches where used |
| `async-parallel`    | Sequential independent calls | `Promise.all()` for independent ops |
| `async-suspense`    | Waiting for all data         | Use Suspense to stream content      |

### 🔴 CRITICAL: Bundle Size

| Pattern                 | Problem                   | Solution                       |
| ----------------------- | ------------------------- | ------------------------------ |
| `bundle-barrel-imports` | Importing entire library  | Import directly from module    |
| `bundle-dynamic`        | Loading unused code       | `next/dynamic` for heavy comps |
| `bundle-defer-third`    | Analytics blocking render | Load after hydration           |

### 🟡 HIGH: Server-Side Performance

| Pattern                | Problem               | Solution                       |
| ---------------------- | --------------------- | ------------------------------ |
| `server-cache-react`   | Duplicate requests    | `React.cache()` per-request    |
| `server-serialization` | Large client payloads | Minimize data passed to client |
| `server-parallel`      | Sequential fetching   | Restructure for parallel       |

### 🟢 MEDIUM: Re-render Optimization

| Pattern                  | Problem                      | Solution                      |
| ------------------------ | ---------------------------- | ----------------------------- |
| `rerender-memo`          | Expensive child re-renders   | Extract to memoized component |
| `rerender-dependencies`  | Unstable effect dependencies | Use primitive dependencies    |
| `rerender-derived-state` | Subscribing to raw values    | Subscribe to derived booleans |
| `rerender-lazy-init`     | Expensive initial state      | Pass function to useState     |

---

## 5. Composition Patterns

### Compound Components

```tsx
// ✅ Flexible composition
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Trigger value="tab1">Tab 1</Tabs.Trigger>
    <Tabs.Trigger value="tab2">Tab 2</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Content value="tab1">Content 1</Tabs.Content>
  <Tabs.Content value="tab2">Content 2</Tabs.Content>
</Tabs>
```

**Use for:** Tabs, Accordion, Dropdown, Modal, Dialog

### Render Props vs Hooks

| Use Case           | Prefer This  | Why                      |
| ------------------ | ------------ | ------------------------ |
| Reusable logic     | Custom hook  | Cleaner, easier to test  |
| Render flexibility | Render props | Consumer controls UI     |
| Cross-cutting      | HOC          | Auth, logging, analytics |

---

## 6. Error Handling

### Error Boundary Strategy

| Scope     | Placement              | Fallback                    |
| --------- | ---------------------- | --------------------------- |
| App-wide  | Root level             | "Something went wrong" page |
| Feature   | Route/feature level    | Feature-specific message    |
| Component | Around risky component | Graceful degradation        |

### Recovery Pattern

| Step | Action                         |
| ---- | ------------------------------ |
| 1    | Show fallback UI               |
| 2    | Log error (Sentry, DataDog)    |
| 3    | Offer retry option             |
| 4    | Preserve user data if possible |

---

## 7. TypeScript Integration

### Props Typing

| Pattern   | Use For               | Example                       |
| --------- | --------------------- | ----------------------------- |
| Interface | Component props       | `interface ButtonProps {}`    |
| Type      | Unions, complex types | `type Status = 'on' \| 'off'` |
| Generic   | Reusable components   | `<DataTable<T>>`              |

### Essential Types

| Need          | Type                     |
| ------------- | ------------------------ |
| Children      | `ReactNode`              |
| Event handler | `MouseEventHandler<T>`   |
| Ref           | `RefObject<Element>`     |
| Component ref | `ComponentRef<typeof X>` |

---

## 8. Testing Priorities

### Test Pyramid for React

| Level       | What to Test                     | Tools               |
| ----------- | -------------------------------- | ------------------- |
| Unit        | Pure functions, hooks logic      | Vitest, Jest        |
| Integration | Component behavior, interactions | React Testing Lib   |
| E2E         | Critical user flows              | Playwright, Cypress |

### Focus Areas

- [ ] User-visible behavior (not implementation)
- [ ] Edge cases (empty states, loading, errors)
- [ ] Accessibility assertions
- [ ] Form validation scenarios

---

## 9. Anti-Patterns

| ❌ Don't                      | ✅ Do                         | Why                         |
| ----------------------------- | ----------------------------- | --------------------------- |
| `'use client'` everywhere     | Server Components by default  | Smaller bundle, better SEO  |
| Prop drilling (5+ levels)     | Context or state management   | Maintainability             |
| Index as key                  | Stable unique ID              | Correct reconciliation      |
| `useEffect` for everything    | Server Components for data    | Avoid waterfalls            |
| Premature optimization        | Profile first                 | Don't guess, measure        |
| Giant components (500+ lines) | Split into smaller pieces     | Testing, reuse, readability |
| Inline function in render     | `useCallback` for stable refs | Performance (when needed)   |

---

## 10. Next.js App Router Specifics

### Server vs Client Decision

```
Does component need...?
│
├── useState, useEffect, event handlers → 'use client'
│
├── Direct data fetching, no interactivity → Server (default)
│
└── Both? → Split: Server parent + Client child
```

### File Conventions

| File            | Purpose          |
| --------------- | ---------------- |
| `page.tsx`      | Route UI         |
| `layout.tsx`    | Shared layout    |
| `loading.tsx`   | Loading skeleton |
| `error.tsx`     | Error boundary   |
| `not-found.tsx` | 404 page         |

### Caching Strategy

| Layer      | Control         | Use Case               |
| ---------- | --------------- | ---------------------- |
| Request    | fetch options   | Per-request caching    |
| Data       | revalidate/tags | ISR, on-demand refresh |
| Full route | route config    | Static pages           |

---

## 11. Quick Decision Trees

### "Which state solution?"

```
Server data? → React Query
Form state? → React Hook Form
Global UI? → Zustand
Theme/Auth? → Context
Simple local? → useState
```

### "Why is it slow?"

```
1. Profile with React DevTools
2. Check for:
   - Unnecessary re-renders → React.memo, useMemo
   - Large bundles → Dynamic imports, barrel avoidance
   - Network waterfalls → Parallel fetching, suspense
   - Memory leaks → Effect cleanup
```

---

## Related Skills

| Need                  | Skill                   |
| --------------------- | ----------------------- |
| Styling               | `tailwind-patterns`     |
| Testing               | `testing-patterns`      |
| API integration       | `api-patterns`          |
| TypeScript advanced   | `typescript-patterns`   |
| Performance deep-dive | `performance-profiling` |

---

> **Remember:** React 19+ with Server Components changes everything. Start server-side, add client only when needed.
