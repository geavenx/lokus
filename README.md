# Swagger/OpenAPI Specification Validator

[![Swagger/OpenAPI Validator CI](https://github.com/geavenx/swagger-validator-v2/actions/workflows/swagger_validator.yml/badge.svg)](https://github.com/geavenx/swagger-validator-v2/actions/workflows/swagger_validator.yml)

This tool validates Swagger/OpenAPI specification files (YAML format) against a configurable list of forbidden keys, patterns, and path-specific rules. It helps ensure API specifications don't contain certain forbidden keys, sensitive information, or insecure configurations.

## Features

- Loads a configuration file (`.forbidden_keys.yaml` by default) to get the list of forbidden items.
- Parses Swagger/OpenAPI YAML files.
- Performs a deep search through all parts of the specification.
- Reports any instances of forbidden keys found, including their path.
- Exits with status code `0` if validation passes, `1` if issues are found, and `2` for other errors (e.g., file not found, parsing issues).
- Supports text and JSON output formats.
- Integrates with GitHub Actions for CI/CD.
- Includes LGPD (Brazilian General Data Protection Law) compliance validation.

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

## Project Structure

```txt
swagger_validator/
├── .github/
│   └── workflows/
│       └── swagger_validator.yml  # GitHub Actions CI workflow
├── src/
│   ├── __init__.py
│   ├── cli.py                     # Command-line argument parser
│   ├── config_loader.py           # Loads .forbidden_keys.yaml
│   ├── deep_search.py             # Core logic for finding forbidden keys
│   ├── lgpd_validator.py          # LGPD compliance validation
│   ├── main.py                    # Main executable script
│   ├── reporter.py                # Handles output formatting and exit codes
│   └── yaml_parser.py             # Loads Swagger/OpenAPI YAML files
├── tests/
│   ├── __init__.py
│   ├── fixtures/                  # Test fixture files (sample configs, specs)
│   ├── test_cli.py
│   ├── test_config_loader.py
│   ├── test_deep_search.py
│   ├── test_lgpd_validator.py     # LGPD validator tests
│   ├── test_reporter.py
│   └── test_yaml_parser.py
├── samples/
│   ├── lgpd_compliant_spec.yaml   # Example of LGPD-compliant spec
│   └── lgpd_non_compliant_spec.yaml # Example of non-compliant spec
├── .forbidden_keys.yaml           # Default configuration for forbidden keys
├── .gitignore
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/swagger-validator-v2.git
   cd swagger-validator-v2
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Basic usage:

```bash
python src/main.py path/to/your/swagger.yaml
```

With custom configuration:

```bash
python src/main.py path/to/your/swagger.yaml --config path/to/config.yaml
```

With verbose output:

```bash
python src/main.py path/to/your/swagger.yaml --verbose
```

With JSON output:

```bash
python src/main.py path/to/your/swagger.yaml --format json
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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAPI Specification](https://swagger.io/specification/)
- [LGPD (Brazilian General Data Protection Law)](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)
