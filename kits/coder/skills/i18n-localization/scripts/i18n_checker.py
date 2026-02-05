#!/usr/bin/env python3
"""
i18n Checker - Internationalization audit for AGT-Kit
======================================================

Detects hardcoded strings and checks translation completeness.

Usage:
    python3 .agent/skills/i18n-localization/scripts/i18n_checker.py <project_path>

Checks:
    - Hardcoded strings in JSX/Vue/Python
    - Locale file completeness (missing keys)
    - i18n library usage patterns
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'venv'}

# Patterns indicating hardcoded strings
HARDCODED_PATTERNS = {
    'jsx': [
        r'>\s*[A-Z][a-zA-Z\s]{3,30}\s*</',  # Text in JSX
        r'(title|placeholder|label|alt)="[A-Z][a-zA-Z\s]{2,}"',  # Attributes
    ],
    'vue': [
        r'>\s*[A-Z][a-zA-Z\s]{3,30}\s*</',
        r'(placeholder|label|title)="[A-Z][a-zA-Z\s]{2,}"',
    ],
    'python': [
        r'(print|raise\s+\w+)\s*\(\s*["\'][A-Z][^"\']{5,}["\']',
        r'flash\s*\(\s*["\'][A-Z][^"\']{5,}["\']',
    ]
}

# Patterns indicating proper i18n usage
I18N_PATTERNS = [
    r't\(["\']',           # react-i18next
    r'useTranslation',     # React hook
    r'\$t\(',              # Vue i18n
    r'_\(["\']',           # Python gettext
    r'gettext\(',          # Python
    r'useTranslations',    # next-intl
    r'FormattedMessage',   # react-intl
]


def find_locale_files(project_path: Path) -> List[Path]:
    """Find translation/locale files."""
    patterns = [
        '**/locales/**/*.json',
        '**/translations/**/*.json',
        '**/lang/**/*.json',
        '**/i18n/**/*.json',
        '**/messages/*.json',
    ]
    
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if not any(skip in f.parts for skip in SKIP_DIRS):
                files.append(f)
    
    return files


def flatten_keys(d: dict, prefix: str = '') -> Set[str]:
    """Flatten nested dict keys."""
    keys = set()
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            keys.update(flatten_keys(v, new_key))
        else:
            keys.add(new_key)
    return keys


def check_locale_completeness(locale_files: List[Path]) -> Dict[str, Any]:
    """Check if all locales have the same keys."""
    issues = []
    passed = []
    
    if not locale_files:
        return {'passed': ['No locale files found (not required)'], 'issues': []}
    
    # Group by language folder
    locales: Dict[str, Dict[str, Set[str]]] = {}
    
    for f in locale_files:
        if f.suffix == '.json':
            try:
                lang = f.parent.name
                content = json.loads(f.read_text(encoding='utf-8'))
                if lang not in locales:
                    locales[lang] = {}
                locales[lang][f.stem] = flatten_keys(content)
            except:
                continue
    
    if len(locales) < 2:
        passed.append(f"Found {len(locale_files)} locale file(s)")
        return {'passed': passed, 'issues': issues}
    
    passed.append(f"Found {len(locales)} languages: {', '.join(locales.keys())}")
    
    # Compare keys across locales
    all_langs = list(locales.keys())
    base_lang = all_langs[0]
    
    for namespace in locales.get(base_lang, {}):
        base_keys = locales[base_lang].get(namespace, set())
        
        for lang in all_langs[1:]:
            other_keys = locales.get(lang, {}).get(namespace, set())
            
            missing = base_keys - other_keys
            if missing:
                issues.append(f"{lang}/{namespace}: Missing {len(missing)} keys")
            
            extra = other_keys - base_keys
            if extra and len(extra) > 3:
                issues.append(f"{lang}/{namespace}: {len(extra)} extra keys")
    
    if not issues:
        passed.append("All locales have matching keys")
    
    return {'passed': passed, 'issues': issues}


def check_hardcoded_strings(project_path: Path) -> Dict[str, Any]:
    """Check for hardcoded strings in code files."""
    issues = []
    passed = []
    
    extensions = {
        '.tsx': 'jsx', '.jsx': 'jsx', '.ts': 'jsx', '.js': 'jsx',
        '.vue': 'vue',
        '.py': 'python'
    }
    
    code_files = []
    for ext in extensions:
        for f in project_path.rglob(f"*{ext}"):
            if not any(skip in f.parts for skip in SKIP_DIRS):
                if not any(x in f.name for x in ['test', 'spec', 'config']):
                    code_files.append(f)
    
    if not code_files:
        return {'passed': ['No code files found'], 'issues': []}
    
    files_with_i18n = 0
    files_with_hardcoded = 0
    examples = []
    
    for file_path in code_files[:50]:  # Limit
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            ext = file_path.suffix
            file_type = extensions.get(ext, 'jsx')
            
            # Check for i18n usage
            has_i18n = any(re.search(p, content) for p in I18N_PATTERNS)
            if has_i18n:
                files_with_i18n += 1
            
            # Check for hardcoded strings
            patterns = HARDCODED_PATTERNS.get(file_type, [])
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches and not has_i18n:
                    files_with_hardcoded += 1
                    if len(examples) < 5:
                        examples.append(f"{file_path.name}: {str(matches[0])[:30]}...")
                    break
                    
        except:
            continue
    
    passed.append(f"Analyzed {len(code_files)} code files")
    
    if files_with_i18n > 0:
        passed.append(f"{files_with_i18n} files use i18n patterns")
    
    if files_with_hardcoded > 0:
        issues.append(f"{files_with_hardcoded} files may have hardcoded strings")
        for ex in examples[:3]:
            issues.append(f"  → {ex}")
    else:
        passed.append("No obvious hardcoded strings detected")
    
    return {'passed': passed, 'issues': issues}


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[AGT-KIT i18n CHECKER] Internationalization Audit")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # Check locale files
    locale_files = find_locale_files(project_path)
    locale_result = check_locale_completeness(locale_files)
    
    # Check hardcoded strings
    code_result = check_hardcoded_strings(project_path)
    
    # Print results
    print("\n📁 LOCALE FILES")
    print("-"*40)
    for item in locale_result['passed']:
        print(f"  ✅ {item}")
    for item in locale_result['issues']:
        print(f"  ⚠️  {item}")
    
    print("\n💻 CODE ANALYSIS")
    print("-"*40)
    for item in code_result['passed']:
        print(f"  ✅ {item}")
    for item in code_result['issues']:
        print(f"  ⚠️  {item}")
    
    # Summary
    all_issues = locale_result['issues'] + code_result['issues']
    critical = sum(1 for i in all_issues if 'hardcoded' in i.lower() or 'missing' in i.lower())
    
    print("\n" + "="*60)
    
    passed = critical == 0
    
    if passed:
        print("✅ i18n CHECK PASSED")
    else:
        print(f"⚠️  i18n CHECK: {critical} issues found")
    
    output = {
        "script": "i18n_checker",
        "skill": "i18n-localization",
        "project": str(project_path),
        "locale_files": len(locale_files),
        "issues": len(all_issues),
        "passed": passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
