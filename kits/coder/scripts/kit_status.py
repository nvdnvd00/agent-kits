#!/usr/bin/env python3
"""
AGT-Kit Status Reporter
========================

Reports the status of the AGT-Kit installation:
- Lists all agents and their assigned skills
- Lists all available skills
- Lists all workflows
- Validates kit integrity

Usage:
    python .agent/scripts/kit_status.py
    python .agent/scripts/kit_status.py --validate
    python .agent/scripts/kit_status.py --json
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any

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
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def find_kit_root() -> Path:
    """Find the .agent directory from current location or script location."""
    # Try from script location
    script_dir = Path(__file__).parent
    agent_dir = script_dir.parent
    
    if (agent_dir / "ARCHITECTURE.md").exists():
        return agent_dir
    
    # Try from current working directory
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        agent_dir = parent / ".agent"
        if agent_dir.exists() and (agent_dir / "ARCHITECTURE.md").exists():
            return agent_dir
    
    return None


def parse_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = file_path.read_text()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                result = {}
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        result[key.strip()] = value.strip()
                return result
    except:
        pass
    return {}


def get_agents(agent_dir: Path) -> List[Dict[str, Any]]:
    """Get list of agents with their metadata."""
    agents = []
    agents_path = agent_dir / "agents"
    
    if not agents_path.exists():
        return agents
    
    for agent_file in agents_path.glob("*.md"):
        frontmatter = parse_frontmatter(agent_file)
        skills = frontmatter.get("skills", "").replace("[", "").replace("]", "").split(",")
        skills = [s.strip() for s in skills if s.strip()]
        
        agents.append({
            "name": agent_file.stem,
            "file": str(agent_file.relative_to(agent_dir)),
            "description": frontmatter.get("description", ""),
            "skills": skills,
        })
    
    return sorted(agents, key=lambda x: x["name"])


def get_skills(agent_dir: Path) -> List[Dict[str, Any]]:
    """Get list of skills with their metadata."""
    skills = []
    skills_path = agent_dir / "skills"
    
    if not skills_path.exists():
        return skills
    
    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        frontmatter = parse_frontmatter(skill_md)
        
        # Check for scripts
        scripts_path = skill_dir / "scripts"
        has_scripts = scripts_path.exists() and any(scripts_path.glob("*.py"))
        
        skills.append({
            "name": skill_dir.name,
            "file": str(skill_md.relative_to(agent_dir)),
            "description": frontmatter.get("description", ""),
            "has_scripts": has_scripts,
        })
    
    return sorted(skills, key=lambda x: x["name"])


def get_workflows(agent_dir: Path) -> List[Dict[str, Any]]:
    """Get list of workflows."""
    workflows = []
    workflows_path = agent_dir / "workflows"
    
    if not workflows_path.exists():
        return workflows
    
    for workflow_file in workflows_path.glob("*.md"):
        frontmatter = parse_frontmatter(workflow_file)
        
        workflows.append({
            "name": workflow_file.stem,
            "command": f"/{workflow_file.stem}",
            "file": str(workflow_file.relative_to(agent_dir)),
            "description": frontmatter.get("description", ""),
        })
    
    return sorted(workflows, key=lambda x: x["name"])


def validate_kit(agent_dir: Path, agents: List, skills: List, workflows: List) -> Dict[str, Any]:
    """Validate kit integrity."""
    issues = []
    warnings = []
    
    skill_names = {s["name"] for s in skills}
    
    # Check agent skill references
    for agent in agents:
        for skill in agent.get("skills", []):
            if skill and skill not in skill_names:
                issues.append(f"Agent '{agent['name']}' references missing skill: {skill}")
    
    # Check for skills without SKILL.md
    skills_path = agent_dir / "skills"
    if skills_path.exists():
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir() and not (skill_dir / "SKILL.md").exists():
                warnings.append(f"Skill directory '{skill_dir.name}' missing SKILL.md")
    
    # Check ARCHITECTURE.md exists
    if not (agent_dir / "ARCHITECTURE.md").exists():
        issues.append("Missing ARCHITECTURE.md")
    
    # Check required files
    required_files = ["ARCHITECTURE.md"]
    for rf in required_files:
        if not (agent_dir / rf).exists():
            issues.append(f"Missing required file: {rf}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
    }


def print_report(agents: List, skills: List, workflows: List, validation: Dict):
    """Print formatted status report."""
    print_header("🤖 AGT-KIT STATUS REPORT")
    
    # Statistics
    print(f"{Colors.BOLD}📊 Statistics{Colors.ENDC}")
    print(f"  Agents:    {len(agents)}")
    print(f"  Skills:    {len(skills)}")
    print(f"  Workflows: {len(workflows)}")
    print()
    
    # Agents
    print(f"{Colors.BOLD}🤖 Agents ({len(agents)}){Colors.ENDC}")
    for agent in agents:
        skill_count = len(agent.get("skills", []))
        print(f"  • {agent['name']} ({skill_count} skills)")
    print()
    
    # Skills with scripts
    skills_with_scripts = [s for s in skills if s.get("has_scripts")]
    print(f"{Colors.BOLD}🧩 Skills with Scripts ({len(skills_with_scripts)}/{len(skills)}){Colors.ENDC}")
    for skill in skills_with_scripts:
        print(f"  • {skill['name']} ✓")
    print()
    
    # Workflows
    print(f"{Colors.BOLD}🔄 Workflows ({len(workflows)}){Colors.ENDC}")
    for workflow in workflows:
        print(f"  • {workflow['command']} - {workflow.get('description', 'No description')[:50]}")
    print()
    
    # Validation
    print(f"{Colors.BOLD}✅ Validation{Colors.ENDC}")
    if validation["valid"]:
        print_success("Kit integrity check passed")
    else:
        for issue in validation["issues"]:
            print_error(issue)
    
    for warning in validation.get("warnings", []):
        print_warning(warning)


def main():
    parser = argparse.ArgumentParser(
        description="AGT-Kit Status Reporter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--validate", action="store_true", help="Run validation checks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    agent_dir = find_kit_root()
    
    if not agent_dir:
        print_error("Could not find .agent directory")
        sys.exit(1)
    
    # Gather data
    agents = get_agents(agent_dir)
    skills = get_skills(agent_dir)
    workflows = get_workflows(agent_dir)
    validation = validate_kit(agent_dir, agents, skills, workflows)
    
    if args.json:
        output = {
            "kit_path": str(agent_dir),
            "statistics": {
                "agents": len(agents),
                "skills": len(skills),
                "workflows": len(workflows),
            },
            "agents": agents,
            "skills": skills,
            "workflows": workflows,
            "validation": validation,
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(agents, skills, workflows, validation)
    
    sys.exit(0 if validation["valid"] else 1)


if __name__ == "__main__":
    main()
