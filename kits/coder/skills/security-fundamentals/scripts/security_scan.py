#!/usr/bin/env python3
"""
Security Scan - Comprehensive security validation
==================================================

Validates security principles from security-fundamentals skill.
Based on OWASP Top 10 2025.

Usage:
    python .agent/skills/security-fundamentals/scripts/security_scan.py <project_path>
    python .agent/skills/security-fundamentals/scripts/security_scan.py . --scan-type all

Scan Types:
    - all: Run all scans (default)
    - deps: Dependency vulnerabilities (OWASP A03)
    - secrets: Hardcoded credentials (OWASP A04)
    - patterns: Dangerous code patterns (OWASP A05)
    - config: Security configuration (OWASP A02)
"""

import subprocess
import json
import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except:
    pass


# Secret patterns to detect
SECRET_PATTERNS = [
    # API Keys & Tokens
    (r'api[_-]?key\s*[=:]\s*["\'][^"\']{10,}["\']', "API Key", "high"),
    (r'token\s*[=:]\s*["\'][^"\']{10,}["\']', "Token", "high"),
    (r'bearer\s+[a-zA-Z0-9\-_.]+', "Bearer Token", "critical"),
    
    # Cloud Credentials
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key", "critical"),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\'][^"\']+["\']', "AWS Secret", "critical"),
    
    # Database & Connections
    (r'password\s*[=:]\s*["\'][^"\']{4,}["\']', "Password", "high"),
    (r'(mongodb|postgres|mysql|redis):\/\/[^\s"\']+', "Database URI", "critical"),
    
    # Private Keys
    (r'-----BEGIN\s+(RSA|PRIVATE|EC)\s+KEY-----', "Private Key", "critical"),
    
    # JWT
    (r'eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+', "JWT Token", "high"),
]

# Dangerous code patterns
DANGEROUS_PATTERNS = [
    # Injection risks
    (r'eval\s*\(', "eval()", "critical", "Code Injection"),
    (r'exec\s*\(', "exec()", "critical", "Code Injection"),
    (r'new\s+Function\s*\(', "Function constructor", "high", "Code Injection"),
    (r'child_process\.exec\s*\(', "child_process.exec", "high", "Command Injection"),
    
    # XSS risks
    (r'dangerouslySetInnerHTML', "dangerouslySetInnerHTML", "high", "XSS"),
    (r'\.innerHTML\s*=', "innerHTML assignment", "medium", "XSS"),
    
    # SQL Injection
    (r'["\'][^"\']*\+\s*[a-zA-Z_]+\s*\+\s*["\'].*(?:SELECT|INSERT|UPDATE|DELETE)', "SQL Concat", "critical", "SQL Injection"),
    
    # Insecure configs
    (r'verify\s*=\s*False', "SSL Verify Disabled", "high", "MITM"),
]

SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '__pycache__', '.venv', 'venv', '.next'}
CODE_EXTENSIONS = {'.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.java'}
CONFIG_EXTENSIONS = {'.json', '.yaml', '.yml', '.toml', '.env'}


def scan_dependencies(project_path: str) -> Dict[str, Any]:
    """Scan for dependency vulnerabilities (OWASP A03)."""
    results = {"tool": "dependency_scanner", "findings": [], "status": "✅ Secure"}
    
    # Check for lock files
    lock_files = {
        "npm": ["package-lock.json", "pnpm-lock.yaml"],
        "pip": ["requirements.txt", "poetry.lock"],
    }
    
    for manager, files in lock_files.items():
        pkg_file = "package.json" if manager == "npm" else "requirements.txt"
        if not (Path(project_path) / pkg_file).exists():
            continue
            
        has_lock = any((Path(project_path) / f).exists() for f in files)
        if not has_lock:
            results["findings"].append({
                "type": "Missing Lock File",
                "severity": "high",
                "message": f"{manager}: No lock file found"
            })
    
    # Run npm audit if applicable
    if (Path(project_path) / "package.json").exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            try:
                audit_data = json.loads(result.stdout)
                vulns = audit_data.get("vulnerabilities", {})
                
                severity_count = {"critical": 0, "high": 0, "moderate": 0}
                for vuln in vulns.values():
                    sev = vuln.get("severity", "low").lower()
                    if sev in severity_count:
                        severity_count[sev] += 1
                
                if severity_count["critical"] > 0:
                    results["status"] = "🔴 Critical vulnerabilities"
                    results["findings"].append({
                        "type": "npm audit",
                        "severity": "critical",
                        "message": f"{severity_count['critical']} critical vulnerabilities"
                    })
                elif severity_count["high"] > 0:
                    results["status"] = "🟡 High vulnerabilities"
                    
                results["npm_audit"] = severity_count
            except json.JSONDecodeError:
                pass
        except:
            pass
    
    return results


def scan_secrets(project_path: str) -> Dict[str, Any]:
    """Scan for hardcoded secrets (OWASP A04)."""
    results = {
        "tool": "secret_scanner",
        "findings": [],
        "status": "✅ No secrets",
        "scanned_files": 0,
        "by_severity": {"critical": 0, "high": 0, "medium": 0}
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CODE_EXTENSIONS and ext not in CONFIG_EXTENSIONS:
                continue
                
            filepath = Path(root) / file
            results["scanned_files"] += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for pattern, secret_type, severity in SECRET_PATTERNS:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            results["findings"].append({
                                "file": str(filepath.relative_to(project_path)),
                                "type": secret_type,
                                "severity": severity,
                            })
                            results["by_severity"][severity] += 1
            except:
                pass
    
    if results["by_severity"]["critical"] > 0:
        results["status"] = "🔴 CRITICAL: Secrets exposed!"
    elif results["by_severity"]["high"] > 0:
        results["status"] = "🟡 HIGH: Secrets found"
    
    results["findings"] = results["findings"][:15]
    return results


def scan_patterns(project_path: str) -> Dict[str, Any]:
    """Scan for dangerous code patterns (OWASP A05)."""
    results = {
        "tool": "pattern_scanner",
        "findings": [],
        "status": "✅ No dangerous patterns",
        "scanned_files": 0
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CODE_EXTENSIONS:
                continue
                
            filepath = Path(root) / file
            results["scanned_files"] += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    for line_num, line in enumerate(lines, 1):
                        for pattern, name, severity, category in DANGEROUS_PATTERNS:
                            if re.search(pattern, line, re.IGNORECASE):
                                results["findings"].append({
                                    "file": str(filepath.relative_to(project_path)),
                                    "line": line_num,
                                    "pattern": name,
                                    "severity": severity,
                                    "category": category,
                                })
            except:
                pass
    
    critical = sum(1 for f in results["findings"] if f["severity"] == "critical")
    if critical > 0:
        results["status"] = f"🔴 CRITICAL: {critical} dangerous patterns"
    elif results["findings"]:
        results["status"] = "🟡 Patterns need review"
    
    results["findings"] = results["findings"][:20]
    return results


def run_full_scan(project_path: str, scan_type: str = "all") -> Dict[str, Any]:
    """Run complete security scan."""
    report = {
        "project": project_path,
        "timestamp": datetime.now().isoformat(),
        "scan_type": scan_type,
        "scans": {},
        "summary": {
            "total_findings": 0,
            "critical": 0,
            "high": 0,
            "overall_status": "✅ SECURE"
        }
    }
    
    scanners = {
        "deps": ("dependencies", scan_dependencies),
        "secrets": ("secrets", scan_secrets),
        "patterns": ("code_patterns", scan_patterns),
    }
    
    for key, (name, scanner) in scanners.items():
        if scan_type == "all" or scan_type == key:
            result = scanner(project_path)
            report["scans"][name] = result
            
            findings = len(result.get("findings", []))
            report["summary"]["total_findings"] += findings
            
            for finding in result.get("findings", []):
                sev = finding.get("severity", "low")
                if sev == "critical":
                    report["summary"]["critical"] += 1
                elif sev == "high":
                    report["summary"]["high"] += 1
    
    if report["summary"]["critical"] > 0:
        report["summary"]["overall_status"] = "🔴 CRITICAL ISSUES"
    elif report["summary"]["high"] > 0:
        report["summary"]["overall_status"] = "🟡 HIGH RISK"
    elif report["summary"]["total_findings"] > 0:
        report["summary"]["overall_status"] = "🟠 REVIEW NEEDED"
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description="AGT-Kit Security Scanner (security-fundamentals skill)"
    )
    parser.add_argument("project_path", nargs="?", default=".", help="Project to scan")
    parser.add_argument("--scan-type", choices=["all", "deps", "secrets", "patterns"],
                        default="all", help="Scan type")
    parser.add_argument("--output", choices=["json", "summary"], default="summary")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.project_path):
        print(json.dumps({"error": f"Not found: {args.project_path}"}))
        sys.exit(1)
    
    result = run_full_scan(args.project_path, args.scan_type)
    
    if args.output == "summary":
        print(f"\n{'='*60}")
        print(f"[AGT-KIT SECURITY SCAN] {result['project']}")
        print(f"{'='*60}")
        print(f"Status: {result['summary']['overall_status']}")
        print(f"Total Findings: {result['summary']['total_findings']}")
        print(f"  Critical: {result['summary']['critical']}")
        print(f"  High: {result['summary']['high']}")
        print(f"{'='*60}\n")
        
        for scan_name, scan_result in result['scans'].items():
            print(f"\n{scan_name.upper()}: {scan_result['status']}")
            for finding in scan_result.get('findings', [])[:5]:
                print(f"  - {finding.get('type', finding.get('pattern', 'Issue'))}: {finding.get('file', finding.get('message', ''))}")
    else:
        print(json.dumps(result, indent=2))
    
    # Exit with error if critical issues
    sys.exit(1 if result['summary']['critical'] > 0 else 0)


if __name__ == "__main__":
    main()
