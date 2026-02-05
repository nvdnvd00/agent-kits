---
name: tailwind-patterns
description: Tailwind CSS v4 patterns and best practices. Utility-first CSS, component patterns, responsive design, dark mode, and design system architecture. Use when styling web applications with Tailwind.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Tailwind CSS Patterns

> Utility-first CSS that actually scales.

---

## Core Principles

1. **Utility-first** - Compose classes, don't write custom CSS
2. **Extract components** - When patterns repeat 3+ times
3. **Design tokens first** - Configure theme before building
4. **Responsive mobile-first** - Start small, scale up
5. **Dark mode native** - Design both themes from the start

---

## 🎨 Tailwind v4 Changes

### CSS-First Configuration (v4)

```css
/* app.css - v4 uses CSS for configuration */
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.1 180);

  /* Spacing */
  --spacing-18: 4.5rem;

  /* Font */
  --font-display: "Cal Sans", sans-serif;

  /* Custom utilities */
  --container-3xl: 1920px;
}
```

### v3 vs v4 Comparison

| Feature           | v3 (tailwind.config.js) | v4 (CSS @theme)           |
| ----------------- | ----------------------- | ------------------------- |
| Configuration     | JavaScript              | CSS with `@theme`         |
| Custom colors     | `theme.extend.colors`   | `--color-*` CSS variables |
| Plugins           | JS plugins              | CSS `@plugin` directive   |
| JIT               | Opt-in                  | Default                   |
| Container queries | Plugin needed           | Native `@container`       |

---

## 📐 Design Token Architecture

### Color System

```css
@theme {
  /* Semantic colors (recommended) */
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.1 0 0);
  --color-muted: oklch(0.96 0.01 250);
  --color-muted-foreground: oklch(0.55 0.02 250);

  --color-primary: oklch(0.6 0.2 250);
  --color-primary-foreground: oklch(1 0 0);

  --color-destructive: oklch(0.6 0.2 25);
  --color-destructive-foreground: oklch(1 0 0);

  --color-border: oklch(0.9 0.01 250);
  --color-ring: oklch(0.7 0.15 250);
}
```

### Typography Scale

```css
@theme {
  --font-sans: "Inter Variable", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
}
```

### Spacing System

```css
@theme {
  /* Use 4px base (0.25rem) */
  --spacing-0: 0;
  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */
  --spacing-12: 3rem; /* 48px */
  --spacing-16: 4rem; /* 64px */
}
```

---

## 🧩 Component Patterns

### Button Component

```tsx
// Base button with variants
const buttonVariants = {
  base: "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
      outline: "border border-border bg-background hover:bg-muted",
      ghost: "hover:bg-muted",
      destructive:
        "bg-destructive text-destructive-foreground hover:bg-destructive/90",
    },
    size: {
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4",
      lg: "h-12 px-6 text-lg",
      icon: "h-10 w-10",
    },
  },
  defaultVariants: {
    variant: "default",
    size: "md",
  },
};
```

### Card Pattern

```tsx
<div className="rounded-xl border border-border bg-card p-6 shadow-sm">
  <div className="flex items-center gap-4 mb-4">
    <div className="h-12 w-12 rounded-full bg-primary/10" />
    <div>
      <h3 className="font-semibold text-foreground">Title</h3>
      <p className="text-sm text-muted-foreground">Subtitle</p>
    </div>
  </div>
  <p className="text-foreground/80">Content goes here...</p>
</div>
```

### Input Pattern

```tsx
<input
  className="
    flex h-10 w-full rounded-lg border border-border 
    bg-background px-3 py-2 text-foreground
    placeholder:text-muted-foreground
    focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent
    disabled:cursor-not-allowed disabled:opacity-50
  "
  placeholder="Enter text..."
/>
```

---

## 📱 Responsive Design

### Mobile-First Breakpoints

| Prefix | Min-width | Target Devices |
| ------ | --------- | -------------- |
| (none) | 0         | Mobile default |
| `sm`   | 640px     | Large phones   |
| `md`   | 768px     | Tablets        |
| `lg`   | 1024px    | Laptops        |
| `xl`   | 1280px    | Desktops       |
| `2xl`  | 1536px    | Large screens  |

### Responsive Pattern

```tsx
// Mobile-first: start with mobile, override for larger
<div
  className="
  grid grid-cols-1 gap-4
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
"
>
  {items.map((item) => (
    <Card key={item.id} />
  ))}
</div>
```

### Container Queries (v4)

```tsx
// Parent defines container
<div className="@container">
  {/* Child responds to container, not viewport */}
  <div className="@sm:flex @md:grid @lg:grid-cols-2">
    Content adapts to container width
  </div>
</div>
```

---

## 🌙 Dark Mode

### Class Strategy (Recommended)

```tsx
// HTML element has 'dark' class
<html className="dark">

// Components use dark: prefix
<div className="bg-white dark:bg-slate-900">
  <p className="text-slate-900 dark:text-white">
    Adapts to theme
  </p>
</div>
```

### Using CSS Variables (Better)

```css
/* Define in @theme - automatically works with dark mode */
@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.1 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: oklch(0.1 0 0);
    --color-foreground: oklch(0.95 0 0);
  }
}
```

```tsx
// Components just use semantic colors - no dark: needed
<div className="bg-background text-foreground">Works in both themes!</div>
```

---

## ⚡ Performance Patterns

### Avoid These

```tsx
// ❌ Dynamic classes (can't be tree-shaken)
<div className={`text-${color}-500`}>

// ❌ Conditional with many variants
<div className={isLarge ? 'text-xl p-8' : 'text-sm p-4'}>

// ✅ Use complete class names
const sizeClasses = {
  sm: 'text-sm p-4',
  lg: 'text-xl p-8',
};
<div className={sizeClasses[size]}>
```

### Class Merging (cn utility)

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage - later classes override earlier
<button className={cn(
  "px-4 py-2 bg-blue-500",
  isActive && "bg-green-500",
  className // Allow override from props
)} />
```

---

## 🎯 Common Patterns

### Flexbox Center

```tsx
<div className="flex items-center justify-center h-screen">
  Centered content
</div>
```

### Truncate Text

```tsx
<p className="truncate">Long text that will truncate...</p>
<p className="line-clamp-2">Multi-line text that clips after 2 lines...</p>
```

### Aspect Ratio

```tsx
<div className="aspect-video">16:9 container</div>
<div className="aspect-square">1:1 container</div>
```

### Glass Effect

```tsx
<div className="backdrop-blur-md bg-white/70 dark:bg-black/70">
  Glassmorphism effect
</div>
```

### Gradient Text

```tsx
<h1 className="bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">
  Gradient Text
</h1>
```

---

## ✅ Checklist

### Setup

- [ ] Tailwind v4 installed correctly
- [ ] CSS `@theme` configured
- [ ] Design tokens defined
- [ ] `cn()` utility created

### Components

- [ ] Using semantic color names
- [ ] Mobile-first responsive
- [ ] Dark mode supported
- [ ] Accessible focus states

### Performance

- [ ] No dynamic class construction
- [ ] Classes are complete strings
- [ ] Unused styles tree-shaken

---

## ❌ Anti-Patterns

| ❌ Don't                         | ✅ Do                            |
| -------------------------------- | -------------------------------- |
| `text-${color}-500` dynamic      | Map to complete class strings    |
| Inline arbitrary values `[23px]` | Define in `@theme` and use token |
| 20+ classes per element          | Extract component or @apply      |
| `dark:` on every element         | Use CSS variables for colors     |
| Skip focus states                | Include `focus-visible:ring-*`   |

---

## 🔗 Related Skills

| Need                     | Skill                    |
| ------------------------ | ------------------------ |
| React component patterns | `react-patterns`         |
| Accessibility            | `accessibility-patterns` |
| Design principles        | `frontend-design`        |
| Performance              | `performance-profiling`  |

---

> **Remember:** Tailwind's power is in its constraints. Stick to the design system, use semantic colors, and resist the urge to add arbitrary values.
