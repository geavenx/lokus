# Healthcare API Security Validation Sample

This directory contains a comprehensive example demonstrating how Lokus validates healthcare APIs for medical data security vulnerabilities and LGPD compliance issues specific to the healthcare industry.

## Files Overview

### API Specifications
- **`healthcare-api-clean.yaml`** - A well-designed healthcare API following medical data security best practices
- **`healthcare-api-problematic.yaml`** - The same API with deliberate security flaws and medical data exposure violations
- **`healthcare-security-config.yaml`** - Tailored configuration for healthcare API validation

## Use Case: Digital Health Platform API

This sample represents a **real-world healthcare API** that handles:
- Patient registration and profile management
- Medical record creation and access
- Appointment scheduling and management
- Prescription creation and fulfillment
- Emergency contact management
- Insurance information handling

### Why This Matters for Healthcare
Healthcare APIs handle the most sensitive personal data including Protected Health Information (PHI). They must comply with strict regulations like LGPD, HIPAA-equivalent standards, and medical privacy laws. This sample demonstrates how Lokus helps identify critical vulnerabilities in medical systems before they compromise patient privacy.

## Validation Results

### Clean Healthcare API (`healthcare-api-clean.yaml`)
```bash
lokus --config healthcare-security-config.yaml healthcare-api-clean.yaml
```
**Results:** 24 total issues found
- 5 forbidden items (minor warnings for medical terminology)
- 9 security issues (rate limiting and authorization recommendations)
- 10 LGPD compliance issues (example data sanitization and justifications)

### Problematic Healthcare API (`healthcare-api-problematic.yaml`)
```bash
lokus --config healthcare-security-config.yaml healthcare-api-problematic.yaml
```
**Results:** 131 total issues found
- 98 forbidden items (major medical data security violations)
- 11 security issues (missing authentication and rate limiting)
- 22 LGPD compliance violations (exposed PHI and missing justifications)

## Healthcare-Specific Security Issues Demonstrated

### Medical Data Exposure
- **Real CPF numbers**: `123.456.789-00`, `987.654.321-00` (patient and emergency contact)
- **Real RG numbers**: `12.345.678-9` 
- **Actual email addresses**: `maria.santos@gmail.com`, `joao.silva@gmail.com`
- **Phone numbers**: `+5511987654321`, `+5511987654322`
- **Medical diagnoses**: `Type 2 Diabetes Mellitus, HbA1c 8.5%`
- **Treatment details**: `Metformin 500mg BID, dietary counseling`

### Healthcare API Security Violations
- **Medical tokens exposed**: `medical_record_token`, `medical_access_token`
- **Provider secrets**: `provider_secret_key`, `doctor_login` examples
- **Pharmacy access**: `pharmacy_access_key` for prescription fulfillment
- **Controlled substances**: `controlled_substance_token` for narcotics
- **Internal medical data**: `internal_medical_id`, `internal_notes`
- **Admin privileges**: `admin_notes`, `admin_privileges` in responses

### Healthcare-Specific Patterns
- **Medical prefixes**: `medical_*`, `patient_*`, `provider_*`, `doctor_*`
- **Healthcare tokens**: `*_token` patterns for medical access
- **Internal systems**: `internal_*` patterns for medical infrastructure
- **Database access**: `database_password`, `db_key_secret` exposure

### LGPD Violations in Healthcare Context
- **Missing medical justifications**: Properties without explaining medical necessity
- **Direct patient IDs**: Sequential integers instead of UUIDs for privacy
- **Exposed diagnostic data**: Medical conditions without proper anonymization
- **Emergency contact PHI**: CPF and personal data of family members
- **Insurance data exposure**: Policy details without proper protection

## Key Differences

| Aspect | Clean Healthcare API | Problematic Healthcare API |
|--------|---------------------|---------------------------|
| **Authentication** | OAuth2 with healthcare scopes | API keys in medical headers |
| **Patient IDs** | UUIDs for medical privacy | Sequential integers |
| **Medical Data** | Sanitized clinical examples | Real diagnostic information |
| **PHI Protection** | No identifiable health info | Exposed medical conditions |
| **Access Control** | Role-based medical access | Admin tokens in documentation |
| **Prescriptions** | Secure medication handling | Controlled substance tokens |

## Configuration Highlights

The `healthcare-security-config.yaml` includes:

### Healthcare-Specific Forbidden Keys
```yaml
forbidden_keys:
  - "medical_record"
  - "diagnosis"
  - "treatment"
  - "prescription"
  - "patient_id"
  - "provider_id"
  - "insurance"
  - "pharmacy"
```

### Medical Pattern Detection
```yaml
forbidden_key_patterns:
  - "^medical_.*"
  - "^patient_.*"
  - "^provider_.*"
  - "^doctor_.*"
  - "^pharmacy_.*"
  - ".*controlled.*"
  - ".*substance.*"
```

### Healthcare Path-Specific Rules
```yaml
forbidden_keys_at_paths:
  - path: "components.schemas.Patient"
    key: "internal_medical_id"
    reason: "Internal medical IDs should not be exposed"
  
  - path: "paths./patients/.*/medical-records"
    key: "medical_record_token"
    reason: "Medical record tokens should not be exposed"
```

### Medical Data Exceptions
```yaml
allowed_exceptions:
  - key: "medicationName"
    path_prefix: "components.schemas"
    reason: "Medication name is required for prescription management"
  
  - key: "emergencyContact"
    path_prefix: "components.schemas"
    reason: "Emergency contact information is required for patient safety"
```

## Healthcare Compliance Benefits

This sample demonstrates critical healthcare security validation:

1. **Medical Privacy Protection** - Prevents PHI exposure in API documentation
2. **LGPD Healthcare Compliance** - Ensures medical data handling follows Brazilian privacy laws
3. **Clinical Data Security** - Validates proper handling of diagnostic and treatment information
4. **Prescription Safety** - Identifies controlled substance token exposure
5. **Patient Identity Protection** - Enforces UUID usage over direct patient identifiers
6. **Provider Access Control** - Validates proper medical professional authentication

## Running the Healthcare Examples

```bash
# Navigate to the project root
cd /path/to/lokus

# Test the clean healthcare API
lokus --config samples/healthcare-api/healthcare-security-config.yaml samples/healthcare-api/healthcare-api-clean.yaml

# Test the problematic healthcare API
lokus --config samples/healthcare-api/healthcare-security-config.yaml samples/healthcare-api/healthcare-api-problematic.yaml

# Generate JSON reports for compliance documentation
lokus --config samples/healthcare-api/healthcare-security-config.yaml --json samples/healthcare-api/healthcare-api-problematic.yaml

# Generate PDF reports for security audits
lokus --config samples/healthcare-api/healthcare-security-config.yaml --pdf samples/healthcare-api/healthcare-api-problematic.yaml
```

## Healthcare Industry Applications

This sample is ideal for:
- **Medical software security audits** - Shows real healthcare API vulnerabilities
- **LGPD compliance in healthcare** - Demonstrates medical data protection requirements
- **Clinical system validation** - Identifies PHI exposure risks
- **Healthcare API development** - Teaches secure medical data handling
- **Regulatory compliance training** - Shows healthcare-specific privacy violations
- **Medical device API security** - Validates connected health device APIs

## Real-World Healthcare Impact

Healthcare APIs handle life-critical data where security breaches can:
- Expose patient medical conditions and treatments
- Violate medical privacy laws (LGPD, HIPAA equivalents)
- Compromise prescription and controlled substance handling
- Leak insurance and billing information
- Enable medical identity theft
- Disrupt emergency medical response systems

---

*This sample demonstrates the critical importance of automated security validation in healthcare APIs, where patient privacy violations can have serious legal, ethical, and medical consequences.*