---
name: mobile-design
description: Mobile-first design thinking for iOS and Android apps. Touch interaction, gesture design, platform conventions, responsive layouts, performance patterns. Use when building React Native, Flutter, or native mobile apps.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Mobile Design Patterns

> Design for thumbs, not mice. Every millisecond matters.

---

## Core Principles

1. **Touch-first** - Minimum 44x44pt tap targets, gesture-friendly
2. **Platform-native** - Respect iOS/Android conventions
3. **Performance-obsessed** - 60fps animations, fast startup
4. **Offline-capable** - Design for unreliable networks
5. **Battery-aware** - Minimize background work

---

## 📱 Platform Conventions

### iOS vs Android Differences

| Element          | iOS                   | Android                    |
| ---------------- | --------------------- | -------------------------- |
| **Back gesture** | Swipe from left edge  | System back button/gesture |
| **Navigation**   | Tab bar at bottom     | Bottom nav or drawer       |
| **Actions**      | Right side of nav bar | FAB or overflow menu       |
| **Typography**   | SF Pro                | Roboto                     |
| **Modals**       | Full-screen or sheet  | Dialog or full-screen      |
| **Switches**     | Rounded, green tint   | Material Design style      |

### Font Sizes (Accessibility-Ready)

| Size Category | iOS (pt) | Android (sp) | Use Case          |
| ------------- | -------- | ------------ | ----------------- |
| Caption       | 12       | 12           | Timestamps, hints |
| Body          | 17       | 14-16        | Main content      |
| Title         | 22       | 20           | Section headers   |
| Large Title   | 34       | 24-34        | Screen titles     |

---

## 👆 Touch Interaction

### Tap Target Sizes

| Requirement   | Minimum Size   | Recommended |
| ------------- | -------------- | ----------- |
| **Apple HIG** | 44 x 44 pt     | 48 x 48 pt  |
| **Material**  | 48 x 48 dp     | 48 x 48 dp  |
| **WCAG 2.2**  | 24 x 24 CSS px | 44 x 44     |

### Gesture Patterns

| Gesture        | Common Use                | Consideration             |
| -------------- | ------------------------- | ------------------------- |
| **Tap**        | Primary action            | Provide visual feedback   |
| **Long press** | Context menu, selection   | Show hint after delay     |
| **Swipe**      | Delete, actions, navigate | Show affordance initially |
| **Pull down**  | Refresh                   | Loading indicator         |
| **Pinch**      | Zoom                      | Photos, maps only         |
| **Two-finger** | Advanced actions          | Provide alternative       |

### Thumb Zone Design

```
+-----------------------------------+
|           Hard to reach           |  <- Top 1/4
|-----------------------------------|
|                                   |
|        Okay - may stretch         |  <- Middle
|                                   |
|-----------------------------------|
|      ✅ Natural thumb zone        |  <- Bottom 1/3
|         Primary actions           |
+-----------------------------------+
```

**Rule:** Place primary actions in bottom 1/3 of screen.

---

## 📐 Responsive Layout

### Safe Areas

```
┌─────────────────────────────────────┐
│         Status Bar (Dynamic)        │ <- Respect safe area
├─────────────────────────────────────┤
│                                     │
│           Content Area              │
│     (Scrollable, edge-to-edge)      │
│                                     │
├─────────────────────────────────────┤
│        Home Indicator Area          │ <- Respect safe area
└─────────────────────────────────────┘
```

### Screen Size Breakpoints

| Device Type     | Width Range | Design Approach        |
| --------------- | ----------- | ---------------------- |
| **Small phone** | < 375px     | Single column, compact |
| **Phone**       | 375-428px   | Standard mobile        |
| **Large phone** | 428-768px   | Can add side elements  |
| **Tablet**      | 768px+      | Multi-column possible  |

### Adaptive vs Responsive

| Approach       | When to Use                    |
| -------------- | ------------------------------ |
| **Adaptive**   | Different layouts per platform |
| **Responsive** | Same layout, flexible sizing   |

---

## 🎨 Visual Design

### Spacing System (8pt Grid)

| Token | Value | Use Case           |
| ----- | ----- | ------------------ |
| `xs`  | 4pt   | Icon padding       |
| `sm`  | 8pt   | Tight grouping     |
| `md`  | 16pt  | Standard spacing   |
| `lg`  | 24pt  | Section separation |
| `xl`  | 32pt  | Major sections     |

### Dark Mode Support

```typescript
// Design with semantic colors
const colors = {
  light: {
    background: "#FFFFFF",
    surface: "#F5F5F5",
    text: "#000000",
    textSecondary: "#666666",
  },
  dark: {
    background: "#000000",
    surface: "#1C1C1E",
    text: "#FFFFFF",
    textSecondary: "#8E8E93",
  },
};
```

### Elevation & Shadows

| Level | Use Case          | iOS Shadow | Android Elevation |
| ----- | ----------------- | ---------- | ----------------- |
| 0     | Flat content      | None       | 0dp               |
| 1     | Cards             | Subtle     | 1-2dp             |
| 2     | FAB, Bottom sheet | Medium     | 6-8dp             |
| 3     | Modal, Dialog     | Strong     | 16-24dp           |

---

## ⚡ Performance Patterns

### 60fps Animation Rules

| ❌ Don't                 | ✅ Do                      |
| ------------------------ | -------------------------- |
| Animate width/height     | Use transform: scale()     |
| Animate left/top         | Use transform: translate() |
| Animate during scroll    | Use native driver          |
| Complex animations in JS | Use Reanimated/Worklets    |

### List Performance

| Technique            | When to Use              |
| -------------------- | ------------------------ |
| **FlashList**        | Large lists (100+ items) |
| **Virtualization**   | Any scrollable list      |
| **Item memoization** | Complex item components  |
| **Skeleton loading** | Initial data fetch       |

### Image Optimization

```typescript
// ✅ Optimized image loading
<FastImage
  source={{
    uri: imageUrl,
    priority: FastImage.priority.normal,
    cache: FastImage.cacheControl.immutable,
  }}
  resizeMode={FastImage.resizeMode.cover}
/>
```

---

## 📴 Offline-First Design

### States to Handle

| State       | UI Pattern                      |
| ----------- | ------------------------------- |
| **Loading** | Skeleton or spinner             |
| **Success** | Content display                 |
| **Empty**   | Empty state with action         |
| **Error**   | Error message + retry           |
| **Offline** | Cached data + offline indicator |
| **Syncing** | Subtle sync indicator           |

### Optimistic UI

```
User Action → Immediate UI Update → Background Sync
                                        ↓
                                   If failed → Revert + Error
```

---

## 🔔 Notifications & Feedback

### Haptic Feedback

| Type        | Use Case                   |
| ----------- | -------------------------- |
| **Light**   | UI selection               |
| **Medium**  | Toggle, switch             |
| **Heavy**   | Significant action         |
| **Success** | Task completed             |
| **Warning** | Destructive action confirm |
| **Error**   | Failed action              |

### Loading States

| Duration | Pattern                      |
| -------- | ---------------------------- |
| < 100ms  | No indicator                 |
| 100ms-1s | Inline spinner               |
| 1s-3s    | Progress indicator           |
| > 3s     | Progress + estimated time    |
| Unknown  | Skeleton + content streaming |

---

## ✅ Design Checklist

### Touch & Interaction

- [ ] All tap targets ≥ 44x44pt
- [ ] Primary actions in thumb zone
- [ ] Gesture hints for swipe actions
- [ ] Visual feedback on all touches

### Platform Compliance

- [ ] iOS HIG followed for iOS
- [ ] Material Design for Android
- [ ] Safe areas respected
- [ ] Status bar handled correctly

### Accessibility

- [ ] Text scales with system settings
- [ ] Color contrast ≥ 4.5:1
- [ ] Touch targets accessible
- [ ] Screen reader labels

### Performance

- [ ] 60fps animations
- [ ] Lists virtualized
- [ ] Images optimized
- [ ] Offline state handled

---

## ❌ Anti-Patterns

| ❌ Don't                           | ✅ Do                               |
| ---------------------------------- | ----------------------------------- |
| Small tap targets (< 44pt)         | Minimum 44x44pt                     |
| Important actions at screen top    | Primary actions in thumb zone       |
| Hamburger menu for main navigation | Bottom tab bar                      |
| Custom back button behavior        | Respect platform conventions        |
| Infinite scroll without pagination | Load more or paginate               |
| Text that doesn't scale            | Support Dynamic Type / Font Scaling |

---

## 🔗 Related Skills

| Need                  | Skill                    |
| --------------------- | ------------------------ |
| React Native patterns | `react-native-patterns`  |
| Flutter patterns      | `flutter-patterns`       |
| Accessibility         | `accessibility-patterns` |
| Performance profiling | `performance-profiling`  |

---

> **Remember:** Mobile users are impatient, distracted, and using one hand. Design for the worst conditions: bad network, bright sunlight, walking while texting.
