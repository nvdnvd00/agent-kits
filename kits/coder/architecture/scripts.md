# AGT-Kit Scripts Reference

> Full script table. Loaded on-demand from `ARCHITECTURE.index.md`.

---

## Master Scripts (Global)

| Script | Purpose | When to Use |
|---|---|---|
| `.agent/scripts/checklist.py` | Priority-ordered validations | Before PR/commit |
| `.agent/scripts/verify_all.py` | Complete pre-deployment suite | Before deploy |
| `.agent/scripts/kit_status.py` | Kit health check & validation | Debugging, health check |
| `.agent/scripts/skills_manager.py` | Enable/disable/search skills | Kit management |

**Usage:**
```bash
# Quick check
python3 .agent/scripts/checklist.py .

# With URL (perf check)
python3 .agent/scripts/checklist.py . --url http://localhost:3000

# Quick mode (Security, Lint, Tests only)
python3 .agent/scripts/checklist.py . --quick

# Full deploy check
python3 .agent/scripts/verify_all.py . --url http://localhost:3000

# Skill management
python3 .agent/scripts/skills_manager.py list
python3 .agent/scripts/skills_manager.py search auth
```

---

## Skill Scripts

| Skill | Script | Purpose |
|---|---|---|
| `clean-code` | `skills/clean-code/scripts/lint_runner.py` | Unified linting (ESLint, Ruff) |
| `testing-patterns` | `skills/testing-patterns/scripts/test_runner.py` | Test execution (Jest, Pytest) |
| `security-fundamentals` | `skills/security-fundamentals/scripts/security_scan.py` | OWASP-based security scan |
| `database-design` | `skills/database-design/scripts/schema_validator.py` | Prisma/Drizzle schema validation |
| `api-patterns` | `skills/api-patterns/scripts/api_validator.py` | OpenAPI & API code validation |
| `i18n-localization` | `skills/i18n-localization/scripts/i18n_checker.py` | Hardcoded strings & locale check |
| `seo-patterns` | `skills/seo-patterns/scripts/seo_checker.py` | SEO & GEO audit |
| `accessibility-patterns` | `skills/accessibility-patterns/scripts/a11y_checker.py` | WCAG 2.2 check |

---

## Adding New Scripts

1. Create in `skills/<skill-name>/scripts/`
2. Naming: `<action>_<target>.py` (e.g., `lint_runner.py`)
3. Standard output: JSON + summary
4. Return exit 0 (pass) or 1 (fail)
5. Update `checklist.py` if core check
