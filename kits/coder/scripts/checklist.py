#!/usr/bin/env python3
"""
AGT-Kit Master Checklist Runner
=================================

Orchestrates validation scripts in priority order for any project type.
Designed to work with AGT-Kit's 37 skills.

Usage:
    python .agent/scripts/checklist.py <project_path>
    python .agent/scripts/checklist.py . --url http://localhost:3000
    python .agent/scripts/checklist.py . --quick

Priority Order (P0-P6):
    P0: Security Scan (vulnerabilities, secrets)
    P1: Lint & Type Check (code quality)
    P2: Schema Validation (if database exists)
    P3: Test Runner (unit/integration tests)
    P4: UX Audit (accessibility, design)
    P5: SEO Check (meta tags, Core Web Vitals)
    P6: Performance (Lighthouse - requires URL)
"""

import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")


def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")


def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


# Define skill-based checks - maps to AGT-Kit skills
CORE_CHECKS = [
    {
        "name": "Security Scan",
        "skill": "security-fundamentals",
        "script": ".agent/skills/security-fundamentals/scripts/security_scan.py",
        "priority": 0,
        "required": True,
    },
    {
        "name": "Lint Check",
        "skill": "clean-code",
        "script": ".agent/skills/clean-code/scripts/lint_runner.py",
        "priority": 1,
        "required": True,
    },
    {
        "name": "Schema Validation",
        "skill": "database-design",
        "script": ".agent/skills/database-design/scripts/schema_validator.py",
        "priority": 2,
        "required": False,
    },
    {
        "name": "Test Runner",
        "skill": "testing-patterns",
        "script": ".agent/skills/testing-patterns/scripts/test_runner.py",
        "priority": 3,
        "required": False,
    },
    {
        "name": "UX Audit",
        "skill": "frontend-design",
        "script": ".agent/skills/frontend-design/scripts/ux_audit.py",
        "priority": 4,
        "required": False,
    },
    {
        "name": "SEO Check",
        "skill": "seo-patterns",
        "script": ".agent/skills/seo-patterns/scripts/seo_checker.py",
        "priority": 5,
        "required": False,
    },
]

PERFORMANCE_CHECKS = [
    {
        "name": "Lighthouse Audit",
        "skill": "performance-profiling",
        "script": ".agent/skills/performance-profiling/scripts/lighthouse_audit.py",
        "priority": 6,
        "required": False,
        "needs_url": True,
    },
    {
        "name": "E2E Tests",
        "skill": "e2e-testing",
        "script": ".agent/skills/e2e-testing/scripts/playwright_runner.py",
        "priority": 7,
        "required": False,
        "needs_url": True,
    },
]

QUICK_CHECKS = ["Security Scan", "Lint Check", "Test Runner"]


def detect_project_type(project_path: Path) -> str:
    """Detect project type to filter relevant checks."""
    if (project_path / "package.json").exists():
        pkg = json.loads((project_path / "package.json").read_text())
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        
        if "next" in deps:
            return "nextjs"
        if "react" in deps:
            return "react"
        if "express" in deps or "fastify" in deps:
            return "node-backend"
        return "node"
    
    if (project_path / "pyproject.toml").exists() or (project_path / "requirements.txt").exists():
        return "python"
    
    if (project_path / "pubspec.yaml").exists():
        return "flutter"
    
    if (project_path / "go.mod").exists():
        return "go"
    
    return "unknown"


def run_script(check: Dict[str, Any], project_path: Path, url: Optional[str] = None) -> Dict[str, Any]:
    """Run a validation script and capture results."""
    script_path = project_path / check["script"]
    
    if not script_path.exists():
        print_warning(f"{check['name']}: Script not found ({check['skill']} skill)")
        return {
            "name": check["name"],
            "skill": check["skill"],
            "passed": True,
            "skipped": True,
            "reason": "Script not found"
        }
    
    print_step(f"Running: {check['name']} ({check['skill']})")
    
    # Build command
    cmd = ["python", str(script_path), str(project_path)]
    if url and check.get("needs_url"):
        cmd.append(url)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{check['name']}: PASSED")
        else:
            print_error(f"{check['name']}: FAILED")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
        
        return {
            "name": check["name"],
            "skill": check["skill"],
            "passed": passed,
            "output": result.stdout[:2000] if result.stdout else "",
            "error": result.stderr[:500] if result.stderr else "",
            "skipped": False
        }
    
    except subprocess.TimeoutExpired:
        print_error(f"{check['name']}: TIMEOUT (>5 minutes)")
        return {"name": check["name"], "skill": check["skill"], "passed": False, "skipped": False, "error": "Timeout"}
    
    except Exception as e:
        print_error(f"{check['name']}: ERROR - {str(e)}")
        return {"name": check["name"], "skill": check["skill"], "passed": False, "skipped": False, "error": str(e)}


def print_summary(results: List[Dict], project_type: str) -> bool:
    """Print final summary report."""
    print_header("📊 AGT-KIT CHECKLIST SUMMARY")
    
    passed = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped = sum(1 for r in results if r.get("skipped"))
    
    print(f"Project Type: {project_type}")
    print(f"Total Checks: {len(results)}")
    print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Failed: {failed}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Skipped: {skipped}{Colors.ENDC}")
    print()
    
    # Results by skill
    print(f"{Colors.BOLD}Results by Skill:{Colors.ENDC}")
    for r in results:
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        print(f"  {status} {r['name']} ({r['skill']})")
    
    print()
    
    if failed > 0:
        print_error(f"{failed} check(s) FAILED - Please fix before proceeding")
        return False
    else:
        print_success("All checks PASSED ✨")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="AGT-Kit Master Checklist - Validate project with AGT-Kit skills",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .agent/scripts/checklist.py .                      # Core checks
  python .agent/scripts/checklist.py . --url http://localhost:3000  # + Performance
  python .agent/scripts/checklist.py . --quick              # Quick checks only
        """
    )
    parser.add_argument("project", help="Project path to validate")
    parser.add_argument("--url", help="URL for performance checks (Lighthouse, Playwright)")
    parser.add_argument("--quick", action="store_true", help="Run only quick checks (Security, Lint, Tests)")
    parser.add_argument("--stop-on-fail", action="store_true", help="Stop on first critical failure")
    
    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        sys.exit(1)
    
    project_type = detect_project_type(project_path)
    
    print_header("🚀 AGT-KIT MASTER CHECKLIST")
    print(f"Project: {project_path}")
    print(f"Type: {project_type}")
    print(f"URL: {args.url if args.url else 'Not provided'}")
    print(f"Mode: {'Quick' if args.quick else 'Full'}")
    
    results = []
    
    # Filter checks based on --quick flag
    checks_to_run = CORE_CHECKS.copy()
    if args.quick:
        checks_to_run = [c for c in checks_to_run if c["name"] in QUICK_CHECKS]
    
    # Run core checks
    print_header("📋 CORE CHECKS")
    for check in sorted(checks_to_run, key=lambda x: x["priority"]):
        result = run_script(check, project_path)
        results.append(result)
        
        # Stop on critical failure if flag set
        if args.stop_on_fail and check["required"] and not result["passed"] and not result.get("skipped"):
            print_error(f"CRITICAL: {check['name']} failed. Stopping.")
            print_summary(results, project_type)
            sys.exit(1)
    
    # Run performance checks if URL provided
    if args.url and not args.quick:
        print_header("⚡ PERFORMANCE CHECKS")
        for check in PERFORMANCE_CHECKS:
            result = run_script(check, project_path, args.url)
            results.append(result)
    
    # Print summary
    all_passed = print_summary(results, project_type)
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
