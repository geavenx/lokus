#!/usr/bin/env python3
import re


def deep_search_forbidden_keys(data, current_path, config_data, verbose=False):
    """
    Recursively searches for forbidden keys in the provided data structure.

    Args:
        data: The current segment of the Swagger/OpenAPI spec (dict or list).
        current_path: A string representing the path to the current data segment.
        config_data: The loaded forbidden keys configuration.
        verbose: Boolean flag for verbose logging.

    Returns:
        A list of findings (dictionaries).
    """
    findings = []
    if not config_data:  # Should not happen if load_config is robust
        if verbose:
            print("Debug: deep_search called with no config_data.")
        return findings

    forbidden_keys_list = config_data.get("forbidden_keys", [])
    forbidden_patterns_list = config_data.get("forbidden_key_patterns", [])
    # Ensure patterns are compiled for efficiency, handle invalid patterns
    compiled_patterns = []
    for idx, pattern_str in enumerate(forbidden_patterns_list):
        try:
            compiled_patterns.append((pattern_str, re.compile(pattern_str)))
        except re.error as e:
            print(
                f"Warning: Invalid regex pattern '{pattern_str}' at index {idx} in configuration: {e}. It will be skipped."
            )

    forbidden_keys_at_paths_list = config_data.get("forbidden_keys_at_paths", [])
    allowed_exceptions_list = config_data.get("allowed_exceptions", [])

    def check_key(key, path):
        # 1. Check for allowed exceptions first
        is_exception = False
        for exc in allowed_exceptions_list:
            exc_key = exc.get("key")
            exc_path_prefix = exc.get("path_prefix", "")
            # Ensure path_prefix is treated as a prefix, not necessarily the full path
            if exc_key == key and path.startswith(exc_path_prefix):
                is_exception = True
                if verbose:
                    print(
                        f"Debug: Key '{key}' at path '{path}' is an allowed exception due to rule: {exc}"
                    )
                break
        if is_exception:
            return

        # 2. Check against globally forbidden keys
        if key in forbidden_keys_list:
            findings.append(
                {
                    "path": path,
                    "key": key,
                    "type": "forbidden_key",
                    "message": f"Key '{key}' is globally forbidden.",
                }
            )

        # 3. Check against forbidden key patterns (regex)
        for pattern_str, compiled_pattern in compiled_patterns:
            if compiled_pattern.fullmatch(key):
                findings.append(
                    {
                        "path": path,
                        "key": key,
                        "type": "forbidden_key_pattern",
                        "message": f"Key '{key}' matches forbidden pattern '{pattern_str}'.",
                    }
                )

        # 4. Check against keys forbidden at specific paths
        for item in forbidden_keys_at_paths_list:
            path_to_check = item.get("path")
            forbidden_key_at_path = item.get("key")
            reason = item.get(
                "reason",
                f"Key '{forbidden_key_at_path}' is forbidden at path '{path_to_check}'.",
            )

            # Normalize paths for comparison (remove leading dot if current_path was empty)
            normalized_path = path.lstrip(".")
            normalized_path_to_check = path_to_check.lstrip(".")

            if (
                normalized_path == normalized_path_to_check
                and key == forbidden_key_at_path
            ):
                findings.append(
                    {
                        "path": path,
                        "key": key,
                        "type": "forbidden_key_at_path",
                        "message": reason,
                    }
                )

    def process_value(value, path):
        if isinstance(value, dict):
            for k, v in value.items():
                new_path = f"{path}.{k}" if path else k
                check_key(k, new_path)
                # Check if the value is a string and matches any patterns
                if isinstance(v, str):
                    for pattern_str, compiled_pattern in compiled_patterns:
                        if compiled_pattern.fullmatch(v):
                            findings.append(
                                {
                                    "path": new_path,
                                    "key": v,
                                    "type": "forbidden_key_pattern",
                                    "message": f"Key '{v}' matches forbidden pattern '{pattern_str}'.",
                                }
                            )
                process_value(v, new_path)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                new_path = f"{path}[{i}]"
                if isinstance(item, dict):
                    for k, v in item.items():
                        item_path = f"{new_path}.{k}"
                        check_key(k, item_path)
                        # Check if the value is a string and matches any patterns
                        if isinstance(v, str):
                            for pattern_str, compiled_pattern in compiled_patterns:
                                if compiled_pattern.fullmatch(v):
                                    findings.append(
                                        {
                                            "path": item_path,
                                            "key": v,
                                            "type": "forbidden_key_pattern",
                                            "message": f"Key '{v}' matches forbidden pattern '{pattern_str}'.",
                                        }
                                    )
                        process_value(v, item_path)
                else:
                    process_value(item, new_path)

    process_value(data, current_path)
    return findings


if __name__ == "__main__":
    # Sample configuration for testing
    sample_config = {
        "forbidden_keys": ["secret", "apiKey"],
        "forbidden_key_patterns": [".*_token$", "^internal_.*"],
        "forbidden_keys_at_paths": [
            {
                "path": "info.contact.email",
                "key": "email",
                "reason": "Contact email is sensitive.",
            },
            {"path": "components.schemas.User.properties.password", "key": "password"},
        ],
        "allowed_exceptions": [
            {"key": "session_token", "path_prefix": "components.schemas.Session"},
            {"key": "apiKey", "path_prefix": "components.securitySchemes.publicApiKey"},
        ],
    }

    # Sample Swagger data for testing
    sample_swagger_data = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
            "contact": {
                "name": "Test User",
                "email": "test@example.com",  # Should be caught by forbidden_keys_at_paths
            },
            "x-internal_debug_flag": True,  # Should be caught by pattern
        },
        "paths": {
            "/login": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "username": {"type": "string"},
                                        "password": {
                                            "type": "string"
                                        },  # Should be caught by forbidden_keys
                                    },
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "password": {
                            "type": "string"
                        },  # Should be caught by forbidden_keys_at_paths
                    },
                },
                "Session": {
                    "type": "object",
                    "properties": {
                        "session_token": {
                            "type": "string"
                        }  # Should be allowed by exception
                    },
                },
                "SensitiveData": {
                    "type": "object",
                    "properties": {
                        "user_secret": {"type": "string"},  # Caught by forbidden_keys
                        "refresh_token": {"type": "string"},  # Caught by pattern
                    },
                },
            },
            "securitySchemes": {
                "appApiKey": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-KEY",  # This key itself is not 'apiKey', so not caught by global 'apiKey'
                    # but if 'X-API-KEY' was in forbidden_keys, it would be.
                },
                "anotherApiKey": {
                    "type": "apiKey",
                    "in": "query",
                    "name": "apiKey",  # Caught by global 'apiKey'
                },
                "publicApiKey": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "apiKey",  # Should be allowed by exception
                },
            },
        },
    }

    print("--- Testing deep_search_forbidden_keys ---")
    findings = deep_search_forbidden_keys(
        sample_swagger_data, "", sample_config, verbose=True
    )

    if findings:
        print("\nForbidden items found:")
        for finding in findings:
            print(
                f"  - Path: {finding['path']}, Key: {finding['key']}, Type: {finding['type']}, Message: {finding['message']}"
            )
    else:
        print("\nNo forbidden items found.")

    print("\n--- Testing with empty data ---")
    findings_empty_data = deep_search_forbidden_keys({}, "", sample_config)
    if not findings_empty_data:
        print("Correctly found no items in empty data.")
    else:
        print(f"Error: Found items in empty data: {findings_empty_data}")

    print("\n--- Testing with empty config ---")
    empty_config = {
        "forbidden_keys": [],
        "forbidden_key_patterns": [],
        "forbidden_keys_at_paths": [],
        "allowed_exceptions": [],
    }
    findings_empty_config = deep_search_forbidden_keys(
        sample_swagger_data, "", empty_config
    )
    if not findings_empty_config:
        print("Correctly found no items with empty config.")
    else:
        print(f"Error: Found items with empty config: {findings_empty_config}")

    print("\n--- Testing with only allowed items ---")
    only_allowed_data = {
        "components": {
            "schemas": {
                "Session": {
                    "type": "object",
                    "properties": {"session_token": {"type": "string"}},
                }
            },
            "securitySchemes": {
                "publicApiKey": {"type": "apiKey", "in": "header", "name": "apiKey"}
            },
        }
    }
    findings_only_allowed = deep_search_forbidden_keys(
        only_allowed_data, "", sample_config, verbose=True
    )
    if not findings_only_allowed:
        print("Correctly found no items in data with only allowed keys.")
    else:
        print(
            f"Error: Found items in data with only allowed keys: {findings_only_allowed}"
        )
