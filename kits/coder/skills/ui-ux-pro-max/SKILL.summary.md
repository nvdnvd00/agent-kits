---
name: ui-ux-pro-max
summary: true
description: "UI/UX design intelligence. 50 styles, 97 palettes, 57 font pairings, 9 stacks. For planning/quick ref — load SKILL.md for full patterns."
---

# UI/UX Pro Max — Summary

> ⚡ Quick ref. Load full `SKILL.md` when implementing specific UI patterns.

## When to Apply
Designing UI, choosing colors/typography, reviewing UX, building landing pages/dashboards.

## Priority Rules
1. **Accessibility** (CRITICAL): 4.5:1 contrast, focus rings, alt text, aria-labels, keyboard nav
2. **Touch & Interaction** (CRITICAL): 44x44px targets, loading states, error feedback, cursor-pointer
3. **Performance** (HIGH): WebP/srcset, prefers-reduced-motion, no content jumping
4. **Layout** (HIGH): viewport meta, min 16px body, no horizontal scroll, z-index scale
5. **Typography/Color** (MEDIUM): 1.5-1.75 line-height, 65-75 char lines, font pairing
6. **Animation** (MEDIUM): 150-300ms, transform/opacity only, skeleton screens
7. **Style** (MEDIUM): consistent style across pages, SVG icons not emojis

## Workflow
```
1. Analyze: product type · style keywords · stack (default: html-tailwind)
2. python3 .agent/skills/ui-ux-pro-max/scripts/search.py "<keywords>" --design-system
3. Supplement: --domain style|chart|ux|typography as needed
4. python3 .agent/skills/ui-ux-pro-max/scripts/search.py "<keywords>" --stack html-tailwind
```

## Common Mistakes
- Emojis as icons → use Heroicons/Lucide SVG
- Glass cards in light mode → use bg-white/80+ not bg-white/10
- No cursor-pointer on clickable cards
- Content behind fixed navbars

> Load full SKILL.md for: complete domain reference, style catalog, pre-delivery checklist
