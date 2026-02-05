#!/usr/bin/env python3
"""
SEO Checker - SEO and GEO audit for AGT-Kit
============================================

Checks pages for SEO best practices and AI citation readiness (GEO).

Usage:
    python3 .agent/skills/seo-patterns/scripts/seo_checker.py <project_path>

Checks:
    - JSON-LD structured data
    - Meta tags (title, description, og:*)
    - Heading structure (H1, H2)
    - E-E-A-T signals (author, dates)
    - FAQ sections (AI-citable)
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'venv', 'test', 'tests'}


def find_pages(project_path: Path) -> List[Path]:
    """Find public-facing web pages."""
    patterns = ['**/*.html', '**/pages/**/*.tsx', '**/app/**/*.tsx', '**/app/**/*.jsx']
    
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if not any(skip in f.parts for skip in SKIP_DIRS):
                # Filter to likely page files
                name = f.stem.lower()
                if any(x in name for x in ['page', 'index', 'home', 'about', 'blog', 'post', 'product']):
                    files.append(f)
                elif 'pages' in f.parts or 'app' in f.parts:
                    files.append(f)
    
    return files[:20]  # Limit


def check_page(file_path: Path) -> Dict[str, Any]:
    """Check a single page for SEO elements."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return {'file': file_path.name, 'passed': [], 'issues': ['Read error'], 'score': 0}
    
    passed = []
    issues = []
    
    # 1. JSON-LD Structured Data
    if 'application/ld+json' in content:
        passed.append("JSON-LD structured data")
        if '"@type"' in content:
            if 'Article' in content:
                passed.append("Article schema")
            if 'FAQPage' in content:
                passed.append("FAQ schema (highly citable)")
    else:
        issues.append("No JSON-LD structured data")
    
    # 2. Heading Structure
    h1_count = len(re.findall(r'<h1[^>]*>', content, re.I))
    h2_count = len(re.findall(r'<h2[^>]*>', content, re.I))
    
    if h1_count == 1:
        passed.append("Single H1 heading")
    elif h1_count == 0:
        issues.append("No H1 heading")
    else:
        issues.append(f"Multiple H1 headings ({h1_count})")
    
    if h2_count >= 2:
        passed.append(f"{h2_count} H2 subheadings")
    else:
        issues.append("Add more H2 subheadings")
    
    # 3. Meta Tags
    if '<title>' in content or 'title=' in content:
        passed.append("Title tag found")
    else:
        issues.append("Missing title tag")
    
    if 'meta' in content.lower() and 'description' in content.lower():
        passed.append("Meta description")
    else:
        issues.append("Missing meta description")
    
    # 4. Author Attribution (E-E-A-T)
    author_patterns = ['author', 'byline', 'written-by', 'rel="author"']
    if any(p in content.lower() for p in author_patterns):
        passed.append("Author attribution")
    else:
        issues.append("No author info (E-E-A-T)")
    
    # 5. Publication Date
    date_patterns = ['datePublished', 'dateModified', 'datetime=', 'pubdate']
    if any(re.search(p, content, re.I) for p in date_patterns):
        passed.append("Publication date")
    else:
        issues.append("No publication date")
    
    # 6. Open Graph
    if 'og:' in content or 'property="og:' in content:
        passed.append("Open Graph tags")
    
    # 7. Lists and Tables (structured content)
    list_count = len(re.findall(r'<(ul|ol)[^>]*>', content, re.I))
    table_count = len(re.findall(r'<table[^>]*>', content, re.I))
    
    if list_count >= 2:
        passed.append(f"{list_count} lists")
    if table_count >= 1:
        passed.append(f"{table_count} table(s)")
    
    # Calculate score
    total = len(passed) + len(issues)
    score = (len(passed) / total * 100) if total > 0 else 0
    
    return {
        'file': file_path.name,
        'passed': passed,
        'issues': issues,
        'score': round(score)
    }


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[AGT-KIT SEO CHECKER] SEO & GEO Audit")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    pages = find_pages(project_path)
    
    if not pages:
        print("\nNo public pages found.")
        print("Looking for: HTML files, pages/, app/ directories")
        output = {
            "script": "seo_checker",
            "skill": "seo-patterns",
            "project": str(project_path),
            "pages_checked": 0,
            "passed": True,
            "message": "No pages found"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    print(f"Found {len(pages)} pages to analyze\n")
    
    results = []
    for page in pages:
        result = check_page(page)
        results.append(result)
        
        # Print summary
        status = "✅" if result['score'] >= 60 else "⚠️"
        print(f"{status} {result['file']}: {result['score']}%")
        
        if result['score'] < 60:
            for issue in result['issues'][:2]:
                print(f"   - {issue}")
    
    # Average score
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    
    print("\n" + "="*60)
    print(f"AVERAGE SEO SCORE: {avg_score:.0f}%")
    print("="*60)
    
    if avg_score >= 80:
        print("✅ Excellent - Well optimized for search & AI")
    elif avg_score >= 60:
        print("✅ Good - Some improvements recommended")
    elif avg_score >= 40:
        print("⚠️  Needs work - Add structured elements")
    else:
        print("❌ Poor - SEO optimization needed")
    
    output = {
        "script": "seo_checker",
        "skill": "seo-patterns",
        "project": str(project_path),
        "pages_checked": len(results),
        "average_score": round(avg_score),
        "passed": avg_score >= 60
    }
    
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if avg_score >= 60 else 1)


if __name__ == "__main__":
    main()
