---
name: aws-patterns
description: AWS CLI and Console patterns for cloud infrastructure management. Use when configuring AWS services, writing CLI scripts, managing IAM, S3, EC2, Lambda, or CloudFormation. Covers security best practices, automation, and service-specific patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AWS Patterns - Cloud Infrastructure Management

> **Philosophy:** Security-first, automation-ready, and production-proven patterns for AWS services.

---

## 📑 Content Map

| Section                 | When to Read                            |
| ----------------------- | --------------------------------------- |
| AWS CLI Basics          | Setting up CLI, configuration, profiles |
| IAM Security Patterns   | Users, roles, policies, access control  |
| S3 Patterns             | Bucket management, object storage, sync |
| EC2 Patterns            | Instance management, security groups    |
| Lambda Patterns         | Serverless functions, deployment        |
| CloudFormation Patterns | Infrastructure as Code                  |
| Security Checklist      | Pre-deployment security validation      |
| Troubleshooting         | Common issues and solutions             |

---

## 🔧 AWS CLI Basics

### Installation & Configuration

```bash
# Install AWS CLI v2 (macOS)
brew install awscli

# Configure default profile
aws configure
# → AWS Access Key ID
# → AWS Secret Access Key
# → Default region (e.g., ap-southeast-1)
# → Default output format (json)

# Configure named profile
aws configure --profile production

# List configurations
aws configure list
aws configure list-profiles

# Get current identity
aws sts get-caller-identity
```

### Profile Management

| Pattern         | Command                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------- |
| Use profile     | `aws s3 ls --profile production`                                                                   |
| Export profile  | `export AWS_PROFILE=production`                                                                    |
| Override region | `aws ec2 describe-instances --region us-west-2`                                                    |
| MFA session     | `aws sts get-session-token --serial-number arn:aws:iam::123456789012:mfa/user --token-code 123456` |

### Output Formats

```bash
# JSON (default, best for scripts)
aws ec2 describe-instances --output json

# Table (human-readable)
aws ec2 describe-instances --output table

# Text (simple, tab-separated)
aws ec2 describe-instances --output text

# Use jq for JSON parsing
aws ec2 describe-instances | jq '.Reservations[].Instances[].InstanceId'
```

---

## 🔐 IAM Security Patterns

### Core Principles (2024-2025)

| Principle                 | Implementation                             |
| ------------------------- | ------------------------------------------ |
| **Least Privilege**       | Grant only minimum required permissions    |
| **Temporary Credentials** | Use IAM roles, avoid long-term access keys |
| **MFA Everywhere**        | Require MFA for console access + API calls |
| **No Root User**          | Never use root for daily tasks             |
| **Regular Audits**        | Review unused roles/users every 90 days    |

### IAM User Management

```bash
# List all users
aws iam list-users

# Create user
aws iam create-user --user-name developer-john

# Create access key (use sparingly!)
aws iam create-access-key --user-name developer-john

# List access keys
aws iam list-access-keys --user-name developer-john

# Delete access key (rotate regularly)
aws iam delete-access-key \
  --user-name developer-john \
  --access-key-id AKIAIOSFODNN7EXAMPLE

# Delete user
aws iam delete-user --user-name developer-john
```

### IAM Role Patterns

```bash
# Create role with trust policy
aws iam create-role \
  --role-name LambdaExecutionRole \
  --assume-role-policy-document file://trust-policy.json

# Attach managed policy
aws iam attach-role-policy \
  --role-name LambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# List role policies
aws iam list-attached-role-policies --role-name LambdaExecutionRole

# Assume role (get temp credentials)
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name MySession
```

### Trust Policy Template

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Policy Best Practices

| ❌ Don't             | ✅ Do                  |
| -------------------- | ---------------------- |
| `"Resource": "*"`    | Specify exact ARNs     |
| `"Action": "*"`      | List specific actions  |
| Attach to users      | Attach to groups/roles |
| Hardcode credentials | Use IAM roles + STS    |
| Skip MFA for admins  | Require MFA always     |

---

## 📦 S3 Patterns

### Bucket Operations

```bash
# List all buckets
aws s3 ls

# Create bucket
aws s3 mb s3://my-unique-bucket-name --region ap-southeast-1

# List bucket contents
aws s3 ls s3://my-bucket/
aws s3 ls s3://my-bucket/ --recursive

# Remove empty bucket
aws s3 rb s3://my-bucket

# Force remove bucket with contents
aws s3 rb s3://my-bucket --force
```

### Object Operations

```bash
# Upload file
aws s3 cp ./local-file.txt s3://my-bucket/

# Upload folder
aws s3 cp ./folder s3://my-bucket/folder --recursive

# Download file
aws s3 cp s3://my-bucket/file.txt ./local-file.txt

# Download folder
aws s3 cp s3://my-bucket/folder ./local-folder --recursive

# Sync (bidirectional)
aws s3 sync ./local-folder s3://my-bucket/folder
aws s3 sync s3://my-bucket/folder ./local-folder

# Sync with delete (dangerous!)
aws s3 sync ./local-folder s3://my-bucket/folder --delete

# Remove file
aws s3 rm s3://my-bucket/file.txt

# Remove folder
aws s3 rm s3://my-bucket/folder --recursive
```

### S3 Security

```bash
# Block public access (ALWAYS)
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

---

## 🖥️ EC2 Patterns

### Instance Management

```bash
# List instances
aws ec2 describe-instances

# Filter running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,PublicIpAddress]' \
  --output table

# Launch instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name MyKeyPair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --count 1

# Start/Stop/Terminate
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Get instance status
aws ec2 describe-instance-status --instance-ids i-1234567890abcdef0
```

### Security Groups

```bash
# Create security group
aws ec2 create-security-group \
  --group-name web-access \
  --description "Allow web traffic" \
  --vpc-id vpc-0123456789abcdef0

# Add inbound rule (SSH)
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/24  # Specific IP range, NOT 0.0.0.0/0!

# Add inbound rule (HTTPS)
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

# List security groups
aws ec2 describe-security-groups --group-ids sg-0123456789abcdef0

# Revoke rule
aws ec2 revoke-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

---

## ⚡ Lambda Patterns

### Function Management

```bash
# List functions
aws lambda list-functions --region ap-southeast-1

# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime nodejs20.x \
  --role arn:aws:iam::123456789012:role/LambdaExecutionRole \
  --handler index.handler \
  --zip-file fileb://function.zip

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://function.zip

# Update configuration
aws lambda update-function-configuration \
  --function-name my-function \
  --timeout 30 \
  --memory-size 256 \
  --environment "Variables={ENV=production,DEBUG=false}"

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  --cli-binary-format raw-in-base64-out \
  response.json

# View logs
aws logs tail /aws/lambda/my-function --follow

# Delete function
aws lambda delete-function --function-name my-function
```

### Lambda Permissions

```bash
# Add API Gateway trigger
aws lambda add-permission \
  --function-name my-function \
  --statement-id apigateway-access \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:region:account-id:api-id/*"

# Add S3 trigger
aws lambda add-permission \
  --function-name my-function \
  --statement-id s3-trigger \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::my-bucket
```

---

## 🏗️ CloudFormation Patterns

### Stack Operations

```bash
# Validate template
aws cloudformation validate-template \
  --template-body file://template.yaml

# Create stack
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=production \
  --capabilities CAPABILITY_IAM

# Update stack
aws cloudformation update-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=staging

# Describe stack
aws cloudformation describe-stacks --stack-name my-stack

# List stack resources
aws cloudformation list-stack-resources --stack-name my-stack

# Get stack events
aws cloudformation describe-stack-events --stack-name my-stack

# Delete stack
aws cloudformation delete-stack --stack-name my-stack

# Wait for completion
aws cloudformation wait stack-create-complete --stack-name my-stack
```

### CloudFormation Template Example

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Simple Lambda + API Gateway

Parameters:
  Environment:
    Type: String
    AllowedValues: [development, staging, production]
    Default: development

Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${Environment}-my-function"
      Runtime: nodejs20.x
      Handler: index.handler
      Code:
        ZipFile: |
          exports.handler = async (event) => {
            return { statusCode: 200, body: 'Hello!' };
          };
      Role: !GetAtt LambdaRole.Arn

  LambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

Outputs:
  FunctionArn:
    Value: !GetAtt LambdaFunction.Arn
    Export:
      Name: !Sub "${Environment}-function-arn"
```

---

## 🛡️ Security Checklist

### Pre-Deployment Audit

```markdown
## AWS Security Checklist

### IAM

- [ ] No root user access keys exist
- [ ] MFA enabled for all console users
- [ ] Access keys rotated within 90 days
- [ ] Unused users/roles removed
- [ ] No wildcard (\*) permissions in policies

### S3

- [ ] Public access blocked on all buckets
- [ ] Encryption enabled (SSE-S3 or SSE-KMS)
- [ ] Versioning enabled for critical buckets
- [ ] Bucket policies reviewed

### EC2

- [ ] Security groups have no 0.0.0.0/0 for SSH (port 22)
- [ ] Security groups have no 0.0.0.0/0 for RDP (port 3389)
- [ ] IMDSv2 required (no v1)
- [ ] EBS volumes encrypted

### Lambda

- [ ] Functions use least privilege roles
- [ ] Environment variables encrypted with KMS
- [ ] VPC configuration if accessing internal resources

### CloudFormation

- [ ] Templates stored in version control
- [ ] Secrets not hardcoded (use SSM/Secrets Manager)
- [ ] Stack policies for critical resources
```

### Monitoring & Logging

```bash
# Enable CloudTrail (MANDATORY)
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail

# Start logging
aws cloudtrail start-logging --name my-trail

# Enable CloudWatch Log Group for Lambda
aws logs create-log-group --log-group-name /aws/lambda/my-function

# Set retention
aws logs put-retention-policy \
  --log-group-name /aws/lambda/my-function \
  --retention-in-days 30
```

---

## 🔧 Troubleshooting

| Issue                          | Solution                                                        |
| ------------------------------ | --------------------------------------------------------------- |
| `Unable to locate credentials` | Run `aws configure` or check `~/.aws/credentials`               |
| `Access Denied`                | Check IAM policy, verify resource ARN, check STS assume-role    |
| `Region not specified`         | Add `--region` flag or set `AWS_DEFAULT_REGION`                 |
| `Invalid JSON`                 | Use `--cli-binary-format raw-in-base64-out` for Lambda payloads |
| `ExpiredToken`                 | Get new STS session token if using MFA/assumed role             |
| `NoSuchBucket`                 | Check bucket name and region, S3 is globally unique             |

### Debug Mode

```bash
# Enable debug output
aws s3 ls --debug

# Check API calls
aws s3 ls --debug 2>&1 | grep "Making request"
```

---

## Anti-Patterns

| ❌ Don't                     | ✅ Do                                          |
| ---------------------------- | ---------------------------------------------- |
| Hardcode access keys in code | Use IAM roles for EC2/Lambda                   |
| Use `0.0.0.0/0` for SSH      | Restrict to specific IP ranges                 |
| Create access keys for root  | Never use root, use IAM users                  |
| Skip MFA for admin accounts  | Require MFA for all privileged access          |
| Use long-term credentials    | Prefer STS temporary credentials               |
| Store secrets in env vars    | Use AWS Secrets Manager or SSM Parameter Store |
| Manual deployments           | Use CloudFormation/Terraform/CDK               |
| Single region deployment     | Multi-region for DR-critical apps              |

---

## Related Skills

| Need                   | Skill                      |
| ---------------------- | -------------------------- |
| Infrastructure as Code | `terraform-patterns`       |
| Kubernetes on AWS      | `kubernetes-patterns`      |
| Docker/ECS             | `docker-patterns`          |
| CI/CD with AWS         | `github-actions`           |
| Security hardening     | `security-fundamentals`    |
| Monitoring             | `monitoring-observability` |

---

> **Remember:** Security is not optional. Every AWS resource should be deployed with encryption, least privilege, and audit logging enabled.
