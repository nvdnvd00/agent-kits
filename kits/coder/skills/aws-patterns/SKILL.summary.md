---
name: aws-patterns
summary: true
description: "AWS CLI and Console patterns. For planning/quick ref — load SKILL.md for full CLI commands."
---

# AWS Patterns — Summary

> ⚡ Quick ref. Load full `SKILL.md` when writing CLI scripts or specific service configs.

## Security First (Non-Negotiable)
- **IAM**: Least privilege · No root · MFA everywhere · Temp credentials (STS) · Never `*` actions/resources
- **S3**: Block public access · Enable versioning + AES256 encryption · Lifecycle policies
- **EC2**: No `0.0.0.0/0` for SSH (port 22) · IMDSv2 required · EBS encrypted
- **Lambda**: Least privilege roles · KMS for env vars · VPC for internal resources
- **All**: CloudTrail multi-region enabled · Secrets in Secrets Manager, never env vars · IaC only (no manual)

## Services Quick Map
- **Identity**: IAM roles + STS assume-role (not long-term access keys)
- **Storage**: S3 with versioning, encryption, lifecycle
- **Compute**: EC2 (VMs) / Lambda (serverless) / ECS (containers)
- **Orchestration**: CloudFormation / Terraform for all infra
- **Observability**: CloudWatch Logs + CloudTrail + Metrics

## Troubleshooting
- `Unable to locate credentials` → run `aws configure` or check `~/.aws/credentials`
- `Access Denied` → check IAM policy, verify ARN, check STS role
- `ExpiredToken` → get new STS session (MFA/assumed role)

> Load full SKILL.md for: complete CLI commands, IAM templates, S3/EC2/Lambda/CloudFormation examples, security checklist
