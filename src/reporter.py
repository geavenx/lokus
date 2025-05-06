#!/usr/bin/env python3
import sys
import json

def report_findings(findings, swagger_file_path, config_file_path, output_format="text", verbose=False):
    """
    Reports the findings of the validation and exits with the appropriate status code.

    Args:
        findings: A list of dictionaries, where each dictionary is a finding.
        swagger_file_path: Path to the validated Swagger file.
        config_file_path: Path to the configuration file used.
        output_format: "text" or "json".
        verbose: Boolean for verbose output (mainly for text format).
    """
    if output_format == "json":
        report_data = {
            "swagger_file_path": swagger_file_path,
            "config_file_path": config_file_path,
            "status": "passed" if not findings else "failed",
            "findings_count": len(findings),
            "findings": findings
        }
        print(json.dumps(report_data, indent=2))
    else: # Default to text format
        print("Swagger/OpenAPI Specification Validator")
        print("--------------------------------------")
        print(f"Specification File: {swagger_file_path}")
        print(f"Configuration File: {config_file_path}")
        print("")

        if findings:
            print(f"STATUS: VALIDATION FAILED - {len(findings)} forbidden item(s) found!")
            print("\nFindings:")
            for i, finding in enumerate(findings, 1):
                print(f"  {i}. Path: {finding.get('path')}")
                print(f"     Key: {finding.get('key')}")
                print(f"     Type: {finding.get('type')}")
                print(f"     Reason: {finding.get('message')}")
                if i < len(findings): print("") # Add a newline between findings
            print("\nPlease review the findings and update the API specification or the validator configuration.")
        else:
            print("STATUS: VALIDATION PASSED - No forbidden items found.")

    # Set exit status
    if findings:
        return 1 # Issues found
    else:
        return 0 # All clear

# Note: sys.exit() will be called in the main script based on the return value of this function
# and other potential errors (like file not found, parse errors) that occur before this stage.

if __name__ == "__main__":
    sample_findings_issues = [
        {
            "path": "info.contact.email", "key": "email", "type": "forbidden_key_at_path",
            "message": "Publicly exposing contact emails in API specs can lead to spam or phishing."
        },
        {
            "path": "components.securitySchemes.LegacyApiKey.x-api-key", "key": "x-api-key", "type": "forbidden_key",
            "message": "Key \t'x-api-key\t' is globally forbidden." # Tab character kept in string literal as it's not a syntax error
        }
    ]
    sample_findings_no_issues = []

    print("--- Testing Reporter (Text Format - Issues Found) ---")
    exit_code_text_issues = report_findings(sample_findings_issues, "specs/api.yaml", ".forbidden_keys.yaml", "text")
    print(f"Exited with: {exit_code_text_issues} (Expected 1)")
    print("\n")

    print("--- Testing Reporter (Text Format - No Issues) ---")
    exit_code_text_no_issues = report_findings(sample_findings_no_issues, "specs/api_clean.yaml", ".forbidden_keys.yaml", "text")
    print(f"Exited with: {exit_code_text_no_issues} (Expected 0)")
    print("\n")

    print("--- Testing Reporter (JSON Format - Issues Found) ---")
    exit_code_json_issues = report_findings(sample_findings_issues, "specs/api.yaml", ".forbidden_keys.yaml", "json")
    # Output is JSON, so we just check the exit code here
    print(f"Exited with: {exit_code_json_issues} (Expected 1)") 
    print("\n")

    print("--- Testing Reporter (JSON Format - No Issues) ---")
    exit_code_json_no_issues = report_findings(sample_findings_no_issues, "specs/api_clean.yaml", ".forbidden_keys.yaml", "json")
    print(f"Exited with: {exit_code_json_no_issues} (Expected 0)")
    print("\n")

    print("--- Testing Reporter (Text Format - Verbose - No specific verbose output in this module yet) ---")
    # Verbose flag is passed but not currently used to change reporter's own output beyond what deep_search might log
    exit_code_text_verbose = report_findings(sample_findings_issues, "specs/api.yaml", ".forbidden_keys.yaml", "text", verbose=True)
    print(f"Exited with: {exit_code_text_verbose} (Expected 1)")

