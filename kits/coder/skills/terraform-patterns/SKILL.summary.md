---
name: terraform-patterns
summary: true
description: "Infrastructure as Code with Terraform/OpenTofu. For planning/quick ref — load SKILL.md for full HCL patterns."
---

# Terraform Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when writing HCL, modules, or CI/CD pipeline steps.

## Workflow (Always)
```
init → plan (REVIEW!) → apply → verify
```
Never apply without reviewing plan. Never manual console changes.

## Key Rules
- **State**: Remote backend (S3+DynamoDB lock) · Never commit `.tfstate` to git
- **Variables**: Always typed + description · `sensitive = true` for secrets · no hardcoded values
- **for_each > count** when items may be removed (prevents index-shift recreation)
- **Modules**: Small, focused, single-responsibility · pin version for prod (`"5.1.2"`)
- **Security**: `trivy config .` / `checkov -d .` before PR · No secrets in .tfvars · Least privilege IAM

## File Structure
`main.tf` · `variables.tf` · `outputs.tf` · `versions.tf` · `modules/` per logical group

## Anti-Patterns
- `latest` provider versions → pin minor `~> 5.0`
- Single state file for everything → per-environment states
- `count` for removable items → use `for_each`
- Skip plan review → always review

> Load full SKILL.md for: HCL templates, count/for_each examples, state backend config, CI/CD GitHub Actions workflow, testing patterns
