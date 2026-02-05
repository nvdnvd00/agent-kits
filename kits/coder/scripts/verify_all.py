#!/usr/bin/env python3
"""
AGT-Kit Full Verification Suite
=================================

Runs COMPLETE validation including all checks + performance + E2E.
Use this before deployment or major releases.

Usage:
    python .agent/scripts/verify_all.py <project_path> --url <URL>
    python .agent/scripts/verify_all.py . --url http://localhost:3000

Includes ALL checks from AGT-Kit skills:
    ✅ Security (security-fundamentals, auth-patterns)
    ✅ Code Quality (clean-code, testing-patterns)
    ✅ Database (database-design, postgres-patterns)
    ✅ Frontend (frontend-design, accessibility-patterns)
    ✅ SEO (seo-patterns)
    ✅ Performance (performance-profiling)
    ✅ E2E Testing (e2e-testing)
    ✅ Mobile (mobile-design) - if applicable
"""

import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# ANSI colors
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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")


def print_step(text: str):
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 {text}{Colors.ENDC}")


def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


# Complete verification suite organized by category
VERIFICATION_SUITE = [
    # P0: Security (CRITICAL)
    {
        "category": "Security",
        "priority": 0,
        "checks": [
            {"name": "Security Scan", "skill": "security-fundamentals", "script": ".agent/skills/security-fundamentals/scripts/security_scan.py", "required": True},
            {"name": "Dependency Audit", "skill": "security-fundamentals", "script": ".agent/skills/security-fundamentals/scripts/dependency_audit.py", "required": False},
            {"name": "Auth Validation", "skill": "auth-patterns", "script": ".agent/skills/auth-patterns/scripts/auth_validator.py", "required": False},
        ]
    },
    
    # P1: Code Quality (CRITICAL)
    {
        "category": "Code Quality",
        "priority": 1,
        "checks": [
            {"name": "Lint Check", "skill": "clean-code", "script": ".agent/skills/clean-code/scripts/lint_runner.py", "required": True},
            {"name": "Type Coverage", "skill": "typescript-patterns", "script": ".agent/skills/typescript-patterns/scripts/type_coverage.py", "required": False},
        ]
    },
    
    # P2: Data Layer
    {
        "category": "Data Layer",
        "priority": 2,
        "checks": [
            {"name": "Schema Validation", "skill": "database-design", "script": ".agent/skills/database-design/scripts/schema_validator.py", "required": False},
            {"name": "PostgreSQL Audit", "skill": "postgres-patterns", "script": ".agent/skills/postgres-patterns/scripts/postgres_audit.py", "required": False},
        ]
    },
    
    # P3: Testing
    {
        "category": "Testing",
        "priority": 3,
        "checks": [
            {"name": "Test Suite", "skill": "testing-patterns", "script": ".agent/skills/testing-patterns/scripts/test_runner.py", "required": False},
        ]
    },
    
    # P4: UX & Accessibility
    {
        "category": "UX & Accessibility",
        "priority": 4,
        "checks": [
            {"name": "UX Audit", "skill": "frontend-design", "script": ".agent/skills/frontend-design/scripts/ux_audit.py", "required": False},
            {"name": "Accessibility Check", "skill": "accessibility-patterns", "script": ".agent/skills/accessibility-patterns/scripts/accessibility_checker.py", "required": False},
        ]
    },
    
    # P5: SEO
    {
        "category": "SEO",
        "priority": 5,
        "checks": [
            {"name": "SEO Check", "skill": "seo-patterns", "script": ".agent/skills/seo-patterns/scripts/seo_checker.py", "required": False},
        ]
    },
    
    # P6: Performance (requires URL)
    {
        "category": "Performance",
        "priority": 6,
        "requires_url": True,
        "checks": [
            {"name": "Lighthouse Audit", "skill": "performance-profiling", "script": ".agent/skills/performance-profiling/scripts/lighthouse_audit.py", "required": True, "needs_url": True},
        ]
    },
    
    # P7: E2E Testing (requires URL)
    {
        "category": "E2E Testing",
        "priority": 7,
        "requires_url": True,
        "checks": [
            {"name": "Playwright E2E", "skill": "e2e-testing", "script": ".agent/skills/e2e-testing/scripts/playwright_runner.py", "required": False, "needs_url": True},
        ]
    },
    
    # P8: Mobile (if applicable)
    {
        "category": "Mobile",
        "priority": 8,
        "checks": [
            {"name": "Mobile Audit", "skill": "mobile-design", "script": ".agent/skills/mobile-design/scripts/mobile_audit.py", "required": False},
        ]
    },
    
    # P9: API (if applicable)
    {
        "category": "API",
        "priority": 9,
        "checks": [
            {"name": "API Validator", "skill": "api-patterns", "script": ".agent/skills/api-patterns/scripts/api_validator.py", "required": False},
        ]
    },
]


def detect_project_type(project_path: Path) -> Dict[str, Any]:
    """Detect project type and relevant categories."""
    info = {"type": "unknown", "categories": ["Security", "Code Quality", "Testing"]}
    
    if (project_path / "package.json").exists():
        try:
            pkg = json.loads((project_path / "package.json").read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            if "next" in deps or "react" in deps:
                info["type"] = "web-frontend"
                info["categories"].extend(["UX & Accessibility", "SEO", "Performance", "E2E Testing"])
            elif "express" in deps or "fastify" in deps:
                info["type"] = "node-backend"
                info["categories"].extend(["Data Layer", "API"])
            else:
                info["type"] = "node"
        except:
            info["type"] = "node"
    
    if (project_path / "pubspec.yaml").exists():
        info["type"] = "flutter"
        info["categories"].append("Mobile")
    
    if (project_path / "pyproject.toml").exists():
        info["type"] = "python"
        info["categories"].extend(["Data Layer", "API"])
    
    return info


def run_script(check: Dict[str, Any], project_path: Path, url: Optional[str] = None) -> Dict[str, Any]:
    """Run validation script."""
    script_path = project_path / check["script"]
    
    if not script_path.exists():
        print_warning(f"{check['name']}: Script not found")
        return {
            "name": check["name"],
            "skill": check["skill"],
            "passed": True,
            "skipped": True,
            "duration": 0
        }
    
    print_step(f"Running: {check['name']}")
    start_time = datetime.now()
    
    # Build command
    cmd = ["python", str(script_path), str(project_path)]
    if url and check.get("needs_url"):
        cmd.append(url)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        duration = (datetime.now() - start_time).total_seconds()
        passed = result.returncode == 0
        
        if passed:
            print_success(f"{check['name']}: PASSED ({duration:.1f}s)")
        else:
            print_error(f"{check['name']}: FAILED ({duration:.1f}s)")
            if result.stderr:
                print(f"  {result.stderr[:300]}")
        
        return {
            "name": check["name"],
            "skill": check["skill"],
            "passed": passed,
            "output": result.stdout[:2000] if result.stdout else "",
            "error": result.stderr[:500] if result.stderr else "",
            "skipped": False,
            "duration": duration
        }
    
    except subprocess.TimeoutExpired:
        duration = (datetime.now() - start_time).total_seconds()
        print_error(f"{check['name']}: TIMEOUT (>{duration:.0f}s)")
        return {"name": check["name"], "skill": check["skill"], "passed": False, "skipped": False, "duration": duration, "error": "Timeout"}
    
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        print_error(f"{check['name']}: ERROR - {str(e)}")
        return {"name": check["name"], "skill": check["skill"], "passed": False, "skipped": False, "duration": duration, "error": str(e)}


def print_final_report(results: List[Dict], start_time: datetime, project_info: Dict) -> bool:
    """Print comprehensive final report."""
    total_duration = (datetime.now() - start_time).total_seconds()
    
    print_header("📊 AGT-KIT FULL VERIFICATION REPORT")
    
    # Statistics
    total = len(results)
    passed = sum(1 for r in results if r["passed"] and not r.get("skipped"))
    failed = sum(1 for r in results if not r["passed"] and not r.get("skipped"))
    skipped = sum(1 for r in results if r.get("skipped"))
    
    print(f"Project Type: {project_info['type']}")
    print(f"Total Duration: {total_duration:.1f}s")
    print(f"Total Checks: {total}")
    print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.ENDC}")
    print(f"{Colors.RED}❌ Failed: {failed}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏭️  Skipped: {skipped}{Colors.ENDC}")
    print()
    
    # Category breakdown
    print(f"{Colors.BOLD}Results by Category:{Colors.ENDC}")
    current_category = None
    for r in results:
        if r.get("category") and r["category"] != current_category:
            current_category = r["category"]
            print(f"\n{Colors.BOLD}{Colors.CYAN}{current_category}:{Colors.ENDC}")
        
        if r.get("skipped"):
            status = f"{Colors.YELLOW}⏭️ {Colors.ENDC}"
        elif r["passed"]:
            status = f"{Colors.GREEN}✅{Colors.ENDC}"
        else:
            status = f"{Colors.RED}❌{Colors.ENDC}"
        
        duration_str = f"({r.get('duration', 0):.1f}s)" if not r.get("skipped") else ""
        print(f"  {status} {r['name']} [{r['skill']}] {duration_str}")
    
    print()
    
    # Failed checks detail
    if failed > 0:
        print(f"{Colors.BOLD}{Colors.RED}❌ FAILED CHECKS:{Colors.ENDC}")
        for r in results:
            if not r["passed"] and not r.get("skipped"):
                print(f"\n{Colors.RED}✗ {r['name']} ({r['skill']}){Colors.ENDC}")
                if r.get("error"):
                    print(f"  Error: {r['error'][:200]}")
        print()
    
    # Final verdict
    if failed > 0:
        print_error(f"VERIFICATION FAILED - {failed} check(s) need attention")
        print(f"\n{Colors.YELLOW}💡 Tip: Fix critical (Security, Lint) issues first{Colors.ENDC}")
        return False
    else:
        print_success("✨ ALL CHECKS PASSED - Ready for deployment! ✨")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="AGT-Kit Full Verification Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python .agent/scripts/verify_all.py . --url http://localhost:3000
  python .agent/scripts/verify_all.py . --url https://staging.example.com --no-e2e
        """
    )
    parser.add_argument("project", help="Project path to validate")
    parser.add_argument("--url", required=True, help="URL for performance & E2E checks")
    parser.add_argument("--no-e2e", action="store_true", help="Skip E2E tests")
    parser.add_argument("--stop-on-fail", action="store_true", help="Stop on first critical failure")
    
    args = parser.parse_args()
    
    project_path = Path(args.project).resolve()
    
    if not project_path.exists():
        print_error(f"Project path does not exist: {project_path}")
        sys.exit(1)
    
    project_info = detect_project_type(project_path)
    
    print_header("🚀 AGT-KIT FULL VERIFICATION SUITE")
    print(f"Project: {project_path}")
    print(f"Type: {project_info['type']}")
    print(f"URL: {args.url}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Relevant Categories: {', '.join(project_info['categories'])}")
    
    start_time = datetime.now()
    results = []
    
    # Run all verification categories
    for suite in sorted(VERIFICATION_SUITE, key=lambda x: x["priority"]):
        category = suite["category"]
        requires_url = suite.get("requires_url", False)
        
        # Skip if category not relevant to project type
        if category not in project_info["categories"]:
            continue
        
        # Skip if requires URL and not provided
        if requires_url and not args.url:
            continue
        
        # Skip E2E if flag set
        if args.no_e2e and category == "E2E Testing":
            continue
        
        print_header(f"📋 {category.upper()}")
        
        for check in suite["checks"]:
            result = run_script(check, project_path, args.url)
            result["category"] = category
            results.append(result)
            
            # Stop on critical failure if flag set
            if args.stop_on_fail and check["required"] and not result["passed"] and not result.get("skipped"):
                print_error(f"CRITICAL: {check['name']} failed. Stopping.")
                print_final_report(results, start_time, project_info)
                sys.exit(1)
    
    # Print final report
    all_passed = print_final_report(results, start_time, project_info)
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
