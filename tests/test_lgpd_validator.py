#!/usr/bin/env python3
import pytest

from src.lgpd_validator import LGPDValidator


@pytest.fixture
def lgpd_validator():
    return LGPDValidator()


def test_sensitive_data_in_examples(lgpd_validator):
    spec = {
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "cpf": {
                            "type": "string",
                            "example": "123.456.789-00",  # Should be caught
                        },
                        "email": {
                            "type": "string",
                            "example": "user@example.com",  # Should be caught
                        },
                    },
                }
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 2
    assert any(
        issue.rule_id == "LGPD-001" and "cpf" in issue.description for issue in issues
    )
    assert any(
        issue.rule_id == "LGPD-001" and "email" in issue.description for issue in issues
    )


def test_sensitive_data_in_descriptions(lgpd_validator):
    spec = {
        "paths": {
            "/users": {
                "post": {
                    "description": "Create a new user with CPF 123.456.789-00",  # Should be caught
                    "requestBody": {
                        "description": "Contact us at support@example.com"  # Should be caught
                    },
                }
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 2
    assert any(
        issue.rule_id == "LGPD-002" and "cpf" in issue.description for issue in issues
    )
    assert any(
        issue.rule_id == "LGPD-002" and "email" in issue.description for issue in issues
    )


def test_sensitive_field_names(lgpd_validator):
    spec = {
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "cpf": {"type": "string"},  # Should be caught
                        "email": {"type": "string"},  # Should be caught
                        "name": {"type": "string"},  # Should be caught
                    },
                }
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 3
    assert all(issue.rule_id == "LGPD-003" for issue in issues)


def test_direct_identifiers_in_paths(lgpd_validator):
    spec = {
        "paths": {
            "/users/{cpf}": {  # Should be caught
                "get": {"summary": "Get user by CPF"}
            },
            "/companies/{cnpj}": {  # Should be caught
                "get": {"summary": "Get company by CNPJ"}
            },
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 2
    assert all(issue.rule_id == "LGPD-004" for issue in issues)


def test_data_minimization(lgpd_validator):
    spec = {
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "User ID"},
                        "name": {"type": "string", "description": "User name"},
                        "extra_field": {
                            "type": "string"
                        },  # Should be caught (no description)
                    },
                }
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 1
    assert issues[0].rule_id == "LGPD-005"
    assert "extra_field" in issues[0].description


def test_purpose_limitation(lgpd_validator):
    spec = {
        "paths": {
            "/users": {
                "post": {
                    "summary": "Create user"  # Should be caught (no description)
                },
                "put": {
                    "summary": "Update user",
                    "description": "Update user information",  # Should pass
                },
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 1
    assert issues[0].rule_id == "LGPD-006"
    assert "post" in issues[0].path


def test_clean_spec(lgpd_validator):
    spec = {
        "paths": {
            "/users": {
                "post": {
                    "summary": "Create user",
                    "description": "Create a new user in the system",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "User ID",
                                        },
                                        "name": {
                                            "type": "string",
                                            "description": "User name",
                                        },
                                    },
                                }
                            }
                        }
                    },
                }
            }
        }
    }
    issues = lgpd_validator.validate_spec(spec)
    assert len(issues) == 0
