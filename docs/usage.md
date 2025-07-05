# Lokus Usage Guide

This guide provides comprehensive information on how to use Lokus for API security and LGPD compliance validation.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Basic Usage](#basic-usage)
- [Command Line Options](#command-line-options)
- [Output Formats](#output-formats)
- [Validation Types](#validation-types)
- [Working with Multiple Files](#working-with-multiple-files)
- [Integration Scenarios](#integration-scenarios)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Installation Methods

### Method 1: Docker (Recommended)

Docker provides the most consistent experience across different environments:

```bash
# Quick validation
docker run --rm -v $(pwd):/workspace geaven/lokus /workspace/api-spec.yaml

# Interactive usage
docker run -it --rm -v $(pwd):/workspace geaven/lokus

# With custom configuration
docker run --rm -v $(pwd):/workspace geaven/lokus \
  --config /workspace/.forbidden_keys.yaml /workspace/api-spec.yaml
```

**Advantages:**
- No local Python environment required
- Consistent behavior across systems
- Isolated execution environment
- Always uses the latest stable version

### Method 2: Using uv (Modern Python Package Manager)

For development environments with uv:

```bash
# Install as a tool
uv tool install lokus

# Use directly
lokus api-spec.yaml

# Or run from project with uv
git clone https://github.com/geavenx/lokus.git
cd lokus
uv sync --locked --all-extras
uv run lokus api-spec.yaml
```

**Advantages:**
- Fast installation and execution
- Automatic dependency management
- Virtual environment isolation
- Easy version management

### Method 3: Traditional pip Installation

For traditional Python environments:

```bash
# Install from source
git clone https://github.com/geavenx/lokus.git
cd lokus
pip install -e .

# Verify installation
lokus --version
```

**Advantages:**
- Direct integration with existing Python workflows
- Easy for debugging and development
- Full control over dependencies

## Basic Usage

### Simple Validation

Validate a single OpenAPI/Swagger specification:

```bash
# Basic validation with default configuration
lokus api-spec.yaml

# Validation with verbose output
lokus --verbose api-spec.yaml

# Validation with custom configuration
lokus --config custom-rules.yaml api-spec.yaml
```

### Common Use Cases

#### 1. Development Workflow
```bash
# Check your API spec before committing
lokus --config .forbidden_keys.yaml openapi.yaml

# Generate detailed report for review
lokus --verbose --json openapi.yaml > validation-report.json
```

#### 2. CI/CD Pipeline
```bash
# Strict validation for production
lokus --config strict-security.yaml --json api-spec.yaml

# Exit code handling
if lokus api-spec.yaml; then
    echo "✅ API specification is secure"
else
    echo "❌ Security issues found"
    exit 1
fi
```

#### 3. Compliance Auditing
```bash
# Generate comprehensive compliance report
lokus --config lgpd-focused.yaml --pdf --verbose api-spec.yaml

# Multiple format output for documentation
lokus --json --pdf api-spec.yaml
```

## Command Line Options

### Core Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--config` | | Specify configuration file path | `--config rules.yaml` |
| `--verbose` | `-v` | Enable detailed output | `-v` |
| `--json` | | Output results in JSON format | `--json` |
| `--pdf` | | Generate PDF report | `--pdf` |
| `--version` | | Show version information | `--version` |
| `--help` | | Display help message | `--help` |

### Configuration Options

```bash
# Use specific configuration file
lokus --config /path/to/config.yaml api-spec.yaml

# Use configuration from different directory
lokus --config ../shared-config/.forbidden_keys.yaml api-spec.yaml

# Default configuration file lookup order:
# 1. .forbidden_keys.yaml (current directory)
# 2. Built-in default configuration
```

### Output Control

```bash
# Verbose output for debugging
lokus --verbose api-spec.yaml

# Quiet mode (only errors)
lokus api-spec.yaml 2>/dev/null

# JSON output for programmatic processing
lokus --json api-spec.yaml | jq '.findings | length'

# PDF report for documentation
lokus --pdf api-spec.yaml
```

## Output Formats

### Console Output (Default)

Human-readable text output with color coding and clear messages:

```
🔍 Running Lokus validation on api-spec.yaml
✅ Configuration loaded: .forbidden_keys.yaml
🔍 Starting deep search for forbidden keys...
❌ Found 2 issue(s):

1. Forbidden key found
   Path: info.contact
   Key: email
   Message: Contact email should not be in API specification

2. Security issue found
   Rule: OWASP-API1-2023
   Severity: HIGH
   Path: /users/{id}
   Description: Missing security requirements
```

### JSON Output

Structured output for programmatic processing:

```json
{
  "summary": {
    "total_findings": 2,
    "security_issues": 1,
    "lgpd_issues": 0,
    "general_findings": 1,
    "validation_status": "failed"
  },
  "findings": [
    {
      "type": "forbidden_key",
      "path": "info.contact",
      "key": "email",
      "message": "Contact email should not be in API specification"
    }
  ],
  "security_issues": [
    {
      "rule_id": "OWASP-API1-2023",
      "title": "Broken Object Level Authorization",
      "severity": "HIGH",
      "path": "/users/{id}",
      "description": "Missing security requirements",
      "recommendation": "Add security requirements to endpoint",
      "reference": "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/"
    }
  ],
  "lgpd_issues": [],
  "metadata": {
    "lokus_version": "1.0.1",
    "validation_date": "2024-01-15T10:30:00Z",
    "specification_file": "api-spec.yaml",
    "configuration_file": ".forbidden_keys.yaml"
  }
}
```

### PDF Report

Professional PDF reports with:
- Executive summary
- Detailed findings with severity levels
- Compliance status
- Recommendations
- Audit trail information

Generated files: `lokus_report-YYYYMMDD_HHMMSS.pdf`

## Validation Types

### 1. Forbidden Keys Validation

Detects sensitive information in API specifications:

```yaml
# Examples of detected issues:
info:
  contact:
    email: admin@company.com  # ❌ Exposed contact email
  
components:
  schemas:
    User:
      properties:
        password: string        # ❌ Password field
        apiKey: string         # ❌ API key field
```

### 2. Security Validation (OWASP API Security Top 10)

Checks for common API security issues:

```yaml
# Missing security requirements
paths:
  /users/{id}:
    get:                      # ❌ No security requirements
      summary: Get user
      
  /admin/users:
    post:                     # ❌ Missing authorization for sensitive endpoint
      summary: Create user
```

### 3. LGPD Compliance Validation

Validates Brazilian data protection requirements:

```yaml
# Sensitive data detection
components:
  schemas:
    Person:
      properties:
        cpf: string           # ❌ Brazilian tax ID
        email: string         # ❌ Personal email
        phone: string         # ❌ Phone number
        
  examples:
    UserExample:
      value:
        cpf: "123.456.789-00" # ❌ Real CPF in example
```

## Working with Multiple Files

### Validate Multiple Specifications

```bash
# Using shell globbing
lokus specs/*.yaml

# Using find command
find . -name "*.yaml" -exec lokus {} \;

# Batch validation with custom script
#!/bin/bash
for spec in api/**/*.yaml; do
    echo "Validating $spec"
    lokus --config configs/$(basename $(dirname $spec)).yaml "$spec"
done
```

### Directory Structure Example

```
project/
├── apis/
│   ├── user-service/
│   │   ├── openapi.yaml
│   │   └── .forbidden_keys.yaml
│   ├── payment-service/
│   │   ├── api-spec.yaml
│   │   └── .forbidden_keys.yaml
└── shared-config/
    ├── base-security.yaml
    ├── lgpd-compliance.yaml
    └── enterprise.yaml
```

### Automated Validation Script

```bash
#!/bin/bash
# validate-all-apis.sh

CONFIG_DIR="shared-config"
FAILED_VALIDATIONS=()

for service_dir in apis/*/; do
    service_name=$(basename "$service_dir")
    spec_file=$(find "$service_dir" -name "*.yaml" -o -name "*.yml" | head -1)
    
    if [ -f "$spec_file" ]; then
        echo "🔍 Validating $service_name..."
        
        if lokus --config "$CONFIG_DIR/enterprise.yaml" "$spec_file"; then
            echo "✅ $service_name passed validation"
        else
            echo "❌ $service_name failed validation"
            FAILED_VALIDATIONS+=("$service_name")
        fi
    fi
done

if [ ${#FAILED_VALIDATIONS[@]} -eq 0 ]; then
    echo "🎉 All services passed validation!"
    exit 0
else
    echo "🚨 Failed validations: ${FAILED_VALIDATIONS[*]}"
    exit 1
fi
```

## Integration Scenarios

### Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Check if any API specs are being committed
API_FILES=$(git diff --cached --name-only | grep -E '\.(yaml|yml)$')

if [ -n "$API_FILES" ]; then
    echo "🔍 Validating API specifications..."
    
    for file in $API_FILES; do
        if ! lokus "$file"; then
            echo "❌ API validation failed for $file"
            echo "Please fix the issues before committing"
            exit 1
        fi
    done
    
    echo "✅ All API specifications are valid"
fi
```

### Makefile Integration

```makefile
# Makefile

.PHONY: validate-api validate-strict validate-compliance

validate-api:
	@echo "🔍 Running basic API validation..."
	@lokus --config configs/basic-config.yaml openapi.yaml

validate-strict:
	@echo "🔍 Running strict security validation..."
	@lokus --config configs/strict-security.yaml openapi.yaml

validate-compliance:
	@echo "🔍 Running LGPD compliance validation..."
	@lokus --config configs/lgpd-focused.yaml --pdf openapi.yaml

validate-all: validate-api validate-strict validate-compliance
	@echo "✅ All validations completed"

ci-validate:
	@lokus --config configs/enterprise.yaml --json openapi.yaml
```

### Docker Compose Integration

```yaml
# docker-compose.yml
version: '3.8'

services:
  api-validator:
    image: geaven/lokus:latest
    volumes:
      - ./specs:/workspace/specs
      - ./configs:/workspace/configs
    command: >
      sh -c "
        for spec in /workspace/specs/*.yaml; do
          echo 'Validating $$spec...'
          lokus --config /workspace/configs/enterprise.yaml $$spec
        done
      "
```

## Best Practices

### 1. Configuration Management

```bash
# Use different configurations for different environments
lokus --config configs/development.yaml api-spec.yaml      # Development
lokus --config configs/staging.yaml api-spec.yaml         # Staging  
lokus --config configs/production.yaml api-spec.yaml      # Production
```

### 2. Continuous Integration

```bash
# Fail fast approach
set -e
lokus --config strict-security.yaml api-spec.yaml

# Collect all issues before failing
lokus --json api-spec.yaml > validation-results.json
ISSUES=$(jq '.summary.total_findings' validation-results.json)
if [ "$ISSUES" -gt 0 ]; then
    echo "Found $ISSUES security issues"
    exit 1
fi
```

### 3. Documentation Generation

```bash
# Generate documentation-ready reports
lokus --pdf --verbose api-spec.yaml
mv lokus_report-*.pdf docs/security-validation-$(date +%Y%m%d).pdf

# Create compliance artifacts
lokus --json --config lgpd-focused.yaml api-spec.yaml > compliance-report.json
```

### 4. Team Workflows

```bash
# Developer workflow
alias validate-api='lokus --config .forbidden_keys.yaml'
alias validate-strict='lokus --config configs/strict-security.yaml'
alias validate-compliance='lokus --config configs/lgpd-focused.yaml --pdf'

# Quick validation
validate-api openapi.yaml

# Full compliance check
validate-compliance openapi.yaml
```

## Troubleshooting

### Common Issues and Solutions

#### 1. File Not Found

```bash
# Error: API specification file not found
lokus nonexistent-file.yaml

# Solution: Check file path and existence
ls -la *.yaml
lokus existing-file.yaml
```

#### 2. Configuration Issues

```bash
# Error: Configuration file parsing failed
lokus --config invalid-config.yaml api-spec.yaml

# Solution: Validate configuration file
python -c "import yaml; yaml.safe_load(open('invalid-config.yaml'))"
```

#### 3. Permission Errors

```bash
# Error: Permission denied
docker run --rm geaven/lokus /workspace/api-spec.yaml

# Solution: Fix volume mounting
docker run --rm -v $(pwd):/workspace geaven/lokus /workspace/api-spec.yaml
```

#### 4. Large File Performance

```bash
# Issue: Slow validation on large files
lokus very-large-spec.yaml

# Solution: Use more specific configuration
lokus --config minimal-config.yaml very-large-spec.yaml
```

#### 5. False Positives

```bash
# Issue: Legitimate keys flagged as forbidden
lokus api-spec.yaml

# Solution: Use allowed exceptions in configuration
# See configuration.md for details
```

### Debug Mode

Enable detailed debugging information:

```bash
# Environment variable approach
LOKUS_DEBUG=1 lokus --verbose api-spec.yaml

# Verbose output with timing
time lokus --verbose api-spec.yaml

# Capture all output
lokus --verbose api-spec.yaml 2>&1 | tee validation.log
```

### Getting Help

When encountering issues:

1. **Check the verbose output**: `lokus --verbose api-spec.yaml`
2. **Validate your configuration**: Use a minimal config first
3. **Test with sample files**: Use the provided sample specifications
4. **Check file permissions**: Ensure Lokus can read your files
5. **Review the documentation**: [Configuration Guide](configuration.md)
6. **Report issues**: [GitHub Issues](https://github.com/geavenx/lokus/issues)

### Support Resources

- 📚 [Configuration Documentation](configuration.md)
- 🐛 [Issue Tracker](https://github.com/geavenx/lokus/issues)
- 💬 [Discussions](https://github.com/geavenx/lokus/discussions)
- 🔄 [CI/CD Templates](../templates/README.md)
- 📧 [Contact Maintainers](https://github.com/geavenx/lokus#maintainers)