#!/usr/bin/env python3
"""
Example validator for api-patterns

Usage:
    python validate.py <project_path>
"""

import sys
from pathlib import Path


def validate(project_path: str) -> dict:
    """Main validation logic"""
    results = {
        'errors': [],
        'warnings': [],
        'passed': []
    }
    
    # TODO: Add validation logic
    results['passed'].append('Placeholder validation passed')
    
    return results


def print_results(results: dict):
    """Pretty print results"""
    print("\n🔍 Validation Results\n")
    
    if results['errors']:
        print(f"❌ Errors ({len(results['errors'])})")
        for error in results['errors']:
            print(f"  - {error}")
    
    if results['warnings']:
        print(f"\n⚠️  Warnings ({len(results['warnings'])})")
        for warning in results['warnings']:
            print(f"  - {warning}")
    
    if results['passed']:
        print(f"\n✅ Passed ({len(results['passed'])})")
        for passed in results['passed']:
            print(f"  - {passed}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    results = validate(project_path)
    print_results(results)
    
    sys.exit(1 if results['errors'] else 0)
