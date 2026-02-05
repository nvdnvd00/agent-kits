---
description: Test generation and test running command. Creates and executes tests for code.
---

# /test - Test Generation and Execution Workflow

$ARGUMENTS

---

## Trigger

Use when user says: "test", "kiểm tra", "write tests", "run tests", or `/test`

## Agent

Route to `test-engineer` agent

---

## Sub-commands

| Command                | Description                        |
| ---------------------- | ---------------------------------- |
| `/test`                | Run all tests                      |
| `/test [file/feature]` | Generate tests for specific target |
| `/test coverage`       | Show test coverage report          |
| `/test watch`          | Run tests in watch mode            |

---

## 🔴 Critical Rules

1. **Test Pyramid** - Unit > Integration > E2E
2. **AAA Pattern** - Arrange, Act, Assert
3. **Behavior over Implementation** - Test what, not how
4. **One Assertion per Test** - When practical

---

## Workflow

### Phase 1: Analyze Target

Determine what needs testing:

```markdown
## Test Analysis

- **Target**: [File/Feature/Component]
- **Type**: Unit / Integration / E2E
- **Framework**: Jest / Vitest / Playwright / etc.
- **Existing Tests**: [Count] tests found
```

### Phase 2: Generate Test Plan

Create comprehensive test plan:

```markdown
## 🧪 Test Plan: [Target]

| Test Case                     | Type        | Coverage   |
| ----------------------------- | ----------- | ---------- |
| Should create user            | Unit        | Happy path |
| Should reject invalid email   | Unit        | Validation |
| Should handle db error        | Unit        | Error case |
| Should return 404 for missing | Integration | Edge case  |
```

Identify:

- Happy path tests
- Error cases
- Edge cases
- Integration points

### Phase 3: Write Tests

Generate tests using project's framework:

```typescript
describe("[Component/Service]", () => {
  describe("[method/feature]", () => {
    it("should [expected behavior]", async () => {
      // Arrange
      const input = {
        /* test data */
      };

      // Act
      const result = await subject.method(input);

      // Assert
      expect(result).toBeDefined();
    });

    it("should throw for [invalid case]", async () => {
      // Arrange
      const invalidInput = {
        /* invalid data */
      };

      // Act & Assert
      await expect(subject.method(invalidInput)).rejects.toThrow(
        "[ExpectedError]",
      );
    });
  });
});
```

### Phase 4: Execute Tests

Run the tests:

```bash
# Run all tests
pnpm test

# Run specific file
pnpm test src/services/auth.test.ts

# Run with coverage
pnpm test --coverage
```

### Phase 5: Report

Present results to user:

```markdown
## 🧪 Test Results

### Summary

✅ **15 tests** (14 passed, 1 failed)

### By Status

| Status    | Count | Files                      |
| --------- | ----- | -------------------------- |
| ✅ Passed | 14    | auth.test.ts, user.test.ts |
| ❌ Failed | 1     | order.test.ts              |

### Failed Tests

❌ `should calculate total with discount`

- Expected: 90
- Received: 100
- File: `order.test.ts:45`

### Coverage

| Metric     | Value |
| ---------- | ----- |
| Statements | 85%   |
| Branches   | 72%   |
| Functions  | 90%   |
| Lines      | 84%   |

### Next Steps

- Fix failed test in `order.test.ts`
- Consider adding tests for uncovered branches
```

---

## Test Patterns

### Unit Test (AAA Pattern)

```typescript
it("should return user by id", async () => {
  // Arrange
  const userId = "user-123";
  mockDb.findOne.mockResolvedValue({ id: userId, name: "Test" });

  // Act
  const user = await userService.findById(userId);

  // Assert
  expect(user.id).toBe(userId);
  expect(mockDb.findOne).toHaveBeenCalledWith({ id: userId });
});
```

### Integration Test

```typescript
describe("POST /api/users", () => {
  it("should create user and return 201", async () => {
    const response = await request(app)
      .post("/api/users")
      .send({ name: "Test", email: "test@test.com" });

    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();
  });
});
```

### E2E Test (Playwright)

```typescript
test("user can login and see dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[name="email"]', "test@test.com");
  await page.fill('[name="password"]', "password123");
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL("/dashboard");
  await expect(page.locator("h1")).toContainText("Welcome");
});
```

---

## Exit Conditions

- ✅ **Success:** All tests passing, coverage targets met
- ❌ **Failure:** Tests cannot run due to syntax/config errors
- ⚠️ **Warning:** Tests run but some fail, coverage below target

---

## Usage Examples

```
/test
/test src/services/auth.service.ts
/test user registration flow
/test coverage
/test fix failed tests
```
