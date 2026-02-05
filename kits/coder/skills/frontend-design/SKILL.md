---
name: frontend-design
description: Design thinking for web UI. Color theory, typography, spacing, layouts, micro-interactions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Design Patterns

> Design is how it works.

---

## Core Principles

1. **Hierarchy matters** - Guide the eye with visual weight
2. **Consistency builds trust** - Same patterns, same meanings
3. **Space is content** - Whitespace is intentional
4. **Motion has meaning** - Animate purposefully

---

## 🎨 Color System

### Palette Structure

| Role      | Use Case                    |
| --------- | --------------------------- |
| Primary   | CTAs, links, brand elements |
| Secondary | Supporting elements         |
| Neutral   | Text, borders, backgrounds  |
| Success   | Confirmations, completed    |
| Warning   | Caution, pending            |
| Error     | Errors, destructive actions |

### Contrast (WCAG)

| Level | Normal Text | Large Text |
| ----- | ----------- | ---------- |
| AA    | 4.5:1       | 3:1        |
| AAA   | 7:1         | 4.5:1      |

---

## 📝 Typography

### Type Scale

| Name | Size     | Line Height | Use Case        |
| ---- | -------- | ----------- | --------------- |
| xs   | 0.75rem  | 1.5         | Labels          |
| sm   | 0.875rem | 1.5         | Secondary text  |
| base | 1rem     | 1.6         | Body text       |
| lg   | 1.125rem | 1.5         | Lead paragraphs |
| xl   | 1.25rem  | 1.4         | Card titles     |
| 2xl  | 1.5rem   | 1.3         | Section headers |
| 3xl  | 1.875rem | 1.2         | Page titles     |

### Rules

- Body line length: 60-75 characters
- Body line height: 1.5-1.7
- Max 2 font families

---

## 📐 Spacing (8pt Grid)

| Token | Value | Use Case         |
| ----- | ----- | ---------------- |
| 1     | 4px   | Tight grouping   |
| 2     | 8px   | Related items    |
| 4     | 16px  | Standard spacing |
| 6     | 24px  | Section gaps     |
| 8     | 32px  | Major sections   |
| 12    | 48px  | Page sections    |

---

## 📊 Layout Patterns

| Pattern    | Description                   |
| ---------- | ----------------------------- |
| Holy Grail | Header, footer, 3-col middle  |
| Sidebar    | Fixed sidebar + fluid content |
| Dashboard  | Sidebar nav + header + grid   |
| Cards      | Auto-filling responsive grid  |

---

## ✨ Micro-Interactions

| Principle | Implementation                   |
| --------- | -------------------------------- |
| Duration  | 150-300ms for interactions       |
| Easing    | ease-out for enter, ease-in exit |

---

## 🧩 Button Hierarchy

| Type        | Use Case       | Style             |
| ----------- | -------------- | ----------------- |
| Primary     | Main action    | Filled, brand     |
| Secondary   | Supporting     | Outlined          |
| Tertiary    | Less important | Text only         |
| Destructive | Delete         | Red, with confirm |

---

## ❌ Anti-Patterns

| Don't                    | Do                   |
| ------------------------ | -------------------- |
| Low contrast text        | WCAG AA minimum      |
| More than 3 fonts        | 1-2 fonts            |
| Inconsistent spacing     | Use spacing tokens   |
| Animation for decoration | Animate purposefully |

---

## 🔗 Related Skills

- `ui-ux-pro-max` - Design system generator (search + recommend)
- `react-patterns` - React components
- `tailwind-patterns` - Tailwind CSS
- `accessibility-patterns` - Accessibility
- `mobile-design` - Mobile design
