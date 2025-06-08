import sys

import click

from lokus.config_loader import load_config
from lokus.deep_search import deep_search_forbidden_keys
from lokus.lgpd_validator import LGPDValidator
from lokus.pdf_reporter import pdf_reporter
from lokus.reporter import report_findings
from lokus.security_validator import SecurityValidator
from lokus.yaml_parser import load_swagger_spec


@click.command()
@click.version_option(prog_name="lokus")
@click.argument(
    "swagger_file",
    type=str,
    required=True,
)
@click.option(
    "--config",
    type=str,
    default=".forbidden_keys.yaml",
    help="Path to the forbidden keys configuration YAML file. (default: .forbidden_keys.yaml in the current directory)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--json", is_flag=True, help="Change output format to JSON")
@click.option("--pdf", is_flag=True, help="Generate a PDF file with report findings.")
def main(swagger_file: str, config: str, verbose: bool, json: bool, pdf: bool) -> None:
    if verbose:
        print("Verbose mode enabled.")
        print(f"Attempting to validate: {swagger_file}")
        print(f"Using configuration: {config}")
        print(f"Output format: {format}")

    # 1. Load configuration

    config_data = load_config(config)
    if config_data is None:
        # load_config already prints error messages
        sys.exit(1)  # Configuration error

    # 2. Load Swagger specification

    swagger_data = load_swagger_spec(swagger_file)
    if swagger_data is None:
        # load_swagger_spec already prints error messages
        sys.exit(1)  # Swagger file error

    # 3. Perform deep search for forbidden keys

    if verbose:
        print("Starting deep search for forbidden keys...")
    findings = deep_search_forbidden_keys(swagger_data, "", config_data, verbose)
    if verbose:
        print(f"Deep search completed. Found {len(findings)} item(s).")

    # 4. Perform security validation

    if verbose:
        print("Starting security validation...")
    security_validator = SecurityValidator()
    security_issues = security_validator.validate_spec(swagger_data)
    if verbose:
        print(f"Security validation completed. Found {len(security_issues)} issue(s).")

    # 5. Perform LGPD compliance validation

    if verbose:
        print("Starting LGPD compliance validation...")
    lgpd_validator = LGPDValidator()
    lgpd_issues = lgpd_validator.validate_spec(swagger_data)
    if verbose:
        print(
            f"LGPD compliance validation completed. Found {len(lgpd_issues)} issue(s)."
        )

    # 6. Report findings and get exit code from reporter
    # The reporter function will print to stdout based on the format
    report_findings(
        findings,
        swagger_file,
        config,
        json,
        verbose,
        security_issues=security_issues,
        lgpd_issues=lgpd_issues,
    )

    # 7. Generate a PDF file with reports
    if pdf:
        pdf_reporter(
            swagger_file_path=swagger_file,
            findings=findings,
            security_issues=security_issues,
            lgpd_issues=lgpd_issues,
        )


if __name__ == "__main__":
    main()
