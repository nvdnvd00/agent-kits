#!/usr/bin/env python3
"""
Schema Validator - Database schema validation for AGT-Kit
==========================================================

Validates Prisma, Drizzle, TypeORM schemas and checks for common issues.

Usage:
    python3 .agent/skills/database-design/scripts/schema_validator.py <project_path>

Checks:
    - Prisma schema syntax and conventions
    - Missing relations and indexes
    - Naming conventions (PascalCase models, camelCase fields)
    - Required fields (id, createdAt, updatedAt)
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


def find_schema_files(project_path: Path) -> List[tuple]:
    """Find database schema files."""
    schemas = []
    
    # Prisma
    for f in project_path.glob('**/prisma/schema.prisma'):
        if 'node_modules' not in str(f):
            schemas.append(('prisma', f))
    
    # Drizzle
    for pattern in ['**/drizzle/*.ts', '**/db/schema*.ts', '**/schema/*.ts']:
        for f in project_path.glob(pattern):
            if 'node_modules' not in str(f) and ('schema' in f.name.lower() or 'table' in f.name.lower()):
                schemas.append(('drizzle', f))
    
    # TypeORM entities
    for f in project_path.glob('**/entities/*.ts'):
        if 'node_modules' not in str(f):
            schemas.append(('typeorm', f))
    
    return schemas[:15]  # Limit


def validate_prisma_schema(file_path: Path) -> Dict[str, Any]:
    """Validate Prisma schema file."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Find all models
        models = re.findall(r'model\s+(\w+)\s*{([^}]+)}', content, re.DOTALL)
        
        if models:
            passed.append(f"Found {len(models)} models")
        else:
            issues.append("No models found in schema")
            return {"passed": passed, "issues": issues}
        
        for model_name, model_body in models:
            # Check PascalCase naming
            if not model_name[0].isupper():
                issues.append(f"Model '{model_name}' should be PascalCase")
            
            # Check for id field
            if '@id' not in model_body:
                issues.append(f"Model '{model_name}' missing @id field")
            
            # Check for timestamps
            has_created = 'createdAt' in model_body or 'created_at' in model_body
            has_updated = 'updatedAt' in model_body or 'updated_at' in model_body
            
            if not has_created:
                issues.append(f"Model '{model_name}' missing createdAt (recommended)")
            if not has_updated:
                issues.append(f"Model '{model_name}' missing updatedAt (recommended)")
            
            # Check for index on foreign keys
            fk_fields = re.findall(r'(\w+Id)\s+\w+', model_body)
            for fk in fk_fields:
                if f'@@index([{fk}])' not in content and f'@@index(["{fk}"])' not in content:
                    issues.append(f"Consider @@index([{fk}]) in {model_name}")
        
        # Check for enums
        enums = re.findall(r'enum\s+(\w+)\s*{', content)
        if enums:
            passed.append(f"Found {len(enums)} enums")
            for enum_name in enums:
                if not enum_name[0].isupper():
                    issues.append(f"Enum '{enum_name}' should be PascalCase")
        
        # Check for datasource
        if 'datasource' in content:
            passed.append("Datasource configured")
        else:
            issues.append("Missing datasource configuration")
        
        # Check for generator
        if 'generator' in content:
            passed.append("Generator configured")
        
    except Exception as e:
        issues.append(f"Parse error: {str(e)[:50]}")
    
    return {"passed": passed, "issues": issues}


def validate_drizzle_schema(file_path: Path) -> Dict[str, Any]:
    """Validate Drizzle schema file."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Check for table definitions
        tables = re.findall(r'(?:export\s+const|const)\s+(\w+)\s*=\s*(?:pgTable|mysqlTable|sqliteTable)', content)
        
        if tables:
            passed.append(f"Found {len(tables)} tables")
        else:
            issues.append("No table definitions found")
        
        # Check for id columns
        if 'primaryKey' in content or '.primaryKey()' in content:
            passed.append("Primary keys defined")
        else:
            issues.append("Missing primary key definitions")
        
        # Check for timestamps
        if 'timestamp' in content.lower() or 'createdAt' in content:
            passed.append("Timestamp fields found")
        
        # Check for relations
        if 'relations' in content:
            passed.append("Relations defined")
        
    except Exception as e:
        issues.append(f"Parse error: {str(e)[:50]}")
    
    return {"passed": passed, "issues": issues}


def validate_typeorm_entity(file_path: Path) -> Dict[str, Any]:
    """Validate TypeORM entity file."""
    issues = []
    passed = []
    
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        # Check for @Entity decorator
        if '@Entity' in content:
            passed.append("@Entity decorator found")
        else:
            issues.append("Missing @Entity decorator")
        
        # Check for @PrimaryGeneratedColumn or @PrimaryColumn
        if '@PrimaryGeneratedColumn' in content or '@PrimaryColumn' in content:
            passed.append("Primary key defined")
        else:
            issues.append("Missing primary key column")
        
        # Check for @CreateDateColumn
        if '@CreateDateColumn' in content:
            passed.append("CreateDateColumn found")
        else:
            issues.append("Consider adding @CreateDateColumn")
        
    except Exception as e:
        issues.append(f"Parse error: {str(e)[:50]}")
    
    return {"passed": passed, "issues": issues}


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    print(f"\n{'='*60}")
    print(f"[AGT-KIT SCHEMA VALIDATOR] Database Schema Check")
    print(f"{'='*60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    schemas = find_schema_files(project_path)
    print(f"Found {len(schemas)} schema files")
    
    if not schemas:
        output = {
            "script": "schema_validator",
            "skill": "database-design",
            "project": str(project_path),
            "schemas_checked": 0,
            "passed": True,
            "message": "No schema files found"
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    
    all_results = []
    total_issues = 0
    
    for schema_type, file_path in schemas:
        print(f"\n📄 {file_path.name} ({schema_type})")
        
        if schema_type == 'prisma':
            result = validate_prisma_schema(file_path)
        elif schema_type == 'drizzle':
            result = validate_drizzle_schema(file_path)
        elif schema_type == 'typeorm':
            result = validate_typeorm_entity(file_path)
        else:
            result = {"passed": [], "issues": []}
        
        # Print results
        for item in result["passed"]:
            print(f"  ✅ {item}")
        for item in result["issues"][:5]:
            print(f"  ⚠️  {item}")
        
        if len(result["issues"]) > 5:
            print(f"  ... and {len(result['issues']) - 5} more issues")
        
        all_results.append({
            "file": str(file_path.name),
            "type": schema_type,
            **result
        })
        total_issues += len(result["issues"])
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    # Schema issues are warnings, not failures
    passed = total_issues < 10
    
    if passed:
        print(f"✅ Schema validation passed ({total_issues} minor issues)")
    else:
        print(f"⚠️  Schema needs review ({total_issues} issues)")
    
    output = {
        "script": "schema_validator",
        "skill": "database-design",
        "project": str(project_path),
        "schemas_checked": len(schemas),
        "total_issues": total_issues,
        "passed": passed,
        "results": all_results
    }
    
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
