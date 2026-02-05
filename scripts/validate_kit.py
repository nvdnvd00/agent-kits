#!/usr/bin/env python3
"""
Kit Structure Validator
Validates a kit against the standard KIT_SPEC.md requirements.

Usage:
    python3 scripts/validate_kit.py kits/<kit-name>
    python3 scripts/validate_kit.py kits/coder --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    passed: bool
    message: str
    category: str
    severity: str  # ERROR, WARNING, INFO


class KitValidator:
    """Validates kit structure against KIT_SPEC.md standards."""
    
    REQUIRED_RULE_FILES = ["GEMINI.md", "CLAUDE.md", "CURSOR.md", "AGENTS.md"]
    REQUIRED_DIRS = ["agents", "skills", "rules"]
    RECOMMENDED_DIRS = ["workflows", "scripts"]
    
    def __init__(self, kit_path: str, verbose: bool = False):
        self.kit_path = Path(kit_path)
        self.verbose = verbose
        self.results: list[ValidationResult] = []
        self.stats = {
            "agents": 0,
            "skills": 0,
            "workflows": 0,
            "scripts": 0,
            "rule_files": 0,
        }
    
    def add_result(self, passed: bool, message: str, category: str, severity: str = "ERROR"):
        self.results.append(ValidationResult(passed, message, category, severity))
    
    def validate_all(self) -> bool:
        """Run all validations and return overall result."""
        print(f"\n🔍 Validating kit: {self.kit_path}\n")
        print("=" * 60)
        
        # Check kit exists
        if not self.kit_path.exists():
            self.add_result(False, f"Kit path does not exist: {self.kit_path}", "structure")
            self._print_results()
            return False
        
        # Structure validations
        self._validate_structure()
        self._validate_architecture_md()
        self._validate_rules_folder()
        self._validate_agents()
        self._validate_skills()
        self._validate_workflows()
        self._validate_path_references()
        
        # Print results
        self._print_results()
        
        # Return overall result
        errors = [r for r in self.results if not r.passed and r.severity == "ERROR"]
        return len(errors) == 0
    
    def _validate_structure(self):
        """Validate directory structure."""
        print("\n📂 Checking directory structure...")
        
        # Required directories
        for dir_name in self.REQUIRED_DIRS:
            dir_path = self.kit_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.add_result(True, f"Required directory exists: {dir_name}/", "structure", "INFO")
            else:
                self.add_result(False, f"Missing required directory: {dir_name}/", "structure")
        
        # Recommended directories
        for dir_name in self.RECOMMENDED_DIRS:
            dir_path = self.kit_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.add_result(True, f"Recommended directory exists: {dir_name}/", "structure", "INFO")
            else:
                self.add_result(True, f"Optional directory missing: {dir_name}/ (recommended)", "structure", "WARNING")
    
    def _validate_architecture_md(self):
        """Validate ARCHITECTURE.md exists and has required sections."""
        print("\n📄 Checking ARCHITECTURE.md...")
        
        arch_path = self.kit_path / "ARCHITECTURE.md"
        if not arch_path.exists():
            self.add_result(False, "Missing required file: ARCHITECTURE.md", "content")
            return
        
        self.add_result(True, "ARCHITECTURE.md exists", "content", "INFO")
        
        content = arch_path.read_text(encoding="utf-8")
        
        # Check required sections
        required_sections = [
            ("Overview", r"##.*Overview"),
            ("Agents", r"##.*Agents"),
            ("Skills", r"##.*Skills"),
            ("Statistics", r"##.*Statistics"),
        ]
        
        for section_name, pattern in required_sections:
            if re.search(pattern, content, re.IGNORECASE):
                self.add_result(True, f"Section found: {section_name}", "content", "INFO")
            else:
                self.add_result(False, f"Missing section in ARCHITECTURE.md: {section_name}", "content")
    
    def _validate_rules_folder(self):
        """Validate rules folder and required rule files."""
        print("\n📜 Checking rules folder...")
        
        rules_path = self.kit_path / "rules"
        if not rules_path.exists():
            self.add_result(False, "Missing rules/ folder", "rules")
            return
        
        # Define frontmatter requirements per tool
        # - GEMINI.md: requires "trigger:" frontmatter
        # - CURSOR.md: requires "description:" or "alwaysApply:" frontmatter
        # - CLAUDE.md: no frontmatter required (plain markdown)
        # - AGENTS.md: no frontmatter required (plain markdown)
        frontmatter_requirements = {
            "GEMINI.md": {"required": True, "fields": ["trigger:"]},
            "CURSOR.md": {"required": True, "fields": ["description:", "alwaysApply:"]},
            "CLAUDE.md": {"required": False, "fields": []},
            "AGENTS.md": {"required": False, "fields": []},
        }
        
        for rule_file in self.REQUIRED_RULE_FILES:
            rule_path = rules_path / rule_file
            if rule_path.exists():
                self.stats["rule_files"] += 1
                self.add_result(True, f"Rule file exists: {rule_file}", "rules", "INFO")
                
                content = rule_path.read_text(encoding="utf-8")
                requirements = frontmatter_requirements.get(rule_file, {"required": False, "fields": []})
                
                if requirements["required"]:
                    # Check frontmatter for tools that require it
                    if content.startswith("---"):
                        # Check for required fields
                        has_required_field = any(field in content[:500] for field in requirements["fields"])
                        if has_required_field:
                            self.add_result(True, f"Frontmatter valid: {rule_file}", "rules", "INFO")
                        else:
                            fields_str = " or ".join(requirements["fields"])
                            self.add_result(False, f"Missing {fields_str} in frontmatter: {rule_file}", "rules")
                    else:
                        self.add_result(False, f"Missing YAML frontmatter: {rule_file}", "rules")
                else:
                    # Claude and Codex don't require frontmatter
                    if self.verbose:
                        self.add_result(True, f"Rule file OK (no frontmatter required): {rule_file}", "rules", "INFO")
            else:
                self.add_result(False, f"Missing required rule file: {rule_file}", "rules")
    
    def _validate_agents(self):
        """Validate agent files."""
        print("\n🤖 Checking agents...")
        
        agents_path = self.kit_path / "agents"
        if not agents_path.exists():
            return
        
        agent_files = list(agents_path.glob("*.md"))
        self.stats["agents"] = len(agent_files)
        
        if len(agent_files) == 0:
            self.add_result(False, "No agent files found in agents/", "agents")
            return
        
        self.add_result(True, f"Found {len(agent_files)} agent(s)", "agents", "INFO")
        
        # Check each agent file
        for agent_file in agent_files:
            content = agent_file.read_text(encoding="utf-8")
            
            # Check frontmatter
            if not content.startswith("---"):
                self.add_result(False, f"Missing frontmatter: {agent_file.name}", "agents")
                continue
            
            # Check required frontmatter fields
            frontmatter_end = content.find("---", 3)
            if frontmatter_end == -1:
                self.add_result(False, f"Invalid frontmatter: {agent_file.name}", "agents")
                continue
            
            frontmatter = content[3:frontmatter_end]
            required_fields = ["name:", "description:", "skills:"]
            
            for field in required_fields:
                if field in frontmatter:
                    if self.verbose:
                        self.add_result(True, f"{agent_file.name}: has {field}", "agents", "INFO")
                else:
                    self.add_result(False, f"{agent_file.name}: missing {field}", "agents", "WARNING")
    
    def _validate_skills(self):
        """Validate skill folders and SKILL.md files."""
        print("\n🧩 Checking skills...")
        
        skills_path = self.kit_path / "skills"
        if not skills_path.exists():
            return
        
        skill_dirs = [d for d in skills_path.iterdir() if d.is_dir()]
        self.stats["skills"] = len(skill_dirs)
        
        if len(skill_dirs) == 0:
            self.add_result(False, "No skill directories found in skills/", "skills")
            return
        
        self.add_result(True, f"Found {len(skill_dirs)} skill(s)", "skills", "INFO")
        
        # Check each skill has SKILL.md
        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                self.add_result(False, f"Missing SKILL.md in: {skill_dir.name}/", "skills")
                continue
            
            content = skill_md.read_text(encoding="utf-8")
            
            # Check frontmatter
            if not content.startswith("---"):
                self.add_result(False, f"Missing frontmatter: {skill_dir.name}/SKILL.md", "skills")
                continue
            
            # Check required fields
            frontmatter_end = content.find("---", 3)
            if frontmatter_end != -1:
                frontmatter = content[3:frontmatter_end]
                if "name:" in frontmatter and "description:" in frontmatter:
                    if self.verbose:
                        self.add_result(True, f"{skill_dir.name}: valid frontmatter", "skills", "INFO")
                else:
                    self.add_result(False, f"{skill_dir.name}: missing name/description", "skills", "WARNING")
    
    def _validate_workflows(self):
        """Validate workflow files."""
        print("\n🔄 Checking workflows...")
        
        workflows_path = self.kit_path / "workflows"
        if not workflows_path.exists():
            self.add_result(True, "No workflows/ folder (optional)", "workflows", "WARNING")
            return
        
        workflow_files = [f for f in workflows_path.glob("*.md") if f.name != ".gitkeep"]
        self.stats["workflows"] = len(workflow_files)
        
        if len(workflow_files) == 0:
            self.add_result(True, "No workflow files (optional)", "workflows", "WARNING")
            return
        
        self.add_result(True, f"Found {len(workflow_files)} workflow(s)", "workflows", "INFO")
        
        # Check each workflow has description frontmatter
        for wf_file in workflow_files:
            content = wf_file.read_text(encoding="utf-8")
            if content.startswith("---") and "description:" in content[:500]:
                if self.verbose:
                    self.add_result(True, f"{wf_file.name}: valid frontmatter", "workflows", "INFO")
            else:
                self.add_result(False, f"Missing description in: {wf_file.name}", "workflows", "WARNING")
    
    def _validate_path_references(self):
        """Check that path references use .agent/ placeholder."""
        print("\n🔗 Checking path references...")
        
        # Check rules files
        rules_path = self.kit_path / "rules"
        if not rules_path.exists():
            return
        
        invalid_refs = []
        for rule_file in rules_path.glob("*.md"):
            content = rule_file.read_text(encoding="utf-8")
            
            # Check for hardcoded tool paths that should be .agent/
            # Skip checking for the actual tool-specific paths in content
            # as CURSOR.md may legitimately mention .cursor/ for documentation
            
            # Check that the file uses .agent/ for path references
            if ".agent/" in content:
                if self.verbose:
                    self.add_result(True, f"{rule_file.name}: uses .agent/ placeholder", "paths", "INFO")
        
        if not invalid_refs:
            self.add_result(True, "Path references look valid", "paths", "INFO")
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("\n📊 VALIDATION RESULTS\n")
        
        # Group by category
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)
        
        # Print by category
        for category, results in categories.items():
            if self.verbose or any(not r.passed for r in results):
                print(f"\n{category.upper()}:")
                for r in results:
                    if self.verbose or not r.passed:
                        icon = "✅" if r.passed else ("⚠️" if r.severity == "WARNING" else "❌")
                        print(f"  {icon} {r.message}")
        
        # Summary
        errors = [r for r in self.results if not r.passed and r.severity == "ERROR"]
        warnings = [r for r in self.results if not r.passed and r.severity == "WARNING"]
        
        print("\n" + "=" * 60)
        print("\n📈 STATISTICS")
        print(f"  Agents:     {self.stats['agents']}")
        print(f"  Skills:     {self.stats['skills']}")
        print(f"  Workflows:  {self.stats['workflows']}")
        print(f"  Rule Files: {self.stats['rule_files']}/4")
        
        print("\n" + "=" * 60)
        if errors:
            print(f"\n❌ FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
            print("\nFix the errors above and run validation again.")
        elif warnings:
            print(f"\n⚠️ PASSED with {len(warnings)} warning(s)")
            print("\nConsider addressing the warnings for a complete kit.")
        else:
            print("\n✅ PASSED: Kit structure is valid!")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate kit structure against KIT_SPEC.md standards",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/validate_kit.py kits/coder
  python3 scripts/validate_kit.py kits/coder --verbose
  python3 scripts/validate_kit.py kits/my-new-kit -v
        """
    )
    parser.add_argument("kit_path", help="Path to kit directory (e.g., kits/coder)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all checks, not just failures")
    
    args = parser.parse_args()
    
    validator = KitValidator(args.kit_path, verbose=args.verbose)
    success = validator.validate_all()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
