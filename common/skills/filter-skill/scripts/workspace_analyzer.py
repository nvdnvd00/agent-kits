#!/usr/bin/env python3
"""
Workspace Analyzer for Filter Skill

Analyzes workspace to detect techstack and recommend skill filtering.
This script provides structured JSON output for AI agents to process.

Usage:
    python3 workspace_analyzer.py [workspace_path]
    python3 workspace_analyzer.py .
    python3 workspace_analyzer.py /path/to/project
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# =============================================================================
# Detection Mappings
# =============================================================================

# Config files → Techstack detection
CONFIG_MAPPINGS = {
    "package.json": {"type": "package_manager", "tech": "nodejs"},
    "pubspec.yaml": {"type": "package_manager", "tech": "flutter"},
    "pyproject.toml": {"type": "package_manager", "tech": "python"},
    "requirements.txt": {"type": "package_manager", "tech": "python"},
    "Cargo.toml": {"type": "package_manager", "tech": "rust"},
    "go.mod": {"type": "package_manager", "tech": "go"},
    "build.gradle": {"type": "package_manager", "tech": "android"},
    "build.gradle.kts": {"type": "package_manager", "tech": "android"},
    "Podfile": {"type": "package_manager", "tech": "ios"},
    "composer.json": {"type": "package_manager", "tech": "php"},
    "Gemfile": {"type": "package_manager", "tech": "ruby"},
}

# Framework markers → Skills
FRAMEWORK_MAPPINGS = {
    "next.config.js": ["react-patterns", "seo-patterns", "frontend-design"],
    "next.config.mjs": ["react-patterns", "seo-patterns", "frontend-design"],
    "next.config.ts": ["react-patterns", "seo-patterns", "frontend-design"],
    "vite.config.js": ["react-patterns", "frontend-design"],
    "vite.config.ts": ["react-patterns", "frontend-design"],
    "angular.json": ["typescript-patterns", "frontend-design"],
    "nuxt.config.js": ["frontend-design", "seo-patterns"],
    "nuxt.config.ts": ["frontend-design", "seo-patterns"],
    "tailwind.config.js": ["tailwind-patterns"],
    "tailwind.config.ts": ["tailwind-patterns"],
    "tailwind.config.mjs": ["tailwind-patterns"],
    "Dockerfile": ["docker-patterns"],
    "docker-compose.yml": ["docker-patterns"],
    "docker-compose.yaml": ["docker-patterns"],
    ".gitlab-ci.yml": ["gitlab-ci-patterns"],
}

# Directory patterns → Skills
DIRECTORY_MAPPINGS = {
    ".github/workflows": ["github-actions"],
    "k8s": ["kubernetes-patterns"],
    "kubernetes": ["kubernetes-patterns"],
    "terraform": ["terraform-patterns"],
    "prisma": ["database-design", "postgres-patterns"],
}

# NPM dependencies → Skills (substring matching)
NPM_DEPENDENCY_MAPPINGS = {
    "react": ["react-patterns"],
    "next": ["react-patterns", "seo-patterns"],
    "@tanstack/react-query": ["react-patterns"],
    "vue": ["frontend-design"],
    "graphql": ["graphql-patterns"],
    "@apollo": ["graphql-patterns"],
    "redis": ["redis-patterns"],
    "ioredis": ["redis-patterns"],
    "pg": ["postgres-patterns"],
    "postgres": ["postgres-patterns"],
    "@prisma/client": ["database-design", "postgres-patterns"],
    "drizzle-orm": ["database-design"],
    "socket.io": ["realtime-patterns"],
    "ws": ["realtime-patterns"],
    "bullmq": ["queue-patterns"],
    "bee-queue": ["queue-patterns"],
    "passport": ["auth-patterns"],
    "@auth": ["auth-patterns"],
    "next-auth": ["auth-patterns"],
    "openai": ["ai-rag-patterns", "prompt-engineering"],
    "langchain": ["ai-rag-patterns"],
    "@langchain": ["ai-rag-patterns"],
    "playwright": ["e2e-testing"],
    "@playwright": ["e2e-testing"],
    "cypress": ["e2e-testing"],
    "jest": ["testing-patterns"],
    "vitest": ["testing-patterns"],
    "eslint": ["clean-code"],
    "prettier": ["clean-code"],
    "typescript": ["typescript-patterns"],
}

# All available skills (from ARCHITECTURE.md)
ALL_SKILLS = [
    "clean-code", "api-patterns", "database-design", "testing-patterns",
    "security-fundamentals", "performance-profiling", "brainstorming",
    "plan-writing", "systematic-debugging", "realtime-patterns",
    "multi-tenancy", "queue-patterns", "docker-patterns", "kubernetes-patterns",
    "auth-patterns", "github-actions", "gitlab-ci-patterns", "prompt-engineering",
    "react-patterns", "typescript-patterns", "e2e-testing", "postgres-patterns",
    "redis-patterns", "graphql-patterns", "ai-rag-patterns",
    "monitoring-observability", "terraform-patterns", "flutter-patterns",
    "react-native-patterns", "seo-patterns", "accessibility-patterns",
    "mermaid-diagrams", "i18n-localization", "mobile-design",
    "documentation-templates", "tailwind-patterns", "frontend-design",
    "ui-ux-pro-max", "nodejs-best-practices"
]

# Core skills that should NEVER be disabled
CORE_SKILLS = [
    "clean-code",
    "brainstorming", 
    "plan-writing",
    "systematic-debugging",
    "testing-patterns",
    "security-fundamentals"
]

# =============================================================================
# Analyzer Class
# =============================================================================

class WorkspaceAnalyzer:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path).resolve()
        self.detected_techs: List[str] = []
        self.detected_frameworks: List[str] = []
        self.recommended_skills: set = set()
        self.config_files_found: List[str] = []
        self.dependencies: Dict[str, List[str]] = {}
    
    def analyze(self) -> Dict[str, Any]:
        """Run full workspace analysis."""
        if not self.workspace.exists():
            return self._error(f"Workspace not found: {self.workspace}")
        
        # Step 1: Scan config files
        self._scan_config_files()
        
        # Step 2: Scan framework markers
        self._scan_framework_markers()
        
        # Step 3: Scan directories
        self._scan_directories()
        
        # Step 4: Parse dependencies
        self._parse_dependencies()
        
        # Step 5: Build recommendations
        return self._build_result()
    
    def _scan_config_files(self):
        """Scan for package manager config files."""
        for filename, info in CONFIG_MAPPINGS.items():
            filepath = self.workspace / filename
            if filepath.exists():
                self.config_files_found.append(filename)
                self.detected_techs.append(info["tech"])
    
    def _scan_framework_markers(self):
        """Scan for framework-specific config files."""
        for filename, skills in FRAMEWORK_MAPPINGS.items():
            filepath = self.workspace / filename
            if filepath.exists():
                self.config_files_found.append(filename)
                self.recommended_skills.update(skills)
                # Extract framework name
                framework = filename.split(".")[0].replace("_", "-")
                if framework not in ["Dockerfile", "docker-compose"]:
                    self.detected_frameworks.append(framework)
    
    def _scan_directories(self):
        """Scan for special directories."""
        for dirname, skills in DIRECTORY_MAPPINGS.items():
            dirpath = self.workspace / dirname
            if dirpath.exists() and dirpath.is_dir():
                self.config_files_found.append(f"{dirname}/")
                self.recommended_skills.update(skills)
    
    def _parse_dependencies(self):
        """Parse dependencies from package managers."""
        # Parse package.json
        package_json = self.workspace / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                
                all_deps = {}
                all_deps.update(data.get("dependencies", {}))
                all_deps.update(data.get("devDependencies", {}))
                
                self.dependencies["npm"] = list(all_deps.keys())
                
                # Match dependencies to skills
                for dep_name in all_deps.keys():
                    for pattern, skills in NPM_DEPENDENCY_MAPPINGS.items():
                        if pattern in dep_name:
                            self.recommended_skills.update(skills)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Parse pubspec.yaml (Flutter)
        pubspec = self.workspace / "pubspec.yaml"
        if pubspec.exists():
            self.recommended_skills.add("flutter-patterns")
            self.recommended_skills.add("mobile-design")
    
    def _build_result(self) -> Dict[str, Any]:
        """Build final analysis result."""
        # Add core skills (always recommended)
        self.recommended_skills.update(CORE_SKILLS)
        
        # Determine which skills to disable
        enabled = list(self.recommended_skills)
        disabled = [s for s in ALL_SKILLS if s not in enabled]
        
        # Remove core skills from disabled (safety check)
        disabled = [s for s in disabled if s not in CORE_SKILLS]
        
        return {
            "success": True,
            "analyzedAt": datetime.now().isoformat(),
            "workspacePath": str(self.workspace),
            "detection": {
                "configFiles": self.config_files_found,
                "technologies": list(set(self.detected_techs)),
                "frameworks": list(set(self.detected_frameworks)),
                "dependencies": self.dependencies
            },
            "recommendations": {
                "enable": sorted(enabled),
                "disable": sorted(disabled),
                "coreSkills": CORE_SKILLS
            },
            "summary": {
                "totalSkillsAvailable": len(ALL_SKILLS),
                "recommendedEnabled": len(enabled),
                "recommendedDisabled": len(disabled),
                "coreSkillsCount": len(CORE_SKILLS)
            }
        }
    
    def _error(self, message: str) -> Dict[str, Any]:
        """Return error result."""
        return {
            "success": False,
            "error": message,
            "analyzedAt": datetime.now().isoformat()
        }


# =============================================================================
# Main
# =============================================================================

def main():
    # Get workspace path from args or use current directory
    if len(sys.argv) > 1:
        workspace_path = sys.argv[1]
    else:
        workspace_path = "."
    
    analyzer = WorkspaceAnalyzer(workspace_path)
    result = analyzer.analyze()
    
    # Output as JSON for AI to parse
    print(json.dumps(result, indent=2))
    
    # Exit code based on success
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
