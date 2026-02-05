#!/usr/bin/env python3
"""
Techstack Scanner for Common Skills Layer

Analyzes workspace to detect technologies, frameworks, and dependencies.
Outputs structured JSON profile for filter-skill and filter-agent to consume.

Usage:
    python3 techstack_scanner.py [workspace_path]
    python3 techstack_scanner.py .
    python3 techstack_scanner.py /path/to/project
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# =============================================================================
# Detection Mappings
# =============================================================================

# Config files → Language/Platform detection
CONFIG_TO_LANGUAGE = {
    "package.json": "nodejs",
    "tsconfig.json": "typescript",
    "pubspec.yaml": "dart",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "Cargo.toml": "rust",
    "go.mod": "go",
    "build.gradle": "kotlin",
    "build.gradle.kts": "kotlin",
    "Podfile": "swift",
    "composer.json": "php",
    "Gemfile": "ruby",
}

# Framework markers → Framework name + Category
FRAMEWORK_MARKERS = {
    "next.config.js": {"framework": "nextjs", "category": "frontend"},
    "next.config.mjs": {"framework": "nextjs", "category": "frontend"},
    "next.config.ts": {"framework": "nextjs", "category": "frontend"},
    "vite.config.js": {"framework": "vite", "category": "frontend"},
    "vite.config.ts": {"framework": "vite", "category": "frontend"},
    "angular.json": {"framework": "angular", "category": "frontend"},
    "nuxt.config.js": {"framework": "nuxtjs", "category": "frontend"},
    "nuxt.config.ts": {"framework": "nuxtjs", "category": "frontend"},
    "tailwind.config.js": {"framework": "tailwindcss", "category": "styling"},
    "tailwind.config.ts": {"framework": "tailwindcss", "category": "styling"},
    "tailwind.config.mjs": {"framework": "tailwindcss", "category": "styling"},
    "Dockerfile": {"framework": "docker", "category": "devops"},
    "docker-compose.yml": {"framework": "docker-compose", "category": "devops"},
    "docker-compose.yaml": {"framework": "docker-compose", "category": "devops"},
    ".gitlab-ci.yml": {"framework": "gitlab-ci", "category": "cicd"},
    "pubspec.yaml": {"framework": "flutter", "category": "mobile"},
}

# Directory patterns → Framework + Category
DIRECTORY_MARKERS = {
    ".github/workflows": {"framework": "github-actions", "category": "cicd"},
    "k8s": {"framework": "kubernetes", "category": "devops"},
    "kubernetes": {"framework": "kubernetes", "category": "devops"},
    "terraform": {"framework": "terraform", "category": "iac"},
    "prisma": {"framework": "prisma", "category": "database"},
}

# NPM dependencies → Category detection
NPM_CATEGORY_MAPPINGS = {
    # Frontend
    "react": "frontend",
    "react-dom": "frontend",
    "vue": "frontend",
    "@angular/core": "frontend",
    "svelte": "frontend",
    # Backend
    "express": "backend",
    "fastify": "backend",
    "@nestjs/core": "backend",
    "koa": "backend",
    "hono": "backend",
    # Database
    "@prisma/client": "database",
    "drizzle-orm": "database",
    "pg": "database",
    "mysql2": "database",
    "mongodb": "database",
    "mongoose": "database",
    "redis": "database",
    "ioredis": "database",
    # AI
    "openai": "ai",
    "langchain": "ai",
    "@langchain/core": "ai",
    "@anthropic-ai/sdk": "ai",
    # Realtime
    "socket.io": "realtime",
    "socket.io-client": "realtime",
    "ws": "realtime",
    # Queue
    "bullmq": "queue",
    "bull": "queue",
    "bee-queue": "queue",
    "amqplib": "queue",
    # Testing
    "jest": "testing",
    "vitest": "testing",
    "playwright": "testing",
    "@playwright/test": "testing",
    "cypress": "testing",
    # Auth
    "passport": "auth",
    "next-auth": "auth",
    "@auth/core": "auth",
    # GraphQL
    "graphql": "graphql",
    "@apollo/server": "graphql",
    "@apollo/client": "graphql",
}

# Frameworks detected from dependencies
NPM_FRAMEWORK_MAPPINGS = {
    "next": "nextjs",
    "react": "react",
    "vue": "vue",
    "@angular/core": "angular",
    "express": "express",
    "fastify": "fastify",
    "@nestjs/core": "nestjs",
    "socket.io": "socketio",
    "tailwindcss": "tailwindcss",
    "@prisma/client": "prisma",
    "drizzle-orm": "drizzle",
}

# =============================================================================
# Scanner Class
# =============================================================================

class TechstackScanner:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path).resolve()
        self.config_files: List[str] = []
        self.languages: set = set()
        self.frameworks: set = set()
        self.databases: List[str] = []
        self.tools: List[str] = []
        self.dependencies: Dict[str, List[str]] = {}
        self.categories: Dict[str, bool] = {
            "frontend": False,
            "backend": False,
            "mobile": False,
            "database": False,
            "devops": False,
            "ai": False,
            "realtime": False,
            "queue": False,
            "graphql": False,
            "auth": False,
            "testing": False,
        }

    def scan(self) -> Dict[str, Any]:
        """Run full workspace scan."""
        if not self.workspace.exists():
            return self._error(f"Workspace not found: {self.workspace}")

        # Step 1: Scan config files for languages
        self._scan_config_files()

        # Step 2: Scan framework markers
        self._scan_framework_markers()

        # Step 3: Scan directories
        self._scan_directories()

        # Step 4: Parse dependencies
        self._parse_dependencies()

        # Step 5: Build result
        return self._build_result()

    def _scan_config_files(self):
        """Scan for config files and detect languages."""
        for filename, language in CONFIG_TO_LANGUAGE.items():
            filepath = self.workspace / filename
            if filepath.exists():
                self.config_files.append(filename)
                self.languages.add(language)

    def _scan_framework_markers(self):
        """Scan for framework-specific config files."""
        for filename, info in FRAMEWORK_MARKERS.items():
            filepath = self.workspace / filename
            if filepath.exists():
                self.config_files.append(filename)
                self.frameworks.add(info["framework"])
                self._set_category(info["category"])

    def _scan_directories(self):
        """Scan for special directories."""
        for dirname, info in DIRECTORY_MARKERS.items():
            dirpath = self.workspace / dirname
            if dirpath.exists() and dirpath.is_dir():
                self.config_files.append(f"{dirname}/")
                self.frameworks.add(info["framework"])
                self._set_category(info["category"])
                self.tools.append(info["framework"])

    def _parse_dependencies(self):
        """Parse dependencies from package managers."""
        # Parse package.json
        package_json = self.workspace / "package.json"
        if package_json.exists():
            try:
                with open(package_json, "r") as f:
                    data = json.load(f)

                all_deps = {}
                all_deps.update(data.get("dependencies", {}))
                all_deps.update(data.get("devDependencies", {}))

                self.dependencies["npm"] = list(all_deps.keys())

                # Detect categories and frameworks from deps
                for dep_name in all_deps.keys():
                    # Check category
                    for pattern, category in NPM_CATEGORY_MAPPINGS.items():
                        if pattern == dep_name or dep_name.startswith(f"{pattern}/"):
                            self._set_category(category)

                    # Check framework
                    for pattern, framework in NPM_FRAMEWORK_MAPPINGS.items():
                        if pattern == dep_name:
                            self.frameworks.add(framework)

            except (json.JSONDecodeError, IOError):
                pass

        # Parse pubspec.yaml (Flutter)
        pubspec = self.workspace / "pubspec.yaml"
        if pubspec.exists():
            self.frameworks.add("flutter")
            self._set_category("mobile")

        # Parse Podfile (iOS)
        podfile = self.workspace / "Podfile"
        if podfile.exists():
            self._set_category("mobile")

        # Parse build.gradle (Android)
        gradle = self.workspace / "build.gradle"
        if gradle.exists() or (self.workspace / "build.gradle.kts").exists():
            self._set_category("mobile")

    def _set_category(self, category: str):
        """Set category flag to True."""
        # Map sub-categories to main categories
        category_map = {
            "frontend": "frontend",
            "backend": "backend",
            "mobile": "mobile",
            "database": "database",
            "devops": "devops",
            "iac": "devops",
            "cicd": "devops",
            "ai": "ai",
            "realtime": "realtime",
            "queue": "queue",
            "graphql": "graphql",
            "auth": "auth",
            "testing": "testing",
            "styling": "frontend",  # Styling is part of frontend
        }
        main_category = category_map.get(category, category)
        if main_category in self.categories:
            self.categories[main_category] = True

    def _build_result(self) -> Dict[str, Any]:
        """Build final scan result."""
        # Detect databases from frameworks
        db_frameworks = ["prisma", "drizzle", "mongodb", "postgresql", "mysql"]
        for fw in self.frameworks:
            if fw in db_frameworks:
                self.databases.append(fw)

        return {
            "success": True,
            "analyzedAt": datetime.now().isoformat(),
            "workspacePath": str(self.workspace),
            "detection": {
                "configFiles": sorted(set(self.config_files)),
                "languages": sorted(self.languages),
                "frameworks": sorted(self.frameworks),
                "databases": sorted(set(self.databases)),
                "tools": sorted(set(self.tools)),
                "dependencies": self.dependencies,
            },
            "categories": self.categories,
        }

    def _error(self, message: str) -> Dict[str, Any]:
        """Return error result."""
        return {
            "success": False,
            "error": message,
            "analyzedAt": datetime.now().isoformat(),
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

    scanner = TechstackScanner(workspace_path)
    result = scanner.scan()

    # Output as JSON for AI to parse
    print(json.dumps(result, indent=2))

    # Exit code based on success
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
