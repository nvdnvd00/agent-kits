---
name: e2e-testing
description: End-to-end testing patterns with Playwright and Cypress. Use when implementing E2E tests, debugging flaky tests, testing critical user flows, setting up CI/CD test pipelines, or establishing E2E testing standards. Covers test design, reliability patterns, CI integration, and visual regression.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# E2E Testing Patterns

> **Philosophy:** E2E tests should give confidence to ship, not slow you down. Test critical paths, make them reliable, run them fast.

---

## 📑 Content Map

| File                             | When to Read                 |
| -------------------------------- | ---------------------------- |
| `references/playwright-api.md`   | Playwright-specific patterns |
| `references/cypress-patterns.md` | Cypress-specific patterns    |
| `references/ci-integration.md`   | CI/CD setup and optimization |

---

## 1. When to Use E2E Testing

### ✅ Use E2E When

| Scenario                    | Why E2E                     |
| --------------------------- | --------------------------- |
| Critical user journeys      | Full flow validation        |
| Authentication flows        | Security-critical paths     |
| Payment/checkout            | Money-critical paths        |
| Cross-browser compatibility | Real browser behavior       |
| Accessibility validation    | Full page context needed    |
| Visual regression           | Layout/styling verification |

### ❌ Don't Use E2E When

| Scenario                        | Better Alternative                  |
| ------------------------------- | ----------------------------------- |
| Unit logic testing              | Unit tests (Vitest, Jest)           |
| Component behavior              | Integration tests (Testing Library) |
| API contract validation         | API tests (Supertest, Hurl)         |
| Unstable/frequently changing UI | Lower-level tests first             |

---

## 2. Playwright vs Cypress Decision

| Factor                | Playwright                  | Cypress               |
| --------------------- | --------------------------- | --------------------- |
| **Multi-browser**     | ✅ Chrome, FF, Safari, Edge | ⚠️ Limited Safari     |
| **Speed**             | ✅ Faster parallel          | ⚠️ Slower             |
| **Cross-origin**      | ✅ Full support             | ⚠️ Limited            |
| **API testing**       | ✅ Built-in                 | ⚠️ Needs plugins      |
| **Learning curve**    | Medium                      | Easy                  |
| **Debugging**         | Trace viewer                | Time-travel debugging |
| **Component testing** | ✅ Supported                | ✅ Supported          |

**Recommendation:** Use **Playwright** for new projects (2025+).

---

## 3. Test Design Principles

### Page Object Model (POM)

```typescript
// pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  readonly email = this.page.getByLabel("Email");
  readonly password = this.page.getByLabel("Password");
  readonly submitBtn = this.page.getByRole("button", { name: "Sign in" });
  readonly errorMessage = this.page.getByRole("alert");

  async login(email: string, password: string) {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submitBtn.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// tests/login.spec.ts
test("successful login redirects to dashboard", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto("/login");

  await loginPage.login("user@example.com", "password123");

  await expect(page).toHaveURL("/dashboard");
});
```

### Test Structure (AAA Pattern)

| Phase       | Action                     |
| ----------- | -------------------------- |
| **Arrange** | Navigate, set up test data |
| **Act**     | Perform user actions       |
| **Assert**  | Verify expected outcomes   |

---

## 4. Selector Strategies (Priority Order)

### ✅ Recommended Selectors

| Priority | Selector Type        | Example                                 |
| -------- | -------------------- | --------------------------------------- |
| 1        | Role (accessibility) | `getByRole('button', {name: 'Submit'})` |
| 2        | Label                | `getByLabel('Email')`                   |
| 3        | Placeholder          | `getByPlaceholder('Search...')`         |
| 4        | Text                 | `getByText('Welcome')`                  |
| 5        | Test ID              | `getByTestId('submit-btn')`             |

### ❌ Avoid

| Selector      | Why                         |
| ------------- | --------------------------- |
| CSS class     | Styling changes break tests |
| Tag name only | Too generic, fragile        |
| XPath         | Hard to read, fragile       |
| nth-child     | Order-dependent, fragile    |

---

## 5. Reliability Patterns

### Auto-Waiting (Playwright)

```typescript
// ✅ Playwright auto-waits for elements
await page.click("button"); // Waits until clickable

// ✅ Explicit assertions wait
await expect(page.getByRole("heading")).toBeVisible();
await expect(page.getByTestId("data")).toContainText("Loaded");
```

### Handling Flaky Tests

| Symptom                | Solution                                |
| ---------------------- | --------------------------------------- |
| Element not found      | Use auto-wait, increase timeout         |
| Race conditions        | Wait for network idle, specific element |
| Animation interference | Disable animations in CI                |
| Timing issues          | Use explicit waits, not setTimeout      |

```typescript
// ✅ Wait for network idle
await page.goto("/dashboard", { waitUntil: "networkidle" });

// ✅ Wait for specific element
await page.waitForSelector('[data-testid="data-loaded"]');

// ✅ Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('a[href="/next-page"]'),
]);
```

### Test Isolation

```typescript
// ✅ Each test gets fresh context
test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

// ✅ Clean up after destructive tests
test.afterEach(async ({ request }) => {
  await request.delete("/api/test-data");
});
```

---

## 6. Authentication Patterns

### Reusable Auth State

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: "setup", testMatch: /.*\.setup\.ts/ },
    {
      name: "chromium",
      dependencies: ["setup"],
      use: {
        storageState: "playwright/.auth/user.json",
      },
    },
  ],
});

// tests/auth.setup.ts
import { test as setup, expect } from "@playwright/test";

setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("user@example.com");
  await page.getByLabel("Password").fill("password123");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page).toHaveURL("/dashboard");
  await page.context().storageState({ path: "playwright/.auth/user.json" });
});
```

---

## 7. Visual Regression Testing

### Playwright Screenshots

```typescript
test("homepage visual regression", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage.png", {
    maxDiffPixels: 100,
    animations: "disabled",
  });
});

// Component screenshot
test("button states", async ({ page }) => {
  const button = page.getByRole("button", { name: "Submit" });
  await expect(button).toHaveScreenshot("button-default.png");

  await button.hover();
  await expect(button).toHaveScreenshot("button-hover.png");
});
```

### Viewport Testing

```typescript
const viewports = [
  { name: "mobile", width: 375, height: 667 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1920, height: 1080 },
];

for (const viewport of viewports) {
  test(`responsive - ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto("/");
    await expect(page).toHaveScreenshot(`${viewport.name}.png`);
  });
}
```

---

## 8. API Testing with Playwright

### Mock API Responses

```typescript
test("handles API error gracefully", async ({ page }) => {
  await page.route("**/api/users", (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: "Server error" }),
    });
  });

  await page.goto("/users");
  await expect(page.getByRole("alert")).toContainText("Something went wrong");
});
```

### API Request Testing

```typescript
test("API returns correct data", async ({ request }) => {
  const response = await request.get("/api/users");

  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  expect(data.users).toHaveLength(10);
});
```

---

## 9. CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - name: Install dependencies
        run: pnpm install

      - name: Install Playwright
        run: pnpm exec playwright install --with-deps chromium

      - name: Start app
        run: pnpm dev &

      - name: Wait for app
        run: pnpm wait-on http://localhost:3000

      - name: Run E2E tests
        run: pnpm test:e2e

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

### CI Optimization

| Technique        | Impact                           |
| ---------------- | -------------------------------- |
| Parallel workers | 2-4x faster                      |
| Sharding         | Distribute across machines       |
| Caching browsers | Faster setup                     |
| Headless mode    | Required in CI                   |
| Fail fast        | Stop on first failure (optional) |

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 4 : undefined,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? "github" : "html",
  use: {
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
});
```

---

## 10. Debugging Techniques

### Playwright Trace Viewer

```bash
# Generate trace
pnpm playwright test --trace on

# View trace
pnpm playwright show-trace trace.zip
```

### Debug Mode

```bash
# Run with browser visible + pause
PWDEBUG=1 pnpm playwright test

# Run specific test with UI
pnpm playwright test --ui
```

### Console Logging

```typescript
test("debug example", async ({ page }) => {
  // Log network requests
  page.on("request", (req) => console.log("→", req.url()));
  page.on("response", (res) => console.log("←", res.status(), res.url()));

  // Log console messages
  page.on("console", (msg) => console.log("Console:", msg.text()));

  await page.goto("/");
});
```

---

## 11. Anti-Patterns

| ❌ Don't                    | ✅ Do                             |
| --------------------------- | --------------------------------- |
| Test implementation details | Test user-visible behavior        |
| Use fixed `setTimeout`      | Use explicit waits                |
| Share state between tests   | Isolate each test                 |
| Test everything in E2E      | Use testing pyramid               |
| Skip flaky tests            | Fix root cause                    |
| Hard-coded credentials      | Environment variables, test users |
| Run against production      | Use staging/preview environments  |

---

## 12. Test Data Management

### Strategies

| Strategy         | Use Case                        | Pros/Cons                 |
| ---------------- | ------------------------------- | ------------------------- |
| API seeding      | Create data via API before test | Fast, reliable            |
| Database seeding | Direct DB manipulation          | Complete control, coupled |
| Factory patterns | Generate random valid data      | Flexible, realistic       |
| Fixtures         | Static test data files          | Simple, explicit          |

```typescript
// Factory pattern example
import { faker } from "@faker-js/faker";

const createUser = () => ({
  email: faker.internet.email(),
  name: faker.person.fullName(),
  password: faker.internet.password({ length: 12 }),
});

test("user registration", async ({ page }) => {
  const user = createUser();
  // Use user data in test...
});
```

---

## Related Skills

| Need                     | Skill                   |
| ------------------------ | ----------------------- |
| Unit/integration testing | `testing-patterns`      |
| CI/CD pipelines          | `github-actions`        |
| Performance testing      | `performance-profiling` |
| Accessibility            | `web-design-guidelines` |

---

> **Remember:** A flaky test is worse than no test. Fix it or delete it. Never skip it forever.
