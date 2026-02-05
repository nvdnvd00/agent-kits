---
name: terraform-patterns
description: Infrastructure as Code with Terraform/OpenTofu. Use when designing modules, managing state, implementing CI/CD for infrastructure, or choosing between IaC approaches. Covers testing, security, multi-environment strategies.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: HIGH
---

# Terraform Patterns - Infrastructure as Code Excellence

> **Philosophy:** Infrastructure is code. Treat it with the same rigor as application code: version control, testing, code review, and automation.

---

## 🎯 Core Principles

| Principle        | Rule                                                  |
| ---------------- | ----------------------------------------------------- |
| **Declarative**  | Describe desired state, not steps to achieve it       |
| **Idempotent**   | Same code + same state = same result, every time      |
| **Version-Able** | All infrastructure changes tracked in version control |
| **Testable**     | Validate before apply, test after                     |
| **Modular**      | Reusable components, single responsibility per module |

```
❌ WRONG: Manual console changes → Export to code
✅ CORRECT: Code → Review → Plan → Apply → Verify
```

---

## 📁 Project Structure

### Standard Layout

```
infrastructure/
├── environments/           # Environment-specific configurations
│   ├── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── dev/
├── modules/                # Reusable modules
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   └── database/
├── examples/               # Usage examples (also test fixtures)
│   ├── complete/
│   └── minimal/
└── tests/                  # Test files
    └── module_test.tftest.hcl
```

### File Organization

| File               | Purpose                                 |
| ------------------ | --------------------------------------- |
| `main.tf`          | Primary resources                       |
| `variables.tf`     | Input variables with descriptions       |
| `outputs.tf`       | Output values                           |
| `versions.tf`      | Provider/Terraform version constraints  |
| `data.tf`          | Data sources (optional)                 |
| `locals.tf`        | Local values (optional)                 |
| `terraform.tfvars` | Environment-specific values (gitignore) |

---

## 🏗️ Module Hierarchy

| Type                      | When to Use                       | Example                   |
| ------------------------- | --------------------------------- | ------------------------- |
| **Resource Module**       | Single logical group of resources | VPC + subnets, SG + rules |
| **Infrastructure Module** | Collection of resource modules    | Full network stack        |
| **Composition**           | Complete infrastructure           | Multi-region deployment   |

```
Resource → Resource Module → Infrastructure Module → Composition
```

---

## 📝 Naming Conventions

### Resources

```hcl
# Good: Descriptive, contextual
resource "aws_instance" "web_server" { }
resource "aws_s3_bucket" "application_logs" { }

# Good: "this" for singleton resources (only one of that type)
resource "aws_vpc" "this" { }

# Avoid: Generic names for non-singletons
resource "aws_instance" "main" { }  # Which one?
```

### Variables

```hcl
# Prefix with context when needed
var.vpc_cidr_block          # Not just "cidr"
var.database_instance_class  # Not just "instance_class"
```

---

## 🔢 Count vs For_Each

| Scenario                          | Use               | Why                       |
| --------------------------------- | ----------------- | ------------------------- |
| Boolean condition (create or not) | `count = ? 1 : 0` | Simple on/off toggle      |
| Simple numeric replication        | `count = N`       | Fixed number of identical |
| Items may be reordered/removed    | `for_each`        | Stable resource addresses |
| Reference by key                  | `for_each`        | Named access              |

### Boolean Condition

```hcl
resource "aws_nat_gateway" "this" {
  count = var.create_nat_gateway ? 1 : 0
  # ...
}
```

### Stable Addressing with for_each

```hcl
# ✅ GOOD - Removing "us-east-1b" only affects that subnet
resource "aws_subnet" "private" {
  for_each = toset(var.availability_zones)

  availability_zone = each.key
  # ...
}

# ❌ BAD - Removing middle AZ recreates all subsequent subnets
resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  availability_zone = var.availability_zones[count.index]
  # ...
}
```

---

## 📦 Block Ordering Standard

### Resource Block

1. `count` or `for_each` FIRST (blank line after)
2. Other arguments
3. `tags` as last real argument
4. `depends_on` after tags (if needed)
5. `lifecycle` at the very end (if needed)

```hcl
resource "aws_nat_gateway" "this" {
  count = var.create_nat_gateway ? 1 : 0

  allocation_id = aws_eip.this[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.name}-nat"
  }

  depends_on = [aws_internet_gateway.this]

  lifecycle {
    create_before_destroy = true
  }
}
```

### Variable Block

1. `description` (ALWAYS required)
2. `type`
3. `default`
4. `validation`
5. `nullable` (when setting to false)

```hcl
variable "environment" {
  description = "Environment name for resource tagging"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }

  nullable = false
}
```

---

## 🗄️ State Management

### Backend Configuration

| Backend             | Use Case                  | State Locking  |
| ------------------- | ------------------------- | -------------- |
| **S3 + DynamoDB**   | AWS projects              | DynamoDB table |
| **Azure Storage**   | Azure projects            | Blob lease     |
| **GCS**             | GCP projects              | Built-in       |
| **Terraform Cloud** | Enterprise, collaboration | Built-in       |

### Remote State Example (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### State Security Checklist

| Check                     | Implementation                     |
| ------------------------- | ---------------------------------- |
| **Encryption at rest**    | `encrypt = true` in backend        |
| **Encryption in transit** | HTTPS/TLS always                   |
| **Access control**        | IAM policies limiting state access |
| **Versioning**            | S3 bucket versioning enabled       |
| **Backup**                | Cross-region replication           |

---

## 🧪 Testing Strategy

### Testing Pyramid

```
        /\
       /  \         E2E Tests (Expensive)
      /____\        - Full environment deployment
     /      \
    /________\      Integration Tests (Moderate)
   /          \     - Module testing with real resources
  /____________\
 /              \   Static Analysis (Cheap)
/________________\  - validate, fmt, lint, security scan
```

### Decision Matrix

| Situation                 | Approach              | Tools                  |
| ------------------------- | --------------------- | ---------------------- |
| Quick syntax check        | Static analysis       | `terraform validate`   |
| Pre-commit validation     | Static + lint         | `tflint`, `trivy`      |
| Terraform 1.6+, simple    | Native test framework | `terraform test`       |
| Pre-1.6, or Go expertise  | Integration testing   | Terratest              |
| Security/compliance focus | Policy as code        | OPA, Sentinel, Checkov |
| Cost-sensitive workflow   | Mock providers (1.7+) | Native tests + mocking |

### Native Testing (1.6+)

```hcl
# tests/module_test.tftest.hcl
run "verify_vpc_created" {
  command = plan

  assert {
    condition     = aws_vpc.this.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block is incorrect"
  }
}

run "verify_apply" {
  command = apply

  assert {
    condition     = output.vpc_id != ""
    error_message = "VPC ID should not be empty"
  }
}
```

---

## 🔐 Security Best Practices

### Essential Security Checks

```bash
# Static security scanning
trivy config .
checkov -d .
tfsec .
```

### Security Rules

| Rule                      | Implementation                         |
| ------------------------- | -------------------------------------- |
| **No secrets in code**    | Use secrets manager, not variables     |
| **Pin provider versions** | `version = "~> 5.0"` not `>= 5.0`      |
| **Enable encryption**     | Encryption at rest for all data stores |
| **Least privilege IAM**   | Minimal permissions, no wildcards      |
| **Private by default**    | No public IPs unless explicitly needed |

### Sensitive Variables

```hcl
variable "database_password" {
  description = "Database master password"
  type        = string
  sensitive   = true  # Won't show in logs
}

output "db_connection_string" {
  description = "Database connection string"
  value       = local.db_connection
  sensitive   = true
}
```

---

## 🔄 CI/CD Integration

### Workflow Stages

```
Format Check → Validate → Lint → Security Scan → Plan → Review → Apply
```

### GitHub Actions Example

```yaml
name: Terraform

on:
  pull_request:
    paths: ["infrastructure/**"]
  push:
    branches: [main]
    paths: ["infrastructure/**"]

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: infrastructure/environments/prod

    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.9.0

      - name: Format Check
        run: terraform fmt -check -recursive

      - name: Init
        run: terraform init -backend=false

      - name: Validate
        run: terraform validate

      - name: Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: config
          scan-ref: .

      - name: Plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 📌 Version Management

### Version Constraint Syntax

```hcl
version = "5.0.0"      # Exact (avoid - inflexible)
version = "~> 5.0"     # Recommended: 5.0.x only
version = ">= 5.0"     # Minimum (risky - breaking changes)
```

### Strategy by Component

| Component          | Strategy            | Example                       |
| ------------------ | ------------------- | ----------------------------- |
| **Terraform**      | Pin minor version   | `required_version = "~> 1.9"` |
| **Providers**      | Pin major version   | `version = "~> 5.0"`          |
| **Modules (prod)** | Pin exact version   | `version = "5.1.2"`           |
| **Modules (dev)**  | Allow patch updates | `version = "~> 5.1"`          |

---

## 🚨 Anti-Patterns

| ❌ Don't                         | ✅ Do                              |
| -------------------------------- | ---------------------------------- |
| Manual console changes           | All changes through code           |
| Secrets in terraform.tfvars      | External secrets manager           |
| Single state file for everything | Per-environment, per-stack states  |
| `terraform apply` without plan   | Always review plan before apply    |
| Hardcoded values                 | Variables with validation          |
| `latest` provider versions       | Pinned versions with lock file     |
| Massive monolithic modules       | Small, focused, composable modules |
| Skip state locking               | Always enable locking              |

---

## 🛠️ Common Issues & Fixes

| Issue                  | Cause                     | Fix                                |
| ---------------------- | ------------------------- | ---------------------------------- |
| **State lock stuck**   | Previous run crashed      | `terraform force-unlock <ID>`      |
| **Resource recreated** | `count` index shifted     | Use `for_each` instead             |
| **Provider error**     | Version mismatch          | Check lock file, run init -upgrade |
| **Cycle detected**     | Circular dependencies     | Use `depends_on` or refactor       |
| **Plan shows changes** | Drift from manual changes | Import or reconcile state          |
| **Timeout on apply**   | Resource creation slow    | Increase timeout in lifecycle      |

---

## ✅ Self-Check Before Completing

| Check                       | Question                                       |
| --------------------------- | ---------------------------------------------- |
| ✅ **Modules?**             | Is reusable logic extracted to modules?        |
| ✅ **State remote?**        | State stored remotely with locking?            |
| ✅ **Versions pinned?**     | Terraform and provider versions constrained?   |
| ✅ **Variables validated?** | Input variables have description + validation? |
| ✅ **Secrets safe?**        | No secrets in code or state?                   |
| ✅ **Tested?**              | Plan reviewed, security scanned?               |
| ✅ **Documented?**          | README for modules, examples provided?         |

---

## 🔗 Related Skills

| Need                    | Skill                 |
| ----------------------- | --------------------- |
| Container orchestration | `kubernetes-patterns` |
| Docker builds           | `docker-patterns`     |
| CI/CD workflows         | `github-actions`      |
| Database design         | `database-design`     |
| Cloud architecture      | Cloud provider docs   |

---

> **Remember:** The best infrastructure code is boring, predictable, and well-tested. If you're debugging infrastructure in production, something went wrong in the development process.
