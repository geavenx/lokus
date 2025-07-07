# Banking API Security Validation Sample

This directory contains a comprehensive example demonstrating how Lokus validates financial services APIs for security vulnerabilities and LGPD compliance issues.

## Files Overview

### API Specifications
- **`bank-api-clean.yaml`** - A well-designed banking API following security best practices
- **`bank-api-problematic.yaml`** - The same API with deliberate security flaws and compliance violations
- **`banking-security-config.yaml`** - Tailored configuration for banking API validation

## Use Case: Digital Banking API

This sample represents a **real-world financial services API** that handles:
- Customer authentication and authorization
- Account management and balance inquiries
- Money transfers between accounts
- Customer profile management
- Loan application processing

### Why This Matters
Financial APIs are prime targets for security attacks and must comply with strict regulations like LGPD (Brazilian General Data Protection Law). This sample demonstrates how Lokus helps identify critical issues before they reach production.

## Validation Results

### Clean API (`bank-api-clean.yaml`)
```bash
lokus --config banking-security-config.yaml bank-api-clean.yaml
```
**Results:** 18 total issues found
- 6 forbidden items (mostly minor warnings)
- 5 security issues (rate limiting recommendations)
- 7 LGPD compliance issues (example data sanitization)

### Problematic API (`bank-api-problematic.yaml`)
```bash
lokus --config banking-security-config.yaml bank-api-problematic.yaml
```
**Results:** 75 total issues found
- 51 forbidden items (major security violations)
- 7 security issues (missing authentication)
- 17 LGPD compliance violations (sensitive data exposure)

## Security Issues Demonstrated

### Forbidden Keys & Patterns
- **Exposed secrets**: `apiKey`, `secretKey`, `admin_secret_key`
- **Internal tokens**: `internal_admin_token`, `internal_reference_token`
- **Pattern violations**: Keys ending in `_token`, `_secret`, `_key`
- **Admin access**: `admin_notes`, `master_key`, `internal_credit_score`

### LGPD Violations
- **Real CPF numbers**: `123.456.789-00`, `987.654.321-00`
- **Real RG numbers**: `12.345.678-9`
- **Actual email addresses**: `joao.silva@gmail.com`
- **Direct customer IDs**: Sequential integers instead of UUIDs
- **Missing justifications**: Properties without purpose descriptions

### Security Vulnerabilities
- **Missing authentication**: Endpoints without proper security schemes
- **No rate limiting**: APIs vulnerable to brute force attacks
- **Broken authorization**: Missing function-level access controls
- **Sensitive data exposure**: Internal admin fields in public schemas

## Key Differences

| Aspect | Clean API | Problematic API |
|--------|-----------|-----------------|
| **Authentication** | OAuth2 with proper scopes | API keys in headers |
| **Customer IDs** | UUIDs for privacy | Sequential integers |
| **Sensitive Data** | Sanitized examples | Real CPF/RG numbers |
| **Admin Access** | No internal fields exposed | Admin tokens in docs |
| **Data Justification** | Clear purpose descriptions | Missing explanations |

## Configuration Highlights

The `banking-security-config.yaml` includes:

### Global Forbidden Keys
```yaml
forbidden_keys:
  - "apiKey"
  - "secretKey"
  - "cpf"
  - "cnpj"
  - "admin"
  - "internal"
```

### Pattern-Based Detection
```yaml
forbidden_key_patterns:
  - ".*_token$"
  - "^internal_.*"
  - "^admin_.*"
  - ".*_secret$"
```

### Path-Specific Rules
```yaml
forbidden_keys_at_paths:
  - path: "components.schemas.CustomerProfile"
    key: "internal_credit_score"
    reason: "Internal credit scores should not be exposed"
```

### Smart Exceptions
```yaml
allowed_exceptions:
  - key: "OAuth2"
    path_prefix: "components.securitySchemes"
    reason: "OAuth2 is a secure authentication method"
```

## Presentation Benefits

This sample provides a **compelling before/after demonstration** showing:

1. **Real-world relevance** - Financial APIs need bulletproof security
2. **Dramatic contrast** - 18 vs 75 issues found
3. **Practical impact** - Shows exactly what Lokus catches
4. **Compliance focus** - LGPD violations clearly identified
5. **Actionable results** - Specific recommendations for fixes

## Running the Examples

```bash
# Navigate to the project root
cd /path/to/lokus

# Test the clean API
lokus --config samples/bank-api/banking-security-config.yaml samples/bank-api/bank-api-clean.yaml

# Test the problematic API
lokus --config samples/bank-api/banking-security-config.yaml samples/bank-api/bank-api-problematic.yaml

# Generate JSON reports
lokus --config samples/bank-api/banking-security-config.yaml --json samples/bank-api/bank-api-problematic.yaml

# Generate PDF reports
lokus --config samples/bank-api/banking-security-config.yaml --pdf samples/bank-api/bank-api-problematic.yaml
```

## Perfect for Demos

This sample is ideal for:
- **Security presentations** - Shows real vulnerabilities
- **LGPD compliance training** - Demonstrates data protection issues
- **Tool demonstrations** - Clear before/after validation
- **Financial sector pitches** - Relevant, high-impact use case
- **Developer education** - Learn secure API design patterns

---

*This sample demonstrates the critical importance of automated security validation in financial services, where a single vulnerability can have catastrophic consequences.*