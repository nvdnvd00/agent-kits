---
name: testing-patterns
description: Testing patterns and principles. Unit, integration, mocking strategies. Use when writing tests, reviewing test coverage, or establishing testing conventions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0
---

# Testing Patterns - Principles & Best Practices

> **Philosophy:** Tests are documentation. Write tests that explain behavior, not implementation.

---

## Test Pyramid

```
          /\            E2E (5-10%)
         /  \           Critical user flows
        /----\
       /      \         Integration (20-30%)
      /--------\        API, DB, services
     /          \
    /------------\      Unit (60-70%)
                        Functions, classes, logic
```

**Rule:** More tests at the base, fewer at the top. Fast, cheap, reliable tests first.

---

## Test Type Selection

```
What are you testing?
│
├─ Pure function / business logic?
│  └─ → Unit test
│
├─ API endpoint / database query?
│  └─ → Integration test
│
├─ Critical user journey?
│  └─ → E2E test
│
├─ External service interaction?
│  └─ → Integration test with mocks
│
└─ UI component rendering?
   └─ → Component test (unit-like)
```

---

## AAA Pattern (Arrange-Act-Assert)

```typescript
// ✅ Clear AAA structure
describe("UserService", () => {
  it("should return user by ID", async () => {
    // Arrange
    const userId = "123";
    const expectedUser = { id: userId, name: "John" };
    mockDb.users.findById.mockResolvedValue(expectedUser);

    // Act
    const result = await userService.getById(userId);

    // Assert
    expect(result).toEqual(expectedUser);
  });
});
```

---

## Unit Test Principles (FIRST)

| Principle           | Meaning            | Example                  |
| ------------------- | ------------------ | ------------------------ |
| **F**ast            | < 100ms each       | No I/O, no network       |
| **I**solated        | No dependencies    | Mock external calls      |
| **R**epeatable      | Same result always | No random, no time       |
| **S**elf-validating | Boolean pass/fail  | No manual verification   |
| **T**imely          | Written with code  | TDD or immediately after |

### What to Unit Test

| ✅ Test        | ❌ Don't Test            |
| -------------- | ------------------------ |
| Business logic | Framework code           |
| Edge cases     | Third-party libraries    |
| Error handling | Simple getters/setters   |
| Calculations   | Constructor-only classes |
| Validations    | Private methods directly |

---

## Integration Test Principles

### What to Integration Test

| Area         | Focus                 | Example              |
| ------------ | --------------------- | -------------------- |
| **API**      | Request/Response      | Correct status codes |
| **Database** | Queries, transactions | Data persistence     |
| **Services** | Inter-service calls   | Message passing      |
| **Auth**     | Token validation      | Protected routes     |

### Setup/Teardown Pattern

```typescript
describe("UserAPI", () => {
  beforeAll(async () => {
    // Connect to test database
    await db.connect();
  });

  beforeEach(async () => {
    // Reset state before each test
    await db.clear();
    await seedTestData();
  });

  afterEach(async () => {
    // Clean up test artifacts
    await cleanupFiles();
  });

  afterAll(async () => {
    // Disconnect resources
    await db.disconnect();
  });
});
```

---

## Mocking Strategy

### When to Mock

| ✅ Mock                  | ❌ Don't Mock       |
| ------------------------ | ------------------- |
| External APIs            | Code under test     |
| Database (in unit tests) | Simple dependencies |
| Time/Date                | Pure functions      |
| Network calls            | In-memory stores    |
| Third-party services     | Internal modules    |

### Mock Types

| Type     | Purpose                      | Example                      |
| -------- | ---------------------------- | ---------------------------- |
| **Stub** | Return fixed values          | `mockFn.mockReturnValue(42)` |
| **Spy**  | Track calls without changing | `jest.spyOn(obj, 'method')`  |
| **Mock** | Replace with expectations    | `jest.fn()`                  |
| **Fake** | Simplified implementation    | In-memory database           |

### Mocking Decision Tree

```
Need to isolate from dependency?
├─ Yes → Is it external (API, DB)?
│  ├─ Yes → Mock it
│  └─ No → Prefer real implementation
│
└─ No → Use real dependency
```

---

## Test Data Strategies

| Strategy    | Use Case              | Example                                   |
| ----------- | --------------------- | ----------------------------------------- |
| **Factory** | Generate varied data  | `createUser({ name: 'John' })`            |
| **Fixture** | Predefined datasets   | JSON files                                |
| **Builder** | Fluent construction   | `UserBuilder.default().withRole('admin')` |
| **Faker**   | Random realistic data | `faker.person.fullName()`                 |

### Factory Pattern Example

```typescript
// factories/user.factory.ts
export const createUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  createdAt: new Date(),
  ...overrides,
});

// Usage
const user = createUser({ role: "admin" });
```

---

## TDD Workflow (Red-Green-Refactor)

```
┌─────────┐      ┌─────────┐      ┌──────────┐
│   RED   │ ──→  │  GREEN  │ ──→  │ REFACTOR │
│  Write  │      │  Write  │      │ Improve  │
│ failing │      │ minimal │      │   code   │
│  test   │      │  code   │      │  quality │
└─────────┘      └─────────┘      └──────────┘
     ↑                                  │
     └──────────────────────────────────┘
```

---

## Test Naming Conventions

| Pattern                           | Example                                  |
| --------------------------------- | ---------------------------------------- |
| **should_behavior**               | `should returnErrorWhenUserNotFound`     |
| **when_condition**                | `whenUserIsNull_throwsError`             |
| **given_when_then**               | `givenValidInput_whenSubmit_thenSuccess` |
| **methodName_condition_expected** | `getUser_withInvalidId_returnsNull`      |

**Rule:** Test names should describe behavior, not implementation.

---

## Coverage Guidelines

| Level    | Meaning                             |
| -------- | ----------------------------------- |
| **80%+** | Good coverage for most projects     |
| **90%+** | High coverage, critical systems     |
| **100%** | Often impractical, may waste effort |

### What to Cover

| Priority   | Area                         |
| ---------- | ---------------------------- |
| **High**   | Business logic, calculations |
| **Medium** | Error paths, edge cases      |
| **Low**    | Simple getters, boilerplate  |

---

## Anti-Patterns

| ❌ Don't                    | ✅ Do                      |
| --------------------------- | -------------------------- |
| Test implementation details | Test behavior/outcomes     |
| Duplicate test code         | Use factories/helpers      |
| Complex test setup          | Simplify or split tests    |
| Ignore flaky tests          | Fix root cause immediately |
| Skip cleanup                | Reset state every test     |
| Test multiple things        | One assertion per test     |
| Hard-code test data         | Use factories              |
| Rely on test order          | Make tests independent     |

---

## Testing Checklist

Before pushing code:

- [ ] All tests pass?
- [ ] Coverage meets threshold?
- [ ] Edge cases covered?
- [ ] Error paths tested?
- [ ] Tests are isolated?
- [ ] No flaky tests?
- [ ] Test names are descriptive?

---

## Related Skills

| Need                | Skill                   |
| ------------------- | ----------------------- |
| Clean code          | `clean-code`            |
| API testing         | `api-patterns`          |
| E2E testing         | `webapp-testing`        |
| Performance testing | `performance-profiling` |

---

> **Remember:** If you can't understand what code does from its tests, rewrite the tests.
