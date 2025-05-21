#!/usr/bin/env python3
import sys

from swagger_validator.cli import parse_arguments
from swagger_validator.config_loader import load_config
from swagger_validator.deep_search import deep_search_forbidden_keys
from swagger_validator.lgpd_validator import LGPDValidator
from swagger_validator.pdf_reporter import pdf_reporter
from swagger_validator.reporter import report_findings
from swagger_validator.security_validator import SecurityValidator
from swagger_validator.yaml_parser import load_swagger_spec

__version__ = "1.0.0"


def main():
    """Main function to run the Swagger/OpenAPI validator."""
    args = parse_arguments()  # cli.py now includes version, which will be picked up

    if args.verbose:
        print("Verbose mode enabled.")
        print(f"Attempting to validate: {args.swagger_file}")
        print(f"Using configuration: {args.config}")
        print(f"Output format: {args.format}")

    # 1. Load configuration

    config_data = load_config(args.config)
    if config_data is None:
        # load_config already prints error messages
        sys.exit(2)  # Configuration error

    # 2. Load Swagger specification

    swagger_data = load_swagger_spec(args.swagger_file)
    if swagger_data is None:
        # load_swagger_spec already prints error messages
        sys.exit(2)  # Swagger file error

    # 3. Perform deep search for forbidden keys

    if args.verbose:
        print("Starting deep search for forbidden keys...")
    findings = deep_search_forbidden_keys(swagger_data, "", config_data, args.verbose)
    if args.verbose:
        print(f"Deep search completed. Found {len(findings)} item(s).")

    # 4. Perform security validation

    if args.verbose:
        print("Starting security validation...")
    security_validator = SecurityValidator()
    security_issues = security_validator.validate_spec(swagger_data)
    if args.verbose:
        print(f"Security validation completed. Found {len(security_issues)} issue(s).")

    # 5. Perform LGPD compliance validation

    if args.verbose:
        print("Starting LGPD compliance validation...")
    lgpd_validator = LGPDValidator()
    lgpd_issues = lgpd_validator.validate_spec(swagger_data)
    if args.verbose:
        print(
            f"LGPD compliance validation completed. Found {len(lgpd_issues)} issue(s)."
        )

    # 6. Report findings and get exit code from reporter
    # The reporter function will print to stdout based on the format

    exit_code = report_findings(
        findings,
        args.swagger_file,
        args.config,
        args.format,
        args.verbose,
        security_issues=security_issues,
        lgpd_issues=lgpd_issues,
    )

    # 7. Generate a PDF file with reports

    if args.pdf:
        pdf_reporter(
            swagger_file_path=args.swagger_file,
            findings=findings,
            security_issues=security_issues,
            lgpd_issues=lgpd_issues,
        )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
