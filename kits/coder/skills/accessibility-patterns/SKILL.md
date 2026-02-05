---
name: accessibility-patterns
description: WCAG compliance, inclusive design, and assistive technology patterns. Use when auditing accessibility, implementing a11y features, or ensuring digital products are accessible to all users.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# Accessibility Patterns - Inclusive Design Excellence

> **Philosophy:** Accessibility is not a feature, it's a fundamental requirement. Design for everyone from the start.

---

## 🎯 Core Principles

| Principle           | Rule                                          |
| ------------------- | --------------------------------------------- |
| **Perceivable**     | Information must be presentable to all senses |
| **Operable**        | UI must be operable by all users              |
| **Understandable**  | Information and UI must be understandable     |
| **Robust**          | Content must work with assistive technologies |
| **Inclusive First** | Build accessibility in, don't bolt it on      |

```
❌ WRONG: Build first, add accessibility later
✅ CORRECT: Consider accessibility in every design decision
```

---

## 📊 WCAG Compliance Levels

| Level   | Description                     | Legal Requirement?      |
| ------- | ------------------------------- | ----------------------- |
| **A**   | Minimum accessibility           | Often required          |
| **AA**  | Standard for most organizations | Most common requirement |
| **AAA** | Highest accessibility standard  | Rarely fully achievable |

> **Target AA for most projects.** It covers the most critical accessibility needs.

---

## 🎨 Visual Accessibility

### Color Contrast

| Element            | AA Ratio | AAA Ratio |
| ------------------ | -------- | --------- |
| Normal text        | 4.5:1    | 7:1       |
| Large text (18px+) | 3:1      | 4.5:1     |
| UI components      | 3:1      | 3:1       |
| Focus indicators   | 3:1      | 3:1       |

```css
/* ✅ GOOD - Sufficient contrast */
.text-primary {
  color: #1a1a1a; /* Contrast: 16.1:1 on white */
  background: #ffffff;
}

/* ❌ BAD - Insufficient contrast */
.text-muted {
  color: #999999; /* Contrast: 2.8:1 - FAILS */
  background: #ffffff;
}
```

### Color Independence

```html
<!-- ❌ BAD - Color only indicates error -->
<input class="error-red" />

<!-- ✅ GOOD - Multiple indicators -->
<input class="error" aria-invalid="true" />
<span class="error-icon">⚠️</span>
<span class="error-message">Email is required</span>
```

---

## ⌨️ Keyboard Accessibility

### Focus Management

| Rule                        | Implementation                    |
| --------------------------- | --------------------------------- |
| All interactive elements    | Must be focusable via Tab         |
| Logical focus order         | Match visual reading order        |
| Visible focus indicators    | Never `outline: none` without alt |
| Focus trapping in modals    | Tab loops within modal            |
| Return focus on modal close | Focus returns to trigger element  |

### Focus Indicator Pattern

```css
/* ✅ GOOD - Visible, accessible focus */
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove default only if custom focus exists */
button:focus:not(:focus-visible) {
  outline: none;
}
```

### Skip Links

```html
<body>
  <a href="#main-content" class="skip-link"> Skip to main content </a>
  <!-- Navigation -->
  <main id="main-content">
    <!-- Content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 10px;
  top: 10px;
  z-index: 9999;
}
```

---

## 🔊 Screen Reader Support

### Semantic HTML

| Use                 | Not                     |
| ------------------- | ----------------------- |
| `<button>`          | `<div onclick>`         |
| `<a href>`          | `<span onclick>`        |
| `<nav>`             | `<div class="nav">`     |
| `<main>`            | `<div class="main">`    |
| `<header>/<footer>` | `<div class="header">`  |
| `<article>`         | `<div class="article">` |

### ARIA Usage Guidelines

```html
<!-- Rule 1: Don't use ARIA if you can use HTML -->
<!-- ❌ BAD -->
<div role="button" tabindex="0">Click me</div>

<!-- ✅ GOOD -->
<button>Click me</button>

<!-- Rule 2: Use ARIA to enhance, not replace -->
<button aria-label="Close dialog" aria-describedby="dialog-desc">
  <svg><!-- X icon --></svg>
</button>
<p id="dialog-desc">This will close the settings dialog</p>
```

### Live Regions

```html
<!-- Announce dynamic content changes -->
<div role="status" aria-live="polite">3 search results found</div>

<div role="alert" aria-live="assertive">Error: Unable to save changes</div>
```

| aria-live Value | Use Case                            |
| --------------- | ----------------------------------- |
| `polite`        | Non-urgent updates (search results) |
| `assertive`     | Urgent (errors, alerts)             |
| `off`           | Don't announce                      |

---

## 📝 Forms Accessibility

### Labels and Descriptions

```html
<!-- ✅ GOOD - Properly labeled -->
<label for="email">Email Address</label>
<input
  type="email"
  id="email"
  aria-describedby="email-hint email-error"
  aria-invalid="false"
  required
/>
<span id="email-hint">We'll never share your email</span>
<span id="email-error" role="alert"></span>
```

### Error Handling

```html
<!-- Error state -->
<label for="password">Password</label>
<input
  type="password"
  id="password"
  aria-invalid="true"
  aria-describedby="password-error"
/>
<span id="password-error" role="alert">
  Password must be at least 8 characters
</span>
```

### Form Validation Pattern

| When      | What                                    |
| --------- | --------------------------------------- |
| On submit | Announce error count, focus first error |
| On blur   | Validate individual field               |
| On fix    | Clear error, don't re-announce success  |

---

## 🖼️ Images and Media

### Alt Text Guidelines

| Image Type        | Alt Text                       |
| ----------------- | ------------------------------ |
| Informative       | Describe content and purpose   |
| Decorative        | `alt=""` (empty)               |
| Functional (link) | Describe destination/action    |
| Complex (chart)   | Brief alt + longer description |

```html
<!-- Informative -->
<img src="chart.png" alt="Sales grew 25% from Q1 to Q2" />

<!-- Decorative -->
<img src="decoration.png" alt="" role="presentation" />

<!-- Complex -->
<figure>
  <img src="complex-chart.png" alt="Revenue breakdown by region" />
  <figcaption>North America leads with 45%, Europe at 30%...</figcaption>
</figure>
```

### Video Accessibility

| Requirement     | Solution                     |
| --------------- | ---------------------------- |
| Deaf users      | Captions (synchronized text) |
| Blind users     | Audio descriptions           |
| Deafblind users | Transcript                   |
| Seizure safety  | No flashing >3 times/second  |

---

## 📱 Touch and Mobile

### Touch Target Size

| Standard        | Minimum Size |
| --------------- | ------------ |
| WCAG 2.2 AA     | 24x24px      |
| WCAG 2.2 AAA    | 44x44px      |
| Apple HIG       | 44x44pt      |
| Material Design | 48x48dp      |

### Spacing Between Targets

```css
.button-group button {
  min-width: 44px;
  min-height: 44px;
  margin: 8px; /* Prevent accidental taps */
}
```

---

## 🧪 Testing Tools

### Automated Testing

| Tool             | Use Case                            |
| ---------------- | ----------------------------------- |
| **axe DevTools** | Browser extension, CI integration   |
| **Lighthouse**   | Chrome DevTools, performance + a11y |
| **WAVE**         | Browser extension, visual feedback  |
| **pa11y**        | CLI tool for CI/CD                  |
| **jest-axe**     | Unit test accessibility assertions  |

### Manual Testing

| Test           | How                                  |
| -------------- | ------------------------------------ |
| Keyboard only  | Unplug mouse, navigate with Tab      |
| Screen reader  | VoiceOver (Mac), NVDA/JAWS (Windows) |
| Zoom 200%      | Browser zoom, check layout           |
| Color contrast | Use contrast checker tools           |
| Motion reduced | Test `prefers-reduced-motion`        |

---

## 🚨 Anti-Patterns

| ❌ Don't                         | ✅ Do                               |
| -------------------------------- | ----------------------------------- |
| `outline: none` without alt      | Custom focus with adequate contrast |
| Color-only indicators            | Multiple visual cues                |
| Generic link text ("click here") | Descriptive link text               |
| Auto-playing media               | User-controlled playback            |
| Time limits without extension    | Allow time extension or removal     |
| Mouse-only interactions          | Keyboard equivalent for all actions |
| Missing form labels              | Associated labels or aria-label     |
| Small touch targets              | Minimum 44x44 touch targets         |

---

## ✅ Accessibility Checklist

### Perceivable

- [ ] All images have appropriate alt text
- [ ] Color contrast meets 4.5:1 for text
- [ ] Color is not the only way to convey info
- [ ] Captions for video content
- [ ] Text can be resized to 200% without loss

### Operable

- [ ] All functionality available via keyboard
- [ ] Visible focus indicators on all elements
- [ ] Skip links for main content
- [ ] No keyboard traps
- [ ] Adequate time for timed content
- [ ] Touch targets are 44x44 minimum

### Understandable

- [ ] Language attribute on `<html>`
- [ ] Consistent navigation pattern
- [ ] Form errors are clearly explained
- [ ] Labels on all form fields
- [ ] Instructions before complex forms

### Robust

- [ ] Valid HTML
- [ ] Semantic elements used correctly
- [ ] ARIA used only when necessary
- [ ] Works with screen readers

---

## 🔗 Related Skills

| Need               | Skill                   |
| ------------------ | ----------------------- |
| SEO implementation | `seo-patterns`          |
| Frontend design    | `frontend-design`       |
| UX research        | UX researcher agent     |
| Performance        | `performance-profiling` |

---

> **Remember:** Every accessibility barrier you remove opens your product to more people. 15-20% of the global population has some form of disability.
