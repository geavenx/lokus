# Lokus: Swagger/OpenAPI Specification Validator

[![Lokus Validator CI](https://github.com/geavenx/Lokus/actions/workflows/lokus.yml/badge.svg)](https://github.com/geavenx/Lokus/actions/workflows/lokus.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful tool for validating Swagger/OpenAPI specification files (YAML format) against configurable security rules and LGPD compliance requirements. This validator helps ensure your API specifications don't contain forbidden keys, sensitive information, or insecure configurations.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [LGPD Compliance Features](#lgpd-compliance-features)
- [Usage Examples](#usage-examples)
- [CI/CD Templates](#cicd-templates)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- 🔍 Deep search through all parts of the specification
- ⚙️ Configurable forbidden keys, patterns, and path-specific rules
- 📝 Multiple output formats (text, JSON, and PDF)
- 🔄 Ready-to-use CI/CD templates for GitHub Actions
- 🛡️ LGPD (Brazilian General Data Protection Law) compliance validation
- 🔒 OWASP API Security Top 10 validation
- 🚦 Clear exit codes for different scenarios:
  - `0`: Validation passes
  - `1`: Issues found
  - `2`: Other errors (file not found, parsing issues)

## How It Works

```mermaid
flowchart TD
    A[Swagger/OpenAPI Spec] --> B[Load Configuration]
    B --> C[Load Swagger Spec]
    B --> D[Deep Search]
    C --> D
    D --> E[Security Validation]
    D --> F[LGPD Compliance]
    E --> G[Report Findings]
    F --> G
    G --> H{Output Format}
    H -->|Text| I[Console Output]
    H -->|JSON| J[JSON Report]
    H -->|PDF| K[PDF Report]

    subgraph Configuration
        B --> B1[Forbidden Keys]
        B --> B2[Key Patterns]
        B --> B3[Path Rules]
    end

    subgraph Validation
        D --> D1[Search Keys]
        D --> D2[Check Patterns]
        E --> E1[Security Rules]
        F --> F1[Data Protection]
        F --> F2[Purpose Definition]

    end
```

## Installation

- **Install from [PyPI](https://pypi.org/project/lokus/) (recommended):**

    ```bash
    pip install lokus
    lokus --version
    ```

- **Using docker:**

    ```bash
    docker run -qit --rm geaven/lokus --version
    ```

- **Using [uv](https://docs.astral.sh/uv/):**

    ```bash
    git clone https://github.com/geavenx/lokus.git
    cd lokus
    uv sync --locked --all-extras
    uv run lokus --version
    ```

- **Building from source:**

    ```bash
    git clone https://github.com/geavenx/lokus.git
    cd lokus
    pip install -e . # The use of a virtual environment is recommended
    lokus --version
    ```


## Quick Start

1. Create a configuration file (`.forbidden_keys.yaml`):

    ```yaml
    forbidden_keys:
      - "apiKey"
      - "secretKey"
      - "password"

    forbidden_key_patterns:
      - ".*_token$"
      - "^internal_.*"
    ```

2. Run the validator:

    ```bash
    # Validate a single file
    lokus path/to/your/api.yaml

    # Validate multiple files
    lokus path/to/specs/*.yaml

    # Use custom config file
    lokus --config custom_config.yaml path/to/your/api.yaml

    # Generate JSON report
    lokus --json path/to/your/api.yaml

    # Generate PDF report
    lokus --pdf path/to/your/api.yaml
    ```

    - Using docker:

    ```bash
    # Validate a single file
    docker run -qit --rm geaven/lokus:latest path/to/your/api.yaml

    # Get help
    docker run -qit --rm geaven/lokus:latest --help
    ```

## Configuration

The validator uses a YAML configuration file (`.forbidden_keys.yaml` by default) to define:

- Globally forbidden keys
- Forbidden key patterns (regex)
- Path-specific forbidden keys
- Allowed exceptions

Example configuration:

```yaml
forbidden_keys:
  - "apiKey"
  - "secretKey"
  - "password"

forbidden_key_patterns:
  - ".*_token$"
  - "^internal_.*"

forbidden_keys_at_paths:
  - path: "info.contact.email"
    key: "email"
    reason: "Contact email is sensitive."

allowed_exceptions:
  - key: "session_token"
    path_prefix: "components.schemas.Session"
```

## LGPD Compliance Features

The validator includes specific checks for LGPD compliance:

1. **Sensitive Data Detection**
   - Identifies common sensitive data patterns (CPF, CNPJ, RG, email, phone numbers)
   - Flags sensitive data in examples and descriptions
   - Detects sensitive field names in schemas and parameters

2. **Data Minimization**
   - Ensures all properties have proper descriptions
   - Flags unnecessary fields without justification
   - Validates that only required data is collected

3. **Purpose Limitation**
   - Requires clear descriptions of data processing purposes
   - Validates that endpoints have proper documentation
   - Ensures transparency in data handling

4. **Direct Identifier Protection**
   - Flags direct identifiers in API paths
   - Recommends using indirect identifiers (e.g., UUIDs)
   - Prevents exposure of sensitive identifiers

## Usage Examples

### Basic Validation

```bash
# Validate a single API specification
lokus api.yaml

# Validate with custom config
lokus --config security_rules.yaml api.yaml
```

### CI/CD Integration

Check the integration in [this project workflow file.](.github/workflows/lokus.yml)

For more comprehensive CI/CD integration, see our [CI/CD Templates](#cicd-templates) section.

## CI/CD Templates

Lokus provides ready-to-use CI/CD templates for seamless integration into your development workflow. These templates make it easy to add API security and LGPD compliance validation to your GitHub Actions pipelines.

### 🚀 Quick Integration

Copy any template to your `.github/workflows/` directory and customize for your project:

```bash
# Basic validation on push/PR
curl -o .github/workflows/lokus-validation.yml \
  https://raw.githubusercontent.com/geavenx/lokus/main/templates/github-actions/basic/lokus-basic.yml

# PR validation with comments
curl -o .github/workflows/lokus-pr.yml \
  https://raw.githubusercontent.com/geavenx/lokus/main/templates/github-actions/basic/lokus-pr.yml
```

### 📋 Available Templates

| Template | Purpose | Features |
|----------|---------|----------|
| **[lokus-basic.yml](templates/github-actions/basic/lokus-basic.yml)** | Simple validation | Push/PR triggers, auto-config creation |
| **[lokus-pr.yml](templates/github-actions/basic/lokus-pr.yml)** | PR integration | Automated PR comments, change detection |
| **[lokus-release.yml](templates/github-actions/basic/lokus-release.yml)** | Release gates | Strict validation, report generation |
| **[lokus-scheduled.yml](templates/github-actions/basic/lokus-scheduled.yml)** | Compliance monitoring | Weekly checks, PDF reports, issue creation |

### ⚙️ Configuration Options

Pre-built configurations for different validation levels:

- **[Basic](templates/configs/basic-config.yaml)**: Essential security checks
- **[Strict Security](templates/configs/strict-security.yaml)**: Comprehensive validation
- **[LGPD Focused](templates/configs/lgpd-focused.yaml)**: Brazilian compliance
- **[Enterprise](templates/configs/enterprise.yaml)**: Complete enterprise validation

### 📖 Full Documentation

For detailed setup instructions, customization options, and troubleshooting:

👉 **[Complete CI/CD Templates Guide](templates/README.md)**

### 🔧 Example Integration

1. **Add a basic workflow**:
   ```yaml
   # .github/workflows/api-security.yml
   name: API Security Validation
   on: [push, pull_request]

   jobs:
     lokus-validation:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Install Lokus
           run: |
             pip install uv
             uv tool install lokus
         - name: Validate API
           run: lokus api-spec.yaml
   ```

2. **Customize for your project**:
   ```yaml
   env:
     SPEC_PATH: "path/to/your/api.yaml"
     CONFIG_PATH: ".forbidden_keys.yaml"
   ```

3. **Add configuration** (optional):
   ```bash
   curl -o .forbidden_keys.yaml \
     https://raw.githubusercontent.com/geavenx/lokus/main/templates/configs/basic-config.yaml
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAPI Specification](https://swagger.io/specification/)
- [LGPD (Brazilian General Data Protection Law)](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)
