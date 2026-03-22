---
name: seo-patterns
description: SEO fundamentals including E-E-A-T, Core Web Vitals, technical SEO, and content optimization. Use when optimizing pages for search engines, improving rankings, or setting up SEO infrastructure.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# SEO Patterns - Sustainable Search Visibility

## ⚡ Quick Reference

- **Core Web Vitals**: LCP < 2.5s · INP < 200ms · CLS < 0.1 · Monitor with Search Console
- **HTML structure**: 1 `<h1>` per page · logical `<h2>→<h6>` · semantic tags (`<article>`, `<nav>`, `<main>`)
- **Meta tags**: Unique `<title>` (50-60 chars) · `<meta description>` (150-160 chars) · `<canonical>`
- **Images**: `alt` on all images · Next-gen format (WebP/AVIF) · `width` + `height` to prevent CLS  
- **Structured data**: JSON-LD format · `Organization`, `Product`, `Article` schemas per content type
- **Tech SEO**: `robots.txt` · `sitemap.xml` · HTTPS · Mobile-first · No render-blocking resources

---


---

## 🎯 Core Principles

| Principle             | Rule                                              |
| --------------------- | ------------------------------------------------- |
| **Content First**     | Quality content is the foundation of all SEO      |
| **Technical Clarity** | Search engines must access, understand, and index |
| **User Focus**        | Optimize for users, not search engines            |
| **E-E-A-T**           | Experience, Expertise, Authoritativeness, Trust   |
| **Patience**          | SEO is a long-term investment, not quick wins     |

```
❌ WRONG: Keyword stuffing, link farms, AI spam
✅ CORRECT: Useful content, technical excellence, earned authority
```

---

## 📊 E-E-A-T Framework

E-E-A-T is NOT a direct ranking factor. It's a framework for evaluating content quality.

| Dimension             | What It Represents                 | Signals                             |
| --------------------- | ---------------------------------- | ----------------------------------- |
| **Experience**        | First-hand, real-world involvement | Original examples, lived experience |
| **Expertise**         | Subject-matter competence          | Credentials, depth, accuracy        |
| **Authoritativeness** | Recognition by others              | Mentions, citations, links          |
| **Trustworthiness**   | Reliability and safety             | HTTPS, transparency, accuracy       |

### YMYL (Your Money or Your Life)

High E-E-A-T requirements for content affecting:

- Health and safety
- Financial decisions
- Legal information
- News and current events

---

## ⚡ Core Web Vitals

| Metric  | Target  | What It Measures          |
| ------- | ------- | ------------------------- |
| **LCP** | < 2.5s  | Largest Contentful Paint  |
| **INP** | < 200ms | Interaction to Next Paint |
| **CLS** | < 0.1   | Cumulative Layout Shift   |

### Improvement Strategies

| Metric | Quick Wins                                    |
| ------ | --------------------------------------------- |
| LCP    | Optimize images, preload critical resources   |
| INP    | Reduce JavaScript, defer non-critical scripts |
| CLS    | Set explicit dimensions on images/embeds      |

---

## 🔧 Technical SEO Essentials

### Crawl & Index Control

| Element         | Purpose                | Implementation                  |
| --------------- | ---------------------- | ------------------------------- |
| **robots.txt**  | Control crawl access   | Block /admin/, /api/, etc.      |
| **XML Sitemap** | Help discovery         | Submit to Search Console        |
| **Canonical**   | Consolidate duplicates | `<link rel="canonical" />`      |
| **Hreflang**    | Multi-language sites   | Define language/region versions |
| **HTTPS**       | Security and trust     | Valid SSL certificate           |

### Robots.txt Example

```txt
User-agent: *
Disallow: /admin/
Disallow: /api/
Disallow: /private/
Allow: /api/public/

Sitemap: https://example.com/sitemap.xml
```

### Meta Tags Priorities

| Tag                 | SEO Impact | Best Practice                           |
| ------------------- | ---------- | --------------------------------------- |
| `<title>`           | High       | Unique, 50-60 chars, keyword near start |
| `meta description`  | Medium     | Compelling, 150-160 chars, for CTR      |
| `<h1>`              | Medium     | One per page, main topic                |
| `meta robots`       | High       | Control indexing per page               |
| `og:*`, `twitter:*` | Low        | Social sharing, not ranking             |

---

## 📝 Content SEO

### On-Page Elements

| Element              | Principle                       |
| -------------------- | ------------------------------- |
| **Title Tag**        | Clear topic + intent            |
| **Meta Description** | Click relevance, not ranking    |
| **H1**               | Page's primary subject          |
| **Headings (H2-H6)** | Logical structure               |
| **Alt Text**         | Accessibility and context       |
| **Internal Links**   | Topic clusters, related content |

### Content Quality Signals

| Dimension       | What Search Engines Look For |
| --------------- | ---------------------------- |
| **Depth**       | Fully answers the query      |
| **Originality** | Adds unique value            |
| **Accuracy**    | Factually correct            |
| **Clarity**     | Easy to understand           |
| **Usefulness**  | Satisfies user intent        |
| **Freshness**   | Updated when relevant        |

---

## 🏗️ Structured Data (Schema)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Build SEO-Friendly React Apps",
  "author": {
    "@type": "Person",
    "name": "John Doe",
    "url": "https://example.com/authors/john"
  },
  "datePublished": "2025-01-15",
  "dateModified": "2025-02-01",
  "publisher": {
    "@type": "Organization",
    "name": "Example Inc",
    "logo": "https://example.com/logo.png"
  }
}
```

### Common Schema Types

| Type               | Use Case                        |
| ------------------ | ------------------------------- |
| **Article**        | Blog posts, news articles       |
| **Product**        | E-commerce product pages        |
| **FAQPage**        | FAQ sections                    |
| **BreadcrumbList** | Site navigation structure       |
| **Organization**   | Company/brand identity          |
| **LocalBusiness**  | Local businesses with locations |
| **HowTo**          | Step-by-step guides             |

---

## 🤖 AI Content Guidelines

Search engines evaluate **output quality**, not authorship method.

### Effective Use

- AI as drafting or research assistant
- Human review for accuracy and clarity
- Original insights and synthesis
- Clear accountability

### Risky Use

- Publishing unedited AI output
- Factual errors or hallucinations
- Thin or duplicated content
- Keyword-driven text with no value

---

## 📈 SEO Measurement

| Area            | Key Metrics                     |
| --------------- | ------------------------------- |
| **Visibility**  | Indexed pages, impressions      |
| **Rankings**    | Position changes, serp features |
| **Traffic**     | Organic sessions, new pages     |
| **Engagement**  | CTR, dwell time, bounce rate    |
| **Conversions** | Organic-attributed conversions  |
| **Technical**   | Core Web Vitals, crawl errors   |

### Essential Tools

- Google Search Console (rankings, indexing)
- Google Analytics 4 (traffic, behavior)
- Lighthouse / PageSpeed Insights (Core Web Vitals)
- Screaming Frog (technical audits)

---

## 🚨 SEO Anti-Patterns

| ❌ Don't                   | ✅ Do                              |
| -------------------------- | ---------------------------------- |
| Keyword stuffing           | Natural language, topic coverage   |
| Duplicate content          | Canonical tags, unique pages       |
| Hidden text/links          | Visible, accessible content        |
| Low-quality link building  | Earn links through quality content |
| Ignore mobile              | Mobile-first design                |
| Block CSS/JS from crawlers | Allow full page rendering          |
| Slow page load             | Optimize Core Web Vitals           |
| Missing alt text           | Descriptive alt for all images     |

---

## ✅ SEO Checklist

### Page-Level

- [ ] Unique, descriptive `<title>` (50-60 chars)
- [ ] Compelling meta description (150-160 chars)
- [ ] One `<h1>` per page
- [ ] Logical heading hierarchy (H2, H3, etc.)
- [ ] Alt text on all images
- [ ] Internal links to related content
- [ ] Canonical tag present
- [ ] Schema markup where applicable

### Site-Level

- [ ] HTTPS enabled
- [ ] XML sitemap submitted
- [ ] robots.txt configured
- [ ] Mobile-friendly design
- [ ] Core Web Vitals passing
- [ ] No broken links (4xx/5xx)
- [ ] Clean URL structure
- [ ] Hreflang for multi-language

---

## 🔗 Related Skills

| Need                     | Skill                     |
| ------------------------ | ------------------------- |
| Performance optimization | `performance-profiling`   |
| Accessibility            | `accessibility-patterns`  |
| React/Next.js SSR        | `react-patterns`          |
| Content structure        | `documentation-templates` |

---

> **Key Principle:** Sustainable SEO is built on useful content, technical clarity, and trust over time. There are no permanent shortcuts.
