#!/usr/bin/env python3
import yaml

def load_config(config_path=".forbidden_keys.yaml"):
    """Loads the forbidden keys configuration from a YAML file."""
    if not config_path:
        print(f"Error: Configuration file path not provided. Using default: .forbidden_keys.yaml")
        config_path = ".forbidden_keys.yaml"

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            # CRITICAL: Always use yaml.safe_load() to prevent arbitrary code execution
            # from a potentially compromised configuration file.
            config = yaml.safe_load(f)
            
            if config is None: # Handles empty config file
                print(f"Warning: Configuration file {config_path} is empty. No rules will be applied.")
                return {
                    "forbidden_keys": [],
                    "forbidden_key_patterns": [],
                    "forbidden_keys_at_paths": [],
                    "allowed_exceptions": []
                }

            if not isinstance(config, dict):
                print(f"Error: Configuration file {config_path} is not a valid YAML dictionary.")
                return None
            
            # Basic validation of top-level keys and their types
            expected_config_structure = {
                "forbidden_keys": list,
                "forbidden_key_patterns": list,
                "forbidden_keys_at_paths": list,
                "allowed_exceptions": list
            }
            
            validated_config = {}
            for key, expected_type in expected_config_structure.items():
                if key in config:
                    if not isinstance(config[key], expected_type):
                        print(f"Warning: Configuration key 	'{key}	' in {config_path} is not of expected type {expected_type.__name__}. It will be ignored.")
                        validated_config[key] = [] # Default to empty list if type is wrong
                    else:
                        validated_config[key] = config[key]
                else:
                    # If a key is missing, initialize it as an empty list
                    validated_config[key] = [] 
            
            # Check for unknown top-level keys
            for key in config.keys():
                if key not in expected_config_structure:
                    print(f"Warning: Unknown top-level key 	'{key}	' in configuration file {config_path}. It will be ignored.")
            
            return validated_config
            
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file {config_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading configuration from {config_path}: {e}")
        return None

if __name__ == "__main__":
    # Test cases for the config loader
    print("--- Testing with default (likely non-existent) config ---")
    cfg = load_config()
    if cfg:
        print("Loaded default config:", cfg)
    else:
        print("Failed to load default config or it was invalid.")

    print("\n--- Testing with a sample valid config ---")
    sample_valid_config_content = """
forbidden_keys:
  - "apiKey"
  - "password"
forbidden_key_patterns:
  - ".*_secret$"
forbidden_keys_at_paths:
  - path: "info.contact.email"
    key: "email"
allowed_exceptions:
  - key: "session_token"
    path_prefix: "components.schemas.UserSession"
"""
    with open("/home/ubuntu/swagger_validator/tests/fixtures/sample_valid_config.yaml", "w", encoding='utf-8') as f:
        f.write(sample_valid_config_content)
    cfg_valid = load_config("/home/ubuntu/swagger_validator/tests/fixtures/sample_valid_config.yaml")
    if cfg_valid:
        print("Loaded valid config:", cfg_valid)
    else:
        print("Failed to load valid config.")

    print("\n--- Testing with a malformed config (invalid YAML) ---")
    sample_malformed_config_content = "forbidden_keys: [key1, key2]: # Invalid YAML"
    with open("/home/ubuntu/swagger_validator/tests/fixtures/sample_malformed_config.yaml", "w", encoding='utf-f') as f:
        f.write(sample_malformed_config_content)
    cfg_malformed = load_config("/home/ubuntu/swagger_validator/tests/fixtures/sample_malformed_config.yaml")
    if not cfg_malformed:
        print("Correctly failed to load malformed config.")

    print("\n--- Testing with a config with wrong type ---")
    sample_wrong_type_config_content = "forbidden_keys: \"not_a_list\""
    with open("/home/ubuntu/swagger_validator/tests/fixtures/sample_wrong_type_config.yaml", "w", encoding='utf-8') as f:
        f.write(sample_wrong_type_config_content)
    cfg_wrong_type = load_config("/home/ubuntu/swagger_validator/tests/fixtures/sample_wrong_type_config.yaml")
    if cfg_wrong_type and isinstance(cfg_wrong_type.get("forbidden_keys"), list):
        print(f"Loaded config with wrong type, 'forbidden_keys' defaulted to empty list: {cfg_wrong_type}")
    else:
        print(f"Failed to handle config with wrong type as expected, or other error. Result: {cfg_wrong_type}")

    print("\n--- Testing with an empty config file ---")
    with open("/home/ubuntu/swagger_validator/tests/fixtures/empty_config.yaml", "w", encoding='utf-8') as f:
        f.write("")
    cfg_empty = load_config("/home/ubuntu/swagger_validator/tests/fixtures/empty_config.yaml")
    if cfg_empty and all(isinstance(v, list) and not v for v in cfg_empty.values()):
        print(f"Loaded empty config correctly: {cfg_empty}")
    else:
        print(f"Failed to load empty config as expected. Result: {cfg_empty}")

    print("\n--- Testing with a config with unknown keys ---")
    sample_unknown_keys_config_content = """
forbidden_keys: ["key1"]
unknown_top_level_key: "some_value"
"""
    with open("/home/ubuntu/swagger_validator/tests/fixtures/unknown_keys_config.yaml", "w", encoding='utf-8') as f:
        f.write(sample_unknown_keys_config_content)
    cfg_unknown = load_config("/home/ubuntu/swagger_validator/tests/fixtures/unknown_keys_config.yaml")
    if cfg_unknown and "unknown_top_level_key" not in cfg_unknown:
        print(f"Loaded config with unknown keys, unknown key ignored: {cfg_unknown}")
    else:
        print(f"Failed to handle unknown keys as expected. Result: {cfg_unknown}")

