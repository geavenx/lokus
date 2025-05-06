# Swagger/OpenAPI Specification Validator

This tool validates Swagger/OpenAPI specification files (YAML format) against a configurable list of forbidden keys, patterns, and path-specific rules. It helps ensure API specifications don't contain certain forbidden keys, sensitive information, or insecure configurations.

## Features

-   Loads a configuration file (`.forbidden_keys.yaml` by default) to get the list of forbidden items.
-   Parses Swagger/OpenAPI YAML files.
-   Performs a deep search through all parts of the specification.
-   Reports any instances of forbidden keys found, including their path.
-   Exits with status code `0` if validation passes, `1` if issues are found, and `2` for other errors (e.g., file not found, parsing issues).
-   Supports text and JSON output formats.
-   Integrates with GitHub Actions for CI/CD.

## Project Structure

```
swagger_validator/
├── .github/
│   └── workflows/
│       └── swagger_validator.yml  # GitHub Actions CI workflow
├── src/
│   ├── __init__.py
│   ├── cli.py                     # Command-line argument parser
│   ├── config_loader.py           # Loads .forbidden_keys.yaml
│   ├── deep_search.py             # Core logic for finding forbidden keys
│   ├── main.py                    # Main executable script
│   ├── reporter.py                # Handles output formatting and exit codes
│   └── yaml_parser.py             # Loads Swagger/OpenAPI YAML files
├── tests/
│   ├── __init__.py
│   ├── fixtures/                  # Test fixture files (sample configs, specs)
│   ├── test_cli.py
│   ├── test_config_loader.py
│   ├── test_deep_search.py
│   ├── test_reporter.py
│   └── test_yaml_parser.py
├── .forbidden_keys.yaml           # Default configuration for forbidden keys
├── .gitignore
├── README.md                      # This file
├── sample_clean_spec.yaml         # A sample Swagger spec that should pass
└── sample_problem_spec.yaml       # A sample Swagger spec with issues
```

## Prerequisites

-   Python 3.8+
-   PyYAML (`pip install PyYAML`)
-   pytest (for running tests, `pip install pytest`)

## Usage

To run the validator:

```bash
python -m src.main <path_to_swagger_file.yaml> [options]
```

**Options:**

-   `SWAGGER_FILE`: Path to the Swagger/OpenAPI YAML file to validate (required).
-   `--config CONFIG_FILE`: Path to the forbidden keys configuration YAML file (default: `.forbidden_keys.yaml`).
-   `--verbose`, `-v`: Enable verbose output.
-   `--format {text,json}`: Output format for the validation report (default: `text`).
-   `--version`: Show program's version number and exit.

**Example:**

```bash
# Validate a specific swagger file using the default config
python -m src.main path/to/your/api_spec.yaml

# Validate with a custom config and JSON output
python -m src.main path/to/your/api_spec.yaml --config path/to/custom_rules.yaml --format json
```

## Configuration (`.forbidden_keys.yaml`)

The configuration file defines what the validator should look for. It supports:

-   `forbidden_keys`: A list of exact key names that are forbidden globally.
-   `forbidden_key_patterns`: A list of regular expressions to match forbidden key names.
-   `forbidden_keys_at_paths`: A list of objects, each specifying a `key` that is forbidden at a specific `path` (dot-notation, e.g., `info.contact.email`). Can include a `reason`.
-   `allowed_exceptions`: A list of objects, each specifying a `key` and a `path_prefix` where this key, even if generally forbidden, is allowed. Can include a `reason`.

Refer to the provided `.forbidden_keys.yaml` for a detailed example.

## Running Tests

To run the unit and integration tests:

```bash
# Ensure PyYAML and pytest are installed
# From the root of the swagger_validator directory:
export PYTHONPATH=.
pytest tests/
```

## CI Integration

A GitHub Actions workflow is provided in `.github/workflows/swagger_validator.yml`. It automatically runs tests and validates sample files on pushes and pull requests to main/develop branches.

