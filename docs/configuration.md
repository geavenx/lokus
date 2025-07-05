# Lokus Configuration Guide

This guide provides comprehensive information on how to configure Lokus for API security and LGPD compliance validation.

## Table of Contents

- [Configuration File Overview](#configuration-file-overview)
- [Configuration Structure](#configuration-structure)
- [Forbidden Keys](#forbidden-keys)
- [Forbidden Key Patterns](#forbidden-key-patterns)
- [Path-Specific Rules](#path-specific-rules)
- [Allowed Exceptions](#allowed-exceptions)
- [Configuration Examples](#configuration-examples)
- [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)
- [Troubleshooting](#troubleshooting)

## Configuration File Overview

Lokus uses YAML configuration files to define validation rules. The default configuration file is `.forbidden_keys.yaml` in the current directory, but you can specify a custom file using the `--config` option.

### Default Configuration Lookup

1. Specified configuration file (`--config custom.yaml`)
2. `.forbidden_keys.yaml` in current directory
3. Built-in default configuration

### Configuration File Format

```yaml
# .forbidden_keys.yaml
forbidden_keys:
  - "key1"
  - "key2"

forbidden_key_patterns:
  - "pattern1"
  - "pattern2"

forbidden_keys_at_paths:
  - path: "specific.path"
    key: "forbidden_key"
    reason: "Explanation"

allowed_exceptions:
  - key: "exception_key"
    path_prefix: "allowed.path"
    reason: "Why this is allowed"
```

## Configuration Structure

### Main Sections

| Section | Type | Description | Required |
|---------|------|-------------|----------|
| `forbidden_keys` | List | Global forbidden key names | No |
| `forbidden_key_patterns` | List | Regex patterns for forbidden keys | No |
| `forbidden_keys_at_paths` | List | Path-specific forbidden keys | No |
| `allowed_exceptions` | List | Exceptions to the rules | No |

### Validation Priority

1. **Allowed Exceptions** (highest priority)
2. **Path-Specific Rules**
3. **Pattern Matching**
4. **Global Forbidden Keys** (lowest priority)

## Forbidden Keys

Global forbidden keys are exact string matches that are prohibited anywhere in the API specification.

### Basic Example

```yaml
forbidden_keys:
  - "apiKey"
  - "password"
  - "secretKey"
  - "token"
  - "secret"
```

### Case Sensitivity

Forbidden keys are **case-sensitive**:

```yaml
forbidden_keys:
  - "Password"    # Matches "Password" but not "password"
  - "password"    # Matches "password" but not "Password"
  - "PASSWORD"    # Matches "PASSWORD" but not "password"
```

### Use Cases

#### Security-Related Keys
```yaml
forbidden_keys:
  # Authentication
  - "apiKey"
  - "accessToken"
  - "refreshToken"
  - "bearerToken"
  - "jwt"
  
  # Credentials
  - "password"
  - "passwd"
  - "pwd"
  - "secret"
  - "secretKey"
  - "privateKey"
  
  # Configuration
  - "config"
  - "env"
  - "environment"
```

#### LGPD/Personal Data
```yaml
forbidden_keys:
  # Brazilian identifiers
  - "cpf"
  - "cnpj"
  - "rg"
  
  # Personal information
  - "email"
  - "phone"
  - "address"
  - "birthDate"
  
  # Sensitive data
  - "creditCard"
  - "bankAccount"
  - "salary"
```

#### Internal System References
```yaml
forbidden_keys:
  # System internals
  - "internalId"
  - "systemId"
  - "debugInfo"
  - "adminPassword"
  
  # Database references
  - "dbPassword"
  - "connectionString"
  - "databaseUrl"
```

## Forbidden Key Patterns

Patterns use regular expressions to match key names dynamically. This is powerful for catching variations and naming conventions.

### Basic Patterns

```yaml
forbidden_key_patterns:
  - ".*_token$"        # Any key ending with "_token"
  - ".*_key$"          # Any key ending with "_key"
  - "^secret_.*"       # Any key starting with "secret_"
  - "^api_.*_secret$"  # Keys like "api_user_secret"
```

### Pattern Matching Behavior

- Patterns use **full match** (`fullmatch()` in Python)
- Case-sensitive by default
- Support full Python regex syntax

### Common Pattern Examples

#### Token Patterns
```yaml
forbidden_key_patterns:
  # Various token formats
  - ".*_token$"              # user_token, auth_token
  - ".*Token$"               # userToken, authToken
  - "^token_.*"              # token_user, token_auth
  - ".*[Tt]oken.*"           # Contains "token" or "Token"
```

#### Key Patterns
```yaml
forbidden_key_patterns:
  # Key variations
  - ".*_key$"                # api_key, secret_key
  - ".*Key$"                 # apiKey, secretKey
  - "^key_.*"                # key_api, key_secret
  - ".*[Kk]ey.*"             # Contains "key" or "Key"
```

#### Credential Patterns
```yaml
forbidden_key_patterns:
  # Password variations
  - ".*[Pp]assword.*"        # password, userPassword, etc.
  - ".*[Pp]ass$"             # pass, userPass
  - ".*[Pp]wd.*"             # pwd, userPwd
  
  # Secret variations
  - ".*[Ss]ecret.*"          # secret, apiSecret, etc.
  - ".*[Cc]redential.*"      # credential, userCredential
  - ".*[Aa]uth.*"            # auth, authKey, authentication
```

#### Brazilian Data Patterns (LGPD)
```yaml
forbidden_key_patterns:
  # CPF variations
  - ".*[Cc]pf.*"             # cpf, userCpf, cpfNumber
  - ".*_cpf$"                # user_cpf, customer_cpf
  
  # Personal data patterns
  - ".*[Ee]mail.*"           # email, userEmail, emailAddress
  - ".*[Pp]hone.*"           # phone, phoneNumber, userPhone
  - ".*[Aa]ddress.*"         # address, homeAddress
```

#### Advanced Patterns
```yaml
forbidden_key_patterns:
  # Complex patterns
  - "^(api|user|admin)_.*_(key|token|secret)$"  # Structured naming
  - ".*[0-9]+.*[Kk]ey.*"                       # Keys with numbers
  - "^[A-Z_]+_SECRET$"                         # ALL_CAPS_SECRET
  - ".*(password|secret|key|token).*"          # Contains any sensitive term
```

### Pattern Testing

Test your patterns before deployment:

```python
import re

pattern = ".*_token$"
test_keys = ["user_token", "auth_token", "not_a_token", "token_user"]

for key in test_keys:
    if re.fullmatch(pattern, key):
        print(f"✅ {key} matches pattern")
    else:
        print(f"❌ {key} does not match pattern")
```

## Path-Specific Rules

Path-specific rules allow you to forbid certain keys only at specific locations in the API specification.

### Basic Structure

```yaml
forbidden_keys_at_paths:
  - path: "specific.path.in.spec"
    key: "forbidden_key"
    reason: "Human-readable explanation"
```

### Path Format

Paths use dot notation to specify locations in the YAML structure:

```yaml
# For this API spec structure:
info:
  contact:
    email: "admin@example.com"

# Use this path:
forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
    reason: "Contact email should not be exposed"
```

### Common Path Examples

#### Info Section
```yaml
forbidden_keys_at_paths:
  # Contact information
  - path: "info.contact"
    key: "email"
    reason: "Contact email should not be in public API spec"
  
  - path: "info.contact"
    key: "phone"
    reason: "Contact phone should not be exposed"
  
  # License information
  - path: "info.license"
    key: "url"
    reason: "License URL should not expose internal systems"
```

#### Server Configuration
```yaml
forbidden_keys_at_paths:
  # Server URLs
  - path: "servers"
    key: "url"
    reason: "Server URLs should not contain sensitive information"
  
  # Server descriptions
  - path: "servers"
    key: "description"
    reason: "Server descriptions should not expose internal details"
```

#### Security Schemes
```yaml
forbidden_keys_at_paths:
  # API key configurations
  - path: "components.securitySchemes"
    key: "apiKey"
    reason: "API key values should not be embedded in specification"
  
  # OAuth URLs
  - path: "components.securitySchemes"
    key: "tokenUrl"
    reason: "Token URLs should not expose internal endpoints"
  
  - path: "components.securitySchemes"
    key: "authorizationUrl"
    reason: "Authorization URLs should not expose internal endpoints"
```

#### Schema Examples
```yaml
forbidden_keys_at_paths:
  # Schema examples
  - path: "components.schemas"
    key: "example"
    reason: "Schema examples should not contain real sensitive data"
  
  # Component examples
  - path: "components.examples"
    key: "value"
    reason: "Examples should not contain real data"
  
  # Default values
  - path: "components.schemas"
    key: "default"
    reason: "Default values should not contain sensitive information"
```

#### Path Parameters
```yaml
forbidden_keys_at_paths:
  # Direct identifiers in paths
  - path: "paths"
    key: "id"
    reason: "Direct database IDs should not be used (use UUIDs instead)"
  
  - path: "paths"
    key: "user_id"
    reason: "Direct user IDs should not be used (use UUIDs instead)"
  
  - path: "paths"
    key: "email"
    reason: "Email should not be used as path parameter"
  
  - path: "paths"
    key: "cpf"
    reason: "CPF should not be used as path parameter"
```

#### Headers
```yaml
forbidden_keys_at_paths:
  # Internal headers
  - path: "components.headers"
    key: "X-Internal"
    reason: "Internal headers should not be documented publicly"
  
  - path: "components.headers"
    key: "X-Debug"
    reason: "Debug headers should not be documented publicly"
```

### Complex Path Matching

For nested structures, use full path specification:

```yaml
# API spec:
paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              properties:
                password: string

# Configuration:
forbidden_keys_at_paths:
  - path: "paths./users.post.requestBody.content.application/json.schema.properties"
    key: "password"
    reason: "Password should not be in request schema"
```

## Allowed Exceptions

Exceptions allow you to override forbidden rules for specific contexts where they are legitimate.

### Basic Structure

```yaml
allowed_exceptions:
  - key: "key_name"
    path_prefix: "allowed.path.prefix"
    reason: "Why this exception is needed"
```

### Exception Matching

- **key**: Exact key name to allow
- **path_prefix**: Path prefix where the key is allowed
- **reason**: Documentation for the exception

### Common Exception Examples

#### Security-Related Schemas
```yaml
allowed_exceptions:
  # Security schema definitions
  - key: "security"
    path_prefix: "components.schemas"
    reason: "Security-related schema definitions are legitimate"
  
  - key: "auth"
    path_prefix: "paths./auth"
    reason: "Authentication endpoints are legitimate"
  
  - key: "login"
    path_prefix: "paths./login"
    reason: "Login endpoints are legitimate"
```

#### Token Response Schemas
```yaml
allowed_exceptions:
  # Token responses
  - key: "token"
    path_prefix: "components.schemas.TokenResponse"
    reason: "Token response schema is legitimate"
  
  - key: "access_token"
    path_prefix: "components.schemas.TokenResponse"
    reason: "Access token in response schema is legitimate"
  
  - key: "refresh_token"
    path_prefix: "components.schemas.TokenResponse"
    reason: "Refresh token in response schema is legitimate"
```

#### LGPD/GDPR Compliance
```yaml
allowed_exceptions:
  # Consent fields
  - key: "consent"
    path_prefix: "components.schemas"
    reason: "Consent-related fields are required for LGPD compliance"
  
  - key: "data_processing_consent"
    path_prefix: "components.schemas"
    reason: "Data processing consent is required for LGPD compliance"
  
  - key: "privacy_policy_accepted"
    path_prefix: "components.schemas"
    reason: "Privacy policy acceptance is required for compliance"
```

#### Verification Status
```yaml
allowed_exceptions:
  # Verification fields
  - key: "email_verified"
    path_prefix: "components.schemas"
    reason: "Email verification status is legitimate"
  
  - key: "phone_verified"
    path_prefix: "components.schemas"
    reason: "Phone verification status is legitimate"
```

#### Business Context
```yaml
allowed_exceptions:
  # Business contact information
  - key: "email"
    path_prefix: "components.schemas.BusinessContact"
    reason: "Business contact email is legitimate"
  
  - key: "phone"
    path_prefix: "components.schemas.BusinessContact"
    reason: "Business contact phone is legitimate"
```

#### Public Configuration
```yaml
allowed_exceptions:
  # Public keys
  - key: "public_key"
    path_prefix: "components.schemas.PublicConfiguration"
    reason: "Public keys for client-side encryption are legitimate"
  
  - key: "api_version"
    path_prefix: "info"
    reason: "API version information is public"
```

### Exception Best Practices

1. **Be Specific**: Use precise path prefixes
2. **Document Reasons**: Always provide clear explanations
3. **Regular Review**: Periodically review exceptions for relevance
4. **Minimal Scope**: Make exceptions as narrow as possible

## Configuration Examples

### Basic Development Configuration

```yaml
# .forbidden_keys.yaml - Basic configuration for development
forbidden_keys:
  - "apiKey"
  - "password"
  - "secretKey"
  - "token"
  - "secret"

forbidden_key_patterns:
  - ".*_token$"
  - ".*_key$"
  - "^secret_.*"

forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
    reason: "Contact email should not be in API specification"

allowed_exceptions: []
```

### Strict Security Configuration

```yaml
# strict-security.yaml - Comprehensive security validation
forbidden_keys:
  # Authentication & Authorization
  - "apiKey"
  - "password"
  - "secretKey"
  - "token"
  - "secret"
  - "key"
  - "auth"
  - "credential"
  - "pass"
  - "pwd"
  - "access_token"
  - "refresh_token"
  - "bearer_token"
  - "jwt"
  - "session"
  - "cookie"
  
  # Infrastructure
  - "database"
  - "db_password"
  - "connection_string"
  - "private_key"
  - "client_secret"
  - "app_secret"
  
  # Personal Data
  - "email"
  - "phone"
  - "ssn"
  - "cpf"
  - "cnpj"
  - "credit_card"

forbidden_key_patterns:
  # Token patterns
  - ".*_token$"
  - ".*_key$"
  - ".*_secret$"
  - ".*_password$"
  - ".*_pass$"
  - ".*_pwd$"
  
  # Secret patterns
  - "^secret_.*"
  - "^api_.*_secret$"
  - "^auth_.*"
  - "^credential_.*"
  - ".*_credential$"
  - ".*_auth$"
  
  # Personal data patterns
  - ".*_email$"
  - ".*_phone$"
  - ".*_cpf$"
  - ".*_cnpj$"

forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
    reason: "Contact email should not be exposed"
  
  - path: "servers"
    key: "url"
    reason: "Server URLs should not contain sensitive information"
  
  - path: "components.securitySchemes"
    key: "apiKey"
    reason: "API key values should not be embedded"

allowed_exceptions:
  - key: "security"
    path_prefix: "components.schemas"
    reason: "Security-related schema definitions are allowed"
  
  - key: "token"
    path_prefix: "components.schemas.TokenResponse"
    reason: "Token response schema is allowed"
```

### LGPD-Focused Configuration

```yaml
# lgpd-focused.yaml - Brazilian data protection compliance
forbidden_keys:
  # Brazilian identifiers
  - "cpf"
  - "cnpj"
  - "rg"
  - "passport"
  - "driver_license"
  
  # Contact information
  - "email"
  - "phone"
  - "telefone"
  - "celular"
  - "address"
  - "endereco"
  
  # Sensitive personal data
  - "birth_date"
  - "data_nascimento"
  - "age"
  - "idade"
  - "gender"
  - "sexo"
  - "race"
  - "raca"
  - "religion"
  - "religiao"

forbidden_key_patterns:
  # CPF patterns
  - ".*cpf.*"
  - ".*_cpf$"
  - "^cpf_.*"
  
  # Email patterns
  - ".*email.*"
  - ".*_email$"
  
  # Personal data patterns
  - ".*personal.*"
  - ".*pessoal.*"
  - ".*private.*"
  - ".*privado.*"
  - ".*sensitive.*"
  - ".*sensivel.*"

forbidden_keys_at_paths:
  - path: "paths./users.post.requestBody"
    key: "cpf"
    reason: "CPF should not be required without explicit consent"
  
  - path: "components.examples"
    key: "cpf"
    reason: "Real CPF numbers should never appear in examples"
  
  - path: "paths"
    key: "email"
    reason: "Email should not be used as path parameter"

allowed_exceptions:
  - key: "consent"
    path_prefix: "components.schemas"
    reason: "Consent fields are required for LGPD compliance"
  
  - key: "email_verified"
    path_prefix: "components.schemas"
    reason: "Email verification status is allowed"
```

### Enterprise Configuration

```yaml
# enterprise.yaml - Complete enterprise validation
forbidden_keys:
  # Comprehensive forbidden keys list
  # (See templates/configs/enterprise.yaml for full example)

forbidden_key_patterns:
  # Comprehensive patterns
  # (See templates/configs/enterprise.yaml for full example)

forbidden_keys_at_paths:
  # Comprehensive path restrictions
  # (See templates/configs/enterprise.yaml for full example)

allowed_exceptions:
  # Carefully curated exceptions
  # (See templates/configs/enterprise.yaml for full example)
```

## Best Practices

### 1. Start Simple, Evolve Gradually

```yaml
# Phase 1: Basic security
forbidden_keys:
  - "password"
  - "secret"
  - "apiKey"

# Phase 2: Add patterns
forbidden_key_patterns:
  - ".*_token$"
  - ".*_key$"

# Phase 3: Add path-specific rules
forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
    reason: "Contact email exposure"

# Phase 4: Add necessary exceptions
allowed_exceptions:
  - key: "security"
    path_prefix: "components.schemas"
    reason: "Security schemas are legitimate"
```

### 2. Environment-Specific Configurations

```bash
# Directory structure
configs/
├── base.yaml              # Common rules
├── development.yaml       # Relaxed for development
├── staging.yaml          # Moderate validation
├── production.yaml       # Strict validation
└── compliance.yaml       # LGPD/GDPR focused
```

### 3. Configuration Inheritance

```yaml
# base.yaml
base_forbidden_keys: &base_keys
  - "password"
  - "secret"
  - "apiKey"

# production.yaml
forbidden_keys:
  <<: *base_keys
  - "debug"
  - "internal"
  - "admin"
```

### 4. Documentation

```yaml
# Always document your rules
forbidden_keys:
  - "debug"        # Remove debug information from production specs

forbidden_key_patterns:
  - ".*_internal$" # Prevent exposure of internal system details

forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
    reason: "Prevents exposure of internal contact information"
```

### 5. Regular Reviews

```bash
# Create a review checklist
# 1. Are all forbidden keys still relevant?
# 2. Do patterns catch new naming conventions?
# 3. Are exceptions still necessary?
# 4. Are path-specific rules covering new API structures?
```

## Advanced Configuration

### Dynamic Configuration

Create configurations programmatically:

```python
import yaml

def create_config(environment="development"):
    base_config = {
        "forbidden_keys": ["password", "secret", "apiKey"],
        "forbidden_key_patterns": [".*_token$", ".*_key$"],
        "forbidden_keys_at_paths": [],
        "allowed_exceptions": []
    }
    
    if environment == "production":
        base_config["forbidden_keys"].extend([
            "debug", "internal", "admin", "test"
        ])
        base_config["forbidden_key_patterns"].extend([
            ".*_debug$", ".*_internal$", ".*_test$"
        ])
    
    return base_config

# Generate configuration
config = create_config("production")
with open("production-config.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False)
```

### Configuration Validation

Validate your configuration before using:

```python
import yaml
import re

def validate_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate patterns
    for pattern in config.get('forbidden_key_patterns', []):
        try:
            re.compile(pattern)
            print(f"✅ Pattern '{pattern}' is valid")
        except re.error as e:
            print(f"❌ Pattern '{pattern}' is invalid: {e}")
    
    # Validate structure
    required_sections = ['forbidden_keys', 'forbidden_key_patterns', 
                        'forbidden_keys_at_paths', 'allowed_exceptions']
    
    for section in required_sections:
        if section not in config:
            print(f"⚠️  Missing section: {section}")
        else:
            print(f"✅ Section '{section}' present")

validate_config(".forbidden_keys.yaml")
```

### Configuration Templates

Create reusable configuration templates:

```yaml
# template.yaml
templates:
  basic_auth: &basic_auth
    - "password"
    - "secret"
    - "apiKey"
    
  oauth_patterns: &oauth_patterns
    - ".*_token$"
    - ".*_secret$"
    
  lgpd_fields: &lgpd_fields
    - "cpf"
    - "cnpj"
    - "email"
    - "phone"

# Use templates
forbidden_keys:
  <<: *basic_auth
  <<: *lgpd_fields

forbidden_key_patterns:
  <<: *oauth_patterns
```

## Troubleshooting

### Common Configuration Issues

#### 1. Invalid YAML Syntax

```yaml
# ❌ Invalid YAML
forbidden_keys:
  - "key1"
  - key2"  # Missing opening quote

# ✅ Valid YAML
forbidden_keys:
  - "key1"
  - "key2"
```

#### 2. Invalid Regex Patterns

```yaml
# ❌ Invalid regex
forbidden_key_patterns:
  - ".*_token["  # Invalid regex syntax

# ✅ Valid regex
forbidden_key_patterns:
  - ".*_token$"
```

#### 3. Incorrect Path Specifications

```yaml
# ❌ Incorrect path
forbidden_keys_at_paths:
  - path: "info/contact"  # Should use dots, not slashes
    key: "email"

# ✅ Correct path
forbidden_keys_at_paths:
  - path: "info.contact"
    key: "email"
```

#### 4. Case Sensitivity Issues

```yaml
# ❌ Will not match "Password" in spec
forbidden_keys:
  - "password"

# ✅ Add both cases if needed
forbidden_keys:
  - "password"
  - "Password"

# ✅ Or use pattern
forbidden_key_patterns:
  - "(?i)password"  # Case-insensitive pattern
```

### Testing Your Configuration

#### Test with Sample Data

```yaml
# test-spec.yaml - Create test API spec
openapi: 3.0.0
info:
  title: Test API
  contact:
    email: "test@example.com"  # Should be caught
components:
  schemas:
    User:
      properties:
        password: string       # Should be caught
        apiKey: string        # Should be caught
```

```bash
# Test your configuration
lokus --config your-config.yaml test-spec.yaml
```

#### Validate Specific Rules

```bash
# Test only forbidden keys
lokus --config basic-config.yaml test-spec.yaml

# Test with verbose output
lokus --verbose --config your-config.yaml test-spec.yaml

# Test with JSON output for analysis
lokus --json --config your-config.yaml test-spec.yaml | jq '.findings'
```

### Configuration Debugging

#### Enable Debug Mode

```bash
# Environment variable approach
LOKUS_DEBUG=1 lokus --verbose --config your-config.yaml api-spec.yaml

# Check configuration loading
lokus --verbose --config your-config.yaml api-spec.yaml 2>&1 | grep -i "config"
```

#### Minimal Configuration Testing

```yaml
# minimal-test.yaml - Start with minimal config
forbidden_keys:
  - "test"

forbidden_key_patterns: []
forbidden_keys_at_paths: []
allowed_exceptions: []
```

### Getting Help

When configuration issues persist:

1. **Validate YAML syntax**: Use online YAML validators
2. **Test regex patterns**: Use regex testing tools
3. **Start minimal**: Begin with simple configuration
4. **Check verbose output**: Use `--verbose` flag
5. **Review examples**: Check provided configuration examples
6. **Contact support**: [GitHub Issues](https://github.com/geavenx/lokus/issues)

### Support Resources

- 📚 [Usage Documentation](usage.md)
- 🔧 [Configuration Examples](../templates/configs/)
- 🐛 [Issue Tracker](https://github.com/geavenx/lokus/issues)
- 💬 [Discussions](https://github.com/geavenx/lokus/discussions)
- 📧 [Contact Maintainers](https://github.com/geavenx/lokus#maintainers)