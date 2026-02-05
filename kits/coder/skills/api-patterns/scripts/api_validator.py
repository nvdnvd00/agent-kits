#!/usr/bin/env python3
"""
API Validator - API endpoint best practices check for AGT-Kit
==============================================================

Validates OpenAPI specs, API code patterns, and common issues.

Usage:
    python3 .agent/skills/api-patterns/scripts/api_validator.py <project_path>

Checks:
    - OpenAPI/Swagger specification completeness
    - Error handling patterns
    - Input validation (Zod, Joi, etc.)
    - Authentication/authorization
    - Rate limiting
    - HTTP status codes
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.next', 'venv'}


def find_api_files(project_path: Path) -> List[tuple]:
    """Find API-related files."""
    files = []
    
    patterns = {
        'openapi': ['**/openapi*.json', '**/openapi*.yaml', '**/swagger*.json', '**/swagger*.yaml'],
        'routes': ['**/routes/**/*.ts', '**/routes/**/*.js', '**/api/**/*.ts', '**/api/**/*.py'],
        'controllers': ['**/controllers/**/*.ts', '**/controllers/**/*.js'],
    }
    
    for file_type, globs in patterns.items():
        for pattern in globs:
            for f in project_path.glob(pattern):
                if not any(skip in f.parts for skip in SKIP_DIRS):
                    files.append((file_type, f))
    
    return files[:20]  # Limit


def check_openapi_spec(file_path: Path) -> Dict[str, Any]:
    """Check OpenAPI/Swagger specification."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # JSON or YAML
        is_json = file_path.suffix == '.json'
        
        if is_json:
            try:
                spec = json.loads(content)
                
                # Version check
                if 'openapi' in spec or 'swagger' in spec:
                    passed.append("OpenAPI version defined")
                
                # Info section
                if 'info' in spec:
                    if spec['info'].get('title'):
                        passed.append("API title defined")
                    if spec['info'].get('version'):
                        passed.append("API version defined")
                    if not spec['info'].get('description'):
                        issues.append("API description missing")
                
                # Paths
                if 'paths' in spec:
                    path_count = len(spec['paths'])
                    passed.append(f"{path_count} endpoints defined")
                    
                    # Check each endpoint
                    for path, methods in spec['paths'].items():
                        for method, details in methods.items():
                            if method in ['get', 'post', 'put', 'patch', 'delete']:
                                if 'responses' not in details:
                                    issues.append(f"{method.upper()} {path}: No responses")
                                if not details.get('summary') and not details.get('description'):
                                    issues.append(f"{method.upper()} {path}: No description")
                else:
                    issues.append("No paths defined")
                    
            except json.JSONDecodeError as e:
                issues.append(f"Invalid JSON: {str(e)[:30]}")
        else:
            # Basic YAML check
            if 'openapi:' in content or 'swagger:' in content:
                passed.append("OpenAPI version defined")
            if 'paths:' in content:
                passed.append("Paths section exists")
            if 'components:' in content:
                passed.append("Components defined")
                
    except Exception as e:
        issues.append(f"Read error: {str(e)[:30]}")
    
    return {"passed": passed, "issues": issues, "type": "openapi"}


def check_api_code(file_path: Path) -> Dict[str, Any]:
    """Check API code for best practices."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Error handling
        error_patterns = [r'try\s*{', r'try:', r'\.catch\(', r'except\s+', r'catch\s*\(']
        if any(re.search(p, content) for p in error_patterns):
            passed.append("Error handling present")
        else:
            issues.append("No error handling found")
        
        # HTTP status codes
        status_patterns = [
            r'\.status\(\d{3}\)', r'status\s*=\s*\d{3}', r'statusCode.*\d{3}',
            r'HttpStatus\.', r'res\.status\('
        ]
        if any(re.search(p, content) for p in status_patterns):
            passed.append("HTTP status codes used")
        else:
            issues.append("No explicit status codes")
        
        # Input validation
        validation_patterns = [r'validate', r'schema', r'zod', r'joi', r'yup', r'pydantic', r'@Body\(']
        if any(re.search(p, content, re.I) for p in validation_patterns):
            passed.append("Input validation present")
        else:
            issues.append("No input validation detected")
        
        # Authentication
        auth_patterns = [r'auth', r'jwt', r'bearer', r'token', r'middleware', r'guard']
        if any(re.search(p, content, re.I) for p in auth_patterns):
            passed.append("Authentication detected")
        
        # Rate limiting
        rate_patterns = [r'rateLimit', r'throttle', r'rate.?limit']
        if any(re.search(p, content, re.I) for p in rate_patterns):
            passed.append("Rate limiting present")
        
        # Logging
        log_patterns = [r'console\.(log|error|warn)', r'logger\.', r'logging\.\w+']
        if any(re.search(p, content) for p in log_patterns):
            passed.append("Logging present")
        
        # CORS
        if 'cors' in content.lower():
            passed.append("CORS configuration")
        
    except Exception as e:
        issues.append(f"Read error: {str(e)[:30]}")
    
    return {"passed": passed, "issues": issues, "type": "code"}


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[AGT-KIT API VALIDATOR] API Best Practices Check")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    api_files = find_api_files(project_path)
    
    if not api_files:
        print("No API files found.")
        print("Looking for: openapi.json, swagger.yaml, routes/, api/, controllers/")
        output = {
            "script": "api_validator",
            "skill": "api-patterns",
            "project": str(project_path),
            "files_checked": 0,
            "passed": True,
            "message": "No API files found"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    print(f"Found {len(api_files)} API files\n")
    
    all_results = []
    total_passed = 0
    total_issues = 0
    
    for file_type, file_path in api_files:
        print(f"📄 {file_path.name} [{file_type}]")
        
        if file_type == 'openapi':
            result = check_openapi_spec(file_path)
        else:
            result = check_api_code(file_path)
        
        for item in result["passed"]:
            print(f"  ✅ {item}")
            total_passed += 1
        for item in result["issues"][:3]:
            print(f"  ⚠️  {item}")
            total_issues += 1
        
        all_results.append({
            "file": str(file_path.name),
            **result
        })
        print()
    
    # Summary
    print("="*60)
    print(f"SUMMARY: {total_passed} passed, {total_issues} issues")
    print("="*60)
    
    passed = total_issues < 5
    
    if passed:
        print("✅ API validation passed")
    else:
        print("⚠️  API needs improvement")
    
    output = {
        "script": "api_validator",
        "skill": "api-patterns",
        "project": str(project_path),
        "files_checked": len(api_files),
        "total_passed": total_passed,
        "total_issues": total_issues,
        "passed": passed
    }
    
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
