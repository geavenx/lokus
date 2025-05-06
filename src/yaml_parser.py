#!/usr/bin/env python3
import yaml

def load_swagger_spec(swagger_file_path):
    """Loads the Swagger/OpenAPI specification from a YAML file."""
    try:
        with open(swagger_file_path, 'r', encoding='utf-8') as f:
            # CRITICAL: Always use yaml.safe_load() for untrusted input.
            # Swagger/OpenAPI files, especially from external sources or user-provided,
            # must be treated as untrusted.
            spec_data = yaml.safe_load(f)
            
            if spec_data is None: # Handles empty swagger file
                print(f"Error: Swagger/OpenAPI file {swagger_file_path} is empty.")
                return None

            if not isinstance(spec_data, dict):
                print(f"Error: Swagger/OpenAPI file {swagger_file_path} is not a valid YAML dictionary.")
                return None
            return spec_data
    except FileNotFoundError:
        print(f"Error: Swagger/OpenAPI file not found at {swagger_file_path}")
        return None
    except yaml.YAMLError as e:
        # This will catch syntax errors in the YAML file.
        print(f"Error parsing Swagger/OpenAPI file {swagger_file_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading Swagger/OpenAPI file {swagger_file_path}: {e}")
        return None

if __name__ == "__main__":
    # Test cases for the swagger spec loader
    print("--- Testing with a sample valid Swagger spec ---")
    sample_valid_spec_content = """
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List all users
      responses:
        '200':
          description: A list of users.
"""
    with open("/home/ubuntu/swagger_validator/tests/fixtures/sample_valid_spec.yaml", "w", encoding='utf-8') as f:
        f.write(sample_valid_spec_content)
    spec_valid = load_swagger_spec("/home/ubuntu/swagger_validator/tests/fixtures/sample_valid_spec.yaml")
    if spec_valid:
        print("Loaded valid spec:", spec_valid)
    else:
        print("Failed to load valid spec.")

    print("\n--- Testing with a non-existent Swagger spec ---")
    spec_non_existent = load_swagger_spec("/home/ubuntu/swagger_validator/tests/fixtures/non_existent_spec.yaml")
    if not spec_non_existent:
        print("Correctly failed to load non-existent spec.")

    print("\n--- Testing with a malformed Swagger spec (invalid YAML) ---")
    sample_malformed_spec_content = "openapi: 3.0.0\ninfo: [title: Sample API] # Invalid YAML for info value"
    with open("/home/ubuntu/swagger_validator/tests/fixtures/sample_malformed_spec.yaml", "w", encoding='utf-8') as f:
        f.write(sample_malformed_spec_content)
    spec_malformed = load_swagger_spec("/home/ubuntu/swagger_validator/tests/fixtures/sample_malformed_spec.yaml")
    if not spec_malformed:
        print("Correctly failed to load malformed spec.")

    print("\n--- Testing with an empty Swagger spec file ---")
    with open("/home/ubuntu/swagger_validator/tests/fixtures/empty_spec.yaml", "w", encoding='utf-8') as f:
        f.write("")
    spec_empty = load_swagger_spec("/home/ubuntu/swagger_validator/tests/fixtures/empty_spec.yaml")
    if not spec_empty:
        print("Correctly failed to load empty spec.")

    print("\n--- Testing with a Swagger spec that is not a dictionary ---")
    sample_not_dict_spec_content = "- item1\n- item2" # A list, not a dict
    with open("/home/ubuntu/swagger_validator/tests/fixtures/not_dict_spec.yaml", "w", encoding='utf-8') as f:
        f.write(sample_not_dict_spec_content)
    spec_not_dict = load_swagger_spec("/home/ubuntu/swagger_validator/tests/fixtures/not_dict_spec.yaml")
    if not spec_not_dict:
        print("Correctly failed to load spec that is not a dictionary.")


