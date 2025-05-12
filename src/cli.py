#!/usr/bin/env python3
import argparse


def parse_arguments():
    """Parses command-line arguments for the Swagger/OpenAPI validator."""
    parser = argparse.ArgumentParser(
        description="Validates Swagger/OpenAPI specification files (YAML format) against a list of forbidden keys."
    )
    parser.add_argument(
        "swagger_file",
        metavar="SWAGGER_FILE",
        type=str,
        help="Path to the Swagger/OpenAPI YAML file to validate.",
    )
    parser.add_argument(
        "--config",
        metavar="CONFIG_FILE",
        type=str,
        default=".forbidden_keys.yaml",
        help="Path to the forbidden keys configuration YAML file. (default: .forbidden_keys.yaml in the current directory)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format for the validation report. (default: text)",
    )
    # Add a version argument
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"  # Placeholder version
    )

    return parser.parse_args()


if __name__ == "__main__":
    # This part is for testing the CLI argument parser directly
    # In the main application, this function will be imported and called.
    args = parse_arguments()
    print("Swagger File:", args.swagger_file)
    print("Config File:", args.config)
    print("Verbose:", args.verbose)
    print("Format:", args.format)
