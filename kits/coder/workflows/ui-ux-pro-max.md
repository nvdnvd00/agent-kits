---
description: Plan and implement UI/UX with design intelligence. Generates design system, style guide, and implementation checklist.
---

# /ui-ux-pro-max Workflow

> UI/UX Design Intelligence workflow with BM25-powered style matching.

## When to Use

- Designing new landing pages, dashboards, or web apps
- Choosing color palettes, typography, and style
- Building UI with specific style requirements
- Need design system recommendations for a product type

## Workflow Steps

### Phase 1: Requirements Analysis

1. **Extract from user request:**
   - Product type (SaaS, e-commerce, portfolio, dashboard, etc.)
   - Style keywords (minimal, playful, professional, dark mode, etc.)
   - Industry (healthcare, fintech, gaming, education, etc.)
   - Tech stack (React, Vue, Next.js - default to `html-tailwind`)

### Phase 2: Generate Design System (REQUIRED)

2. **Run design system generator:**

```bash
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

**Example:**

```bash
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Serenity Spa"
```

### Phase 3: Detailed Searches (Optional)

3. **Get additional details if needed:**

| Need                  | Command                                 |
| --------------------- | --------------------------------------- |
| More style options    | `--domain style "glassmorphism dark"`   |
| Chart recommendations | `--domain chart "real-time dashboard"`  |
| UX guidelines         | `--domain ux "animation accessibility"` |
| Alternative fonts     | `--domain typography "elegant luxury"`  |
| Landing structure     | `--domain landing "hero social-proof"`  |

### Phase 4: Stack Guidelines

4. **Get stack-specific best practices:**

```bash
python3 .agent/skills/ui-ux-pro-max/scripts/search.py "<keywords>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

### Phase 5: Implementation

5. **Build with design system:**
   - Apply colors from design system
   - Use recommended typography (Google Fonts)
   - Follow layout pattern
   - Implement key effects
   - Avoid anti-patterns

### Phase 6: Pre-Delivery Checklist

6. **Verify before delivery:**
   - [ ] No emojis as icons (use SVG: Heroicons/Lucide)
   - [ ] cursor-pointer on all clickable elements
   - [ ] Hover states with smooth transitions (150-300ms)
   - [ ] Light mode: text contrast 4.5:1 minimum
   - [ ] Focus states visible for keyboard nav
   - [ ] prefers-reduced-motion respected
   - [ ] Responsive: 375px, 768px, 1024px, 1440px

## Available Domains

| Domain       | Use For                              |
| ------------ | ------------------------------------ |
| `product`    | Product type recommendations         |
| `style`      | UI styles, colors, effects           |
| `typography` | Font pairings, Google Fonts          |
| `color`      | Color palettes by product type       |
| `landing`    | Page structure, CTA strategies       |
| `chart`      | Chart types, library recommendations |
| `ux`         | Best practices, anti-patterns        |
| `react`      | React/Next.js performance            |
| `web`        | Web interface guidelines             |

## Critical Rules

1. **Always start with `--design-system`** for comprehensive recommendations
2. **Default stack is `html-tailwind`** unless user specifies otherwise
3. **Follow Pre-Delivery Checklist** before delivering any UI code
4. **Avoid Purple Ban** - Never use purple/violet as primary unless requested
5. **No emojis as icons** - Always use SVG icons (Heroicons, Lucide)

## Exit Conditions

- ✅ Design system generated and applied
- ✅ UI implementation matches design system
- ✅ Pre-delivery checklist passed
- ✅ Responsive design verified
