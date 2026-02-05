#!/usr/bin/env python3
"""
Accessibility Checker - WCAG compliance audit for AGT-Kit
==========================================================

Checks HTML/JSX for common accessibility issues.

Usage:
    python3 .agent/skills/accessibility-patterns/scripts/a11y_checker.py <project_path>

Checks based on WCAG 2.2:
    - Images with alt text
    - Form labels
    - Heading hierarchy
    - Color contrast considerations
    - ARIA attributes
    - Keyboard navigation hints
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

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'venv'}


def find_ui_files(project_path: Path) -> List[Path]:
    """Find UI component files."""
    patterns = ['**/*.tsx', '**/*.jsx', '**/*.html', '**/*.vue']
    
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if not any(skip in f.parts for skip in SKIP_DIRS):
                # Skip test files
                if not any(x in f.name.lower() for x in ['test', 'spec', 'mock']):
                    files.append(f)
    
    return files[:30]  # Limit


def check_file(file_path: Path) -> Dict[str, Any]:
    """Check a single file for accessibility issues."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return {'file': file_path.name, 'passed': [], 'issues': ['Read error']}
    
    passed = []
    issues = []
    
    # 1. Images with alt text
    img_tags = re.findall(r'<img[^>]*>', content, re.I)
    img_without_alt = [img for img in img_tags if 'alt=' not in img.lower()]
    
    if img_tags and not img_without_alt:
        passed.append(f"All {len(img_tags)} images have alt text")
    elif img_without_alt:
        issues.append(f"{len(img_without_alt)} images missing alt text")
    
    # 2. Form labels
    inputs = re.findall(r'<input[^>]*>', content, re.I)
    inputs_need_label = [i for i in inputs if 'type="hidden"' not in i.lower() and 'type="submit"' not in i.lower()]
    
    has_labels = 'label' in content.lower() or 'aria-label' in content.lower()
    if inputs_need_label and has_labels:
        passed.append("Form labels/aria-labels found")
    elif inputs_need_label and not has_labels:
        issues.append("Form inputs may be missing labels")
    
    # 3. Heading hierarchy
    h1_count = len(re.findall(r'<h1[^>]*>', content, re.I))
    h2_count = len(re.findall(r'<h2[^>]*>', content, re.I))
    h3_count = len(re.findall(r'<h3[^>]*>', content, re.I))
    
    if h1_count <= 1:
        passed.append("Proper H1 usage (0-1)")
    else:
        issues.append(f"Multiple H1 tags ({h1_count}) - bad for a11y")
    
    # Check for skipped heading levels (h1 -> h3 without h2)
    if h3_count > 0 and h2_count == 0 and h1_count > 0:
        issues.append("Skipped heading level (H1 -> H3)")
    
    # 4. ARIA attributes
    aria_patterns = ['aria-label', 'aria-labelledby', 'aria-describedby', 'role=']
    has_aria = any(p in content for p in aria_patterns)
    if has_aria:
        passed.append("ARIA attributes used")
    
    # 5. Focus indicators
    focus_patterns = [':focus', 'onFocus', 'tabIndex', 'focus-visible']
    has_focus = any(p in content for p in focus_patterns)
    if has_focus:
        passed.append("Focus handling present")
    
    # 6. Buttons with text/aria-label
    buttons = re.findall(r'<button[^>]*>([^<]*)</button>', content, re.I)
    empty_buttons = [b for b in re.findall(r'<button[^>]*>', content, re.I) 
                     if 'aria-label' not in b.lower() and '>' in b and '</' in content[content.find(b):content.find(b)+100]]
    
    # Check for icon-only buttons
    icon_buttons = re.findall(r'<button[^>]*>\s*<[^>]+/>\s*</button>', content, re.I)
    if icon_buttons:
        issues.append(f"{len(icon_buttons)} icon-only buttons may need aria-label")
    
    # 7. Links with meaningful text
    links = re.findall(r'<a[^>]*>([^<]*)</a>', content, re.I)
    bad_link_text = ['click here', 'read more', 'here', 'more']
    problematic_links = [l for l in links if l.lower().strip() in bad_link_text]
    
    if problematic_links:
        issues.append(f"{len(problematic_links)} links with non-descriptive text")
    elif links:
        passed.append("Link text appears descriptive")
    
    # 8. Color contrast (basic check)
    if 'color:' in content.lower() or 'backgroundColor' in content:
        if 'contrast' in content.lower() or '--' in content:  # CSS variables
            passed.append("Color theming detected")
    
    # 9. Skip links
    if 'skip' in content.lower() and 'main' in content.lower():
        passed.append("Skip link pattern detected")
    
    return {'file': file_path.name, 'passed': passed, 'issues': issues}


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[AGT-KIT A11Y CHECKER] Accessibility Audit (WCAG 2.2)")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    files = find_ui_files(project_path)
    
    if not files:
        print("\nNo UI files found.")
        output = {
            "script": "a11y_checker",
            "skill": "accessibility-patterns",
            "project": str(project_path),
            "files_checked": 0,
            "passed": True
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    print(f"Found {len(files)} UI files to analyze\n")
    
    results = []
    total_passed = 0
    total_issues = 0
    
    for file_path in files:
        result = check_file(file_path)
        
        if result['issues'] or result['passed']:
            results.append(result)
            total_passed += len(result['passed'])
            total_issues += len(result['issues'])
            
            if result['issues']:
                print(f"⚠️  {result['file']}")
                for issue in result['issues'][:2]:
                    print(f"   - {issue}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    print(f"✅ {total_passed} accessibility patterns found")
    print(f"⚠️  {total_issues} potential issues")
    
    passed = total_issues < 10
    
    if passed:
        print("\n✅ Accessibility check passed")
    else:
        print("\n⚠️  Review accessibility issues")
    
    output = {
        "script": "a11y_checker",
        "skill": "accessibility-patterns",
        "project": str(project_path),
        "files_checked": len(files),
        "patterns_found": total_passed,
        "issues_found": total_issues,
        "passed": passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
