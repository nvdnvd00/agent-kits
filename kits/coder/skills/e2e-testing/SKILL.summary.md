---
name: e2e-testing
summary: true
description: "E2E testing with Playwright and Cypress. For planning/quick ref — load SKILL.md for full code examples."
---

# E2E Testing Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when writing Playwright/Cypress test code.

## Tool Selection
- **New projects (2025+)**: Playwright (multi-browser, faster, better DX)
- **Existing Cypress projects**: Stay on Cypress
- **Avoid**: Selenium

## When to Use E2E
✅ Login flows · Payment/checkout · Critical user journeys · Cross-browser · Visual regression

❌ Unit logic · Component behavior · API contracts → use lower-level tests

## Selector Priority (always)
1. `getByRole('button', {name: 'Submit'})` — accessibility-first
2. `getByLabel('Email')`
3. `getByPlaceholder('...')`
4. `getByText('...')`
5. `getByTestId('submit-btn')` — last resort

**NEVER**: CSS class · XPath · nth-child (all brittle)

## Reliability Rules
- Never use `setTimeout` / `sleep()` → use `await expect(locator).toBeVisible()`
- Playwright auto-waits on interactions — trust it
- Isolate each test (beforeEach/afterEach clean up)
- Auth: reuse `storageState` (login once, reuse cookies)

## CI Config
- `fullyParallel: true` · `workers: 4` in CI
- `retries: 2` in CI · `trace: "on-first-retry"`
- Upload `playwright-report/` on failure

## Anti-Patterns
- Fixed `setTimeout` → use explicit waits
- Shared state between tests → isolate each test
- Testing everything in E2E → use testing pyramid
- Skip flaky tests → fix or delete them

> Load full SKILL.md for: Page Object Model code, auth setup pattern, visual regression, mock API, GitHub Actions YAML, test data factory
