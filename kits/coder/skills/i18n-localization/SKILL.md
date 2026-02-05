---
name: i18n-localization
description: Internationalization and localization patterns. Use when implementing multi-language support, translation workflows, locale handling, RTL support, or currency/date formatting.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# i18n & Localization Patterns

> Make software work beautifully in every language and culture.

---

## Core Principles

1. **Externalize all strings** - No hardcoded text in components
2. **Use ICU Message Format** - Handle plurals, gender, and complex formatting
3. **Design for translation** - Leave room for text expansion (30-50%)
4. **Test with pseudo-localization** - Catch issues early
5. **Locale is more than language** - Includes date, number, currency formats

---

## 🔧 Framework Selection

| Framework             | Platform     | Best For                    |
| --------------------- | ------------ | --------------------------- |
| **next-intl**         | Next.js      | App Router, RSC support     |
| **react-intl**        | React        | Established, ICU format     |
| **i18next**           | Universal    | Flexible, plugin ecosystem  |
| **vue-i18n**          | Vue          | Vue-native, composition API |
| **expo-localization** | React Native | Mobile apps with Expo       |

### Decision Tree

```
Next.js App Router?
├── Yes → next-intl (best RSC support)
└── No → React SPA?
    ├── Yes → react-intl or i18next
    └── No → Vue?
        ├── Yes → vue-i18n
        └── No → i18next (universal)
```

---

## 📁 Project Structure

```
locales/
├── en/
│   ├── common.json      # Shared strings
│   ├── auth.json        # Auth-related
│   ├── dashboard.json   # Feature-specific
│   └── errors.json      # Error messages
├── vi/
│   ├── common.json
│   ├── auth.json
│   └── ...
└── ja/
    └── ...
```

### Namespace Strategy

| Namespace   | Contents                    |
| ----------- | --------------------------- |
| `common`    | Shared: buttons, labels     |
| `auth`      | Login, register, password   |
| `errors`    | Error messages, validations |
| `[feature]` | Feature-specific strings    |

---

## 🌍 Key Naming Convention

```json
// ✅ GOOD: Descriptive, hierarchical keys
{
  "auth": {
    "login": {
      "title": "Sign In",
      "button": "Sign In",
      "forgotPassword": "Forgot password?"
    }
  }
}

// ❌ BAD: Flat, unclear keys
{
  "login_title": "Sign In",
  "btn1": "Sign In"
}
```

### Naming Rules

| Rule                  | Example                      |
| --------------------- | ---------------------------- |
| **camelCase keys**    | `forgotPassword`             |
| **Nested by feature** | `auth.login.title`           |
| **Semantic naming**   | `submitButton` not `button1` |
| **No hardcoded text** | Even for "OK" or "Cancel"    |

---

## 📝 ICU Message Format

### Plurals

```json
{
  "itemCount": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

### Gender/Select

```json
{
  "greeting": "{gender, select, male {Mr.} female {Ms.} other {}} {name}"
}
```

### Date & Number

```json
{
  "lastUpdated": "Updated {date, date, medium}",
  "price": "Price: {amount, number, ::currency/USD}"
}
```

### Rich Text (react-intl)

```tsx
<FormattedMessage
  id="terms"
  defaultMessage="By signing up, you agree to our <link>Terms of Service</link>"
  values={{
    link: (chunks) => <Link href="/terms">{chunks}</Link>,
  }}
/>
```

---

## 🔄 Translation Workflow

### Development Flow

```
1. Add key to en/[namespace].json
2. Use key in component
3. Export for translators
4. Import translations
5. Review in context
```

### Translation Management

| Tool         | Pricing     | Best For               |
| ------------ | ----------- | ---------------------- |
| **Crowdin**  | Free tier   | Open source, community |
| **Lokalise** | Paid        | Professional teams     |
| **Phrase**   | Paid        | Enterprise             |
| **Tolgee**   | Open source | Self-hosted            |

### Pseudo-localization

```typescript
// Test without real translations
// "Hello" → "[Ħëľľö]" (longer + special chars)

const pseudoLocalize = (str: string) => {
  const map: Record<string, string> = {
    a: "ä",
    e: "ë",
    i: "ï",
    o: "ö",
    u: "ü",
    A: "Ä",
    E: "Ë",
    I: "Ï",
    O: "Ö",
    U: "Ü",
  };
  const converted = str.replace(/[aeiouAEIOU]/g, (c) => map[c] || c);
  return `[${converted}]`;
};
```

---

## 📱 RTL Support

### CSS Approach

```css
/* Use logical properties */
.container {
  /* ❌ Physical */
  margin-left: 16px;
  padding-right: 8px;

  /* ✅ Logical (RTL-aware) */
  margin-inline-start: 16px;
  padding-inline-end: 8px;
}

/* Direction-aware flex */
.row {
  display: flex;
  flex-direction: row; /* Auto-reverses in RTL */
}
```

### Logical Properties Mapping

| Physical           | Logical               |
| ------------------ | --------------------- |
| `left`             | `inline-start`        |
| `right`            | `inline-end`          |
| `top`              | `block-start`         |
| `bottom`           | `block-end`           |
| `margin-left`      | `margin-inline-start` |
| `padding-right`    | `padding-inline-end`  |
| `text-align: left` | `text-align: start`   |

### HTML Direction

```tsx
<html dir={isRTL ? 'rtl' : 'ltr'} lang={locale}>
```

---

## 🔢 Formatting

### Dates

```typescript
// Use Intl.DateTimeFormat
const formatDate = (date: Date, locale: string) => {
  return new Intl.DateTimeFormat(locale, {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
};

// Results:
// en-US: "January 15, 2025"
// vi-VN: "15 tháng 1, 2025"
// ja-JP: "2025年1月15日"
```

### Numbers & Currency

```typescript
const formatCurrency = (amount: number, locale: string, currency: string) => {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
  }).format(amount);
};

// Results for 1234.56:
// en-US, USD: "$1,234.56"
// vi-VN, VND: "1.234,56 ₫"
// ja-JP, JPY: "¥1,235" (no decimals)
```

### Relative Time

```typescript
const formatRelative = (date: Date, locale: string) => {
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  const diff = (date.getTime() - Date.now()) / 1000;

  if (Math.abs(diff) < 60) return rtf.format(Math.round(diff), "second");
  if (Math.abs(diff) < 3600) return rtf.format(Math.round(diff / 60), "minute");
  // ... etc
};
```

---

## ✅ Implementation Checklist

### Setup

- [ ] i18n library installed and configured
- [ ] Default locale defined
- [ ] Locale detection (browser/user preference)
- [ ] Fallback locale strategy

### Content

- [ ] All user-facing strings externalized
- [ ] ICU format for plurals/formatting
- [ ] No string concatenation for sentences
- [ ] Translator context/comments added

### Styling

- [ ] CSS uses logical properties
- [ ] RTL tested with real RTL content
- [ ] Text expansion tested (30-50% longer)
- [ ] Fonts support all target languages

### Testing

- [ ] Pseudo-localization tested
- [ ] All locales render correctly
- [ ] Date/number formats verified
- [ ] RTL layout tested

---

## ❌ Anti-Patterns

| ❌ Don't                          | ✅ Do                                      |
| --------------------------------- | ------------------------------------------ |
| Concatenate strings for sentences | Use ICU message format                     |
| Hardcode "OK", "Cancel", etc.     | Externalize ALL strings                    |
| Use physical CSS properties       | Use logical properties for RTL             |
| Assume text length stays same     | Design for 30-50% expansion                |
| Store locale in localStorage only | Support URL-based locale switching         |
| Use images with embedded text     | Separate text layer or generate per-locale |

---

## 🔗 Related Skills

| Need           | Skill                    |
| -------------- | ------------------------ |
| React patterns | `react-patterns`         |
| API design     | `api-patterns`           |
| Accessibility  | `accessibility-patterns` |
| Testing        | `testing-patterns`       |

---

> **Remember:** Localization is not just translation. It's making users feel the product was made for them, in their language, with their cultural expectations.
