#!/usr/bin/env python3
"""
Skills Manager - Manage AGT-Kit skills dynamically
===================================================

Enable/disable skills without deleting them.

Usage:
    python3 .agent/scripts/skills_manager.py list          # List active skills
    python3 .agent/scripts/skills_manager.py disabled      # List disabled skills
    python3 .agent/scripts/skills_manager.py enable SKILL  # Enable a skill
    python3 .agent/scripts/skills_manager.py disable SKILL # Disable a skill
    python3 .agent/scripts/skills_manager.py search QUERY  # Search skills
    python3 .agent/scripts/skills_manager.py info SKILL    # Show skill details
"""

import sys
import os
import re
from pathlib import Path

# Fix console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except:
    pass

# Paths
SCRIPT_DIR = Path(__file__).parent
AGENT_DIR = SCRIPT_DIR.parent
SKILLS_DIR = AGENT_DIR / "skills"
DISABLED_DIR = SKILLS_DIR / ".disabled"


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md."""
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return {}
    
    metadata = {}
    for line in fm_match.group(1).split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata


def get_skill_info(skill_path: Path) -> dict:
    """Get information about a skill."""
    skill_md = skill_path / "SKILL.md"
    info = {
        "name": skill_path.name,
        "path": str(skill_path),
        "has_skill_md": skill_md.exists(),
        "has_scripts": (skill_path / "scripts").exists(),
        "description": "",
    }
    
    if skill_md.exists():
        try:
            content = skill_md.read_text(encoding='utf-8')
            metadata = parse_frontmatter(content)
            info["description"] = metadata.get("description", "")[:80]
        except:
            pass
    
    return info


def list_active():
    """List all active skills."""
    print("\n🟢 Active Skills\n" + "="*50)
    
    skills = sorted([
        d for d in SKILLS_DIR.iterdir() 
        if d.is_dir() and not d.name.startswith('.')
    ], key=lambda x: x.name)
    
    with_scripts = 0
    for skill in skills:
        info = get_skill_info(skill)
        script_icon = "📜" if info["has_scripts"] else "  "
        desc = f" - {info['description']}" if info["description"] else ""
        print(f"  {script_icon} {skill.name}{desc}")
        if info["has_scripts"]:
            with_scripts += 1
    
    print(f"\n✅ Total: {len(skills)} skills ({with_scripts} with scripts)")


def list_disabled():
    """List all disabled skills."""
    if not DISABLED_DIR.exists():
        print("❌ No disabled skills")
        return
    
    print("\n⚪ Disabled Skills\n" + "="*50)
    
    disabled = sorted([d for d in DISABLED_DIR.iterdir() if d.is_dir()])
    
    for skill in disabled:
        print(f"  • {skill.name}")
    
    print(f"\n📊 Total: {len(disabled)} disabled skills")


def enable_skill(skill_name: str):
    """Enable a disabled skill."""
    source = DISABLED_DIR / skill_name
    target = SKILLS_DIR / skill_name
    
    if not source.exists():
        print(f"❌ Skill '{skill_name}' not found in .disabled/")
        return False
    
    if target.exists():
        print(f"⚠️  Skill '{skill_name}' already active")
        return False
    
    source.rename(target)
    print(f"✅ Enabled: {skill_name}")
    return True


def disable_skill(skill_name: str):
    """Disable an active skill."""
    source = SKILLS_DIR / skill_name
    target = DISABLED_DIR / skill_name
    
    if not source.exists():
        print(f"❌ Skill '{skill_name}' not found")
        return False
    
    if source.name.startswith('.'):
        print(f"⚠️  Cannot disable system directory")
        return False
    
    DISABLED_DIR.mkdir(exist_ok=True)
    source.rename(target)
    print(f"✅ Disabled: {skill_name}")
    return True


def search_skills(query: str):
    """Search skills by name or description."""
    print(f"\n🔍 Searching for '{query}'\n" + "="*50)
    
    query_lower = query.lower()
    matches = []
    
    for skill_path in SKILLS_DIR.iterdir():
        if not skill_path.is_dir() or skill_path.name.startswith('.'):
            continue
        
        info = get_skill_info(skill_path)
        
        # Search in name and description
        if query_lower in skill_path.name.lower() or query_lower in info["description"].lower():
            matches.append(info)
    
    if matches:
        for info in matches:
            script_icon = "📜" if info["has_scripts"] else "  "
            desc = f" - {info['description']}" if info["description"] else ""
            print(f"  {script_icon} {info['name']}{desc}")
        print(f"\n✅ Found {len(matches)} matching skills")
    else:
        print("  No skills found matching your query")


def show_skill_info(skill_name: str):
    """Show detailed info about a skill."""
    skill_path = SKILLS_DIR / skill_name
    
    if not skill_path.exists():
        print(f"❌ Skill '{skill_name}' not found")
        return
    
    info = get_skill_info(skill_path)
    skill_md = skill_path / "SKILL.md"
    
    print(f"\n📦 Skill: {skill_name}\n" + "="*50)
    print(f"Path: {info['path']}")
    print(f"Has SKILL.md: {'✅' if info['has_skill_md'] else '❌'}")
    print(f"Has Scripts: {'✅' if info['has_scripts'] else '❌'}")
    
    if info['has_scripts']:
        scripts_dir = skill_path / "scripts"
        scripts = list(scripts_dir.glob("*.py"))
        print(f"\nScripts ({len(scripts)}):")
        for script in scripts:
            print(f"  • {script.name}")
    
    if skill_md.exists():
        try:
            content = skill_md.read_text(encoding='utf-8')
            metadata = parse_frontmatter(content)
            if metadata.get("description"):
                print(f"\nDescription:\n  {metadata['description']}")
        except:
            pass


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_active()
    elif command == "disabled":
        list_disabled()
    elif command == "enable":
        if len(sys.argv) < 3:
            print("❌ Usage: skills_manager.py enable SKILL_NAME")
            sys.exit(1)
        enable_skill(sys.argv[2])
    elif command == "disable":
        if len(sys.argv) < 3:
            print("❌ Usage: skills_manager.py disable SKILL_NAME")
            sys.exit(1)
        disable_skill(sys.argv[2])
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Usage: skills_manager.py search QUERY")
            sys.exit(1)
        search_skills(sys.argv[2])
    elif command == "info":
        if len(sys.argv) < 3:
            print("❌ Usage: skills_manager.py info SKILL_NAME")
            sys.exit(1)
        show_skill_info(sys.argv[2])
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
