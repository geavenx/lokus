#!/usr/bin/env python3
import pytest

from src.deep_search import deep_search_forbidden_keys


# Sample configurations and data for testing deep_search
@pytest.fixture
def sample_config_for_search():
    return {
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
            {
                "key": "internal_metrics_token",
                "path_prefix": "custom.internal_metrics",
            },  # More specific exception
        ],
    }


@pytest.fixture
def sample_swagger_data_for_search():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
            "contact": {"name": "Test User", "email": "test@example.com"},
            "x-internal_debug_flag": True,
            "description": "Contains a secret key.",
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
                                        "password": {"type": "string"},
                                    },
                                }
                            }
                        }
                    }
                }
            },
            "/data": {
                "get": {
                    "parameters": [{"name": "user_auth_token", "in": "header"}],
                    "responses": {"200": {"description": "Success"}},
                }
            },
        },
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "password": {"type": "string"},
                    },
                },
                "Session": {
                    "type": "object",
                    "properties": {"session_token": {"type": "string"}},
                },
                "LegacyData": {
                    "type": "object",
                    "properties": {"secret": {"type": "string"}},
                },
            },
            "securitySchemes": {
                "appApiKey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
                "globalApiKey": {"type": "apiKey", "in": "query", "name": "apiKey"},
                "publicApiKey": {"type": "apiKey", "in": "header", "name": "apiKey"},
            },
        },
        "custom": {
            "internal_metrics": {
                "endpoint": "/metrics",
                "internal_metrics_token": "dont_flag_me",
            }
        },
    }


def test_deep_search_no_findings(sample_config_for_search):
    data = {"info": {"title": "Clean API"}}
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) == 0


def test_deep_search_finds_global_forbidden_key(sample_config_for_search):
    data = {
        "top_level_secret": "value",
        "components": {"schemas": {"LegacyData": {"properties": {"secret": "s3cr3t"}}}},
    }
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) >= 1
    found_secret = any(
        f["key"] == "secret"
        and f["path"] == "components.schemas.LegacyData.properties.secret"
        for f in findings
    )
    assert found_secret


# def test_deep_search_finds_pattern_key(sample_config_for_search):
#     data = {"user_auth_token": "tokval", "info": {"x-internal_debug_flag": True}}
#     findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
#     # Expect 2 findings: user_auth_token and x-internal_debug_flag
#     assert len(findings) == 2
#     found_token = any(
#         f["key"] == "user_auth_token" and f["type"] == "forbidden_key_pattern"
#         for f in findings
#     )
#     found_internal_flag = any(
#         f["key"] == "x-internal_debug_flag" and f["type"] == "forbidden_key_pattern"
#         for f in findings
#     )
#     assert found_token
#     assert found_internal_flag


def test_deep_search_finds_path_specific_key(sample_config_for_search):
    data = {"info": {"contact": {"email": "dev@example.com"}}}
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) == 1
    assert findings[0]["key"] == "email"
    assert findings[0]["path"] == "info.contact.email"
    assert findings[0]["type"] == "forbidden_key_at_path"


def test_deep_search_honors_allowed_exception(sample_config_for_search):
    data = {
        "components": {
            "schemas": {"Session": {"properties": {"session_token": "allowed"}}}
        }
    }
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) == 0


def test_deep_search_honors_path_prefix_exception(sample_config_for_search):
    data = {"components": {"securitySchemes": {"publicApiKey": {"name": "apiKey"}}}}
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) == 0


# def test_deep_search_finds_mixed_issues(
#     sample_config_for_search, sample_swagger_data_for_search
# ):
#     findings = deep_search_forbidden_keys(
#         sample_swagger_data_for_search, "", sample_config_for_search, verbose=True
#     )
#
#     expected_findings_details = [
#         {"path": "info.contact.email", "key": "email", "type": "forbidden_key_at_path"},
#         {
#             "path": "info.x-internal_debug_flag",
#             "key": "x-internal_debug_flag",
#             "type": "forbidden_key_pattern",
#         },
#         {
#             "path": "paths./login.post.requestBody.content.application/json.schema.properties.password",
#             "key": "password",
#             "type": "forbidden_key",
#         },
#         {
#             "path": "paths./data.get.parameters[0].name",
#             "key": "user_auth_token",
#             "type": "forbidden_key_pattern",
#         },
#         {
#             "path": "components.schemas.User.properties.password",
#             "key": "password",
#             "type": "forbidden_key_at_path",
#         },
#         {
#             "path": "components.schemas.User.properties.password",
#             "key": "password",
#             "type": "forbidden_key",
#         },
#         {
#             "path": "components.schemas.LegacyData.properties.secret",
#             "key": "secret",
#             "type": "forbidden_key",
#         },
#         {
#             "path": "components.securitySchemes.globalApiKey.name",
#             "key": "apiKey",
#             "type": "forbidden_key",
#         },
#     ]
#
#     assert len(findings) == len(expected_findings_details)
#
#     for expected in expected_findings_details:
#         match = False
#         for found in findings:
#             if (
#                 found["path"] == expected["path"]
#                 and found["key"] == expected["key"]
#                 and found["type"] == expected["type"]
#             ):
#                 match = True
#                 break
#         assert match, f"Expected finding not found: {expected}"


def test_deep_search_with_invalid_regex_in_config(capsys):
    config_with_bad_pattern = {
        "forbidden_key_patterns": ["valid_pattern.*", "invalid_regex_["],
        "forbidden_keys": [],
        "forbidden_keys_at_paths": [],
        "allowed_exceptions": [],
    }
    data = {"some_key": "value", "invalid_regex_key": "value"}
    findings = deep_search_forbidden_keys(data, "", config_with_bad_pattern)
    captured = capsys.readouterr()
    assert "Warning: Invalid regex pattern" in captured.out
    assert "invalid_regex_[" in captured.out
    # Check if valid patterns still work (if any were present and matched)
    # In this case, no valid pattern matches, so findings should be empty
    assert len(findings) == 0


def test_deep_search_list_traversal(sample_config_for_search):
    data = {"items": [{"id": 1}, {"secret": "in_list"}, {"name": "item3"}]}
    findings = deep_search_forbidden_keys(data, "", sample_config_for_search)
    assert len(findings) == 1
    assert findings[0]["key"] == "secret"
    assert findings[0]["path"] == "items[1].secret"


def test_deep_search_empty_config():
    config = {
        "forbidden_keys": [],
        "forbidden_key_patterns": [],
        "forbidden_keys_at_paths": [],
        "allowed_exceptions": [],
    }
    data = {"secret": "value", "user_token": "value"}
    findings = deep_search_forbidden_keys(data, "", config)
    assert len(findings) == 0


def test_deep_search_no_data():
    config = {
        "forbidden_keys": ["secret"],
        "forbidden_key_patterns": [],
        "forbidden_keys_at_paths": [],
        "allowed_exceptions": [],
    }
    findings = deep_search_forbidden_keys({}, "", config)
    assert len(findings) == 0
    findings_list = deep_search_forbidden_keys([], "", config)
    assert len(findings_list) == 0
