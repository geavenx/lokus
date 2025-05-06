#!/usr/bin/env python3
import pytest
import yaml # For creating test fixture content
import os
from src.config_loader import load_config

FIXTURES_DIR = "/home/ubuntu/swagger_validator/tests/fixtures"

@pytest.fixture(scope="function", autouse=True)
def ensure_fixtures_dir():
    os.makedirs(FIXTURES_DIR, exist_ok=True)

@pytest.fixture
def valid_config_file(tmp_path):
    content = {
        "forbidden_keys": ["key1", "secretKey"],
        "forbidden_key_patterns": [".*_token$"],
        "forbidden_keys_at_paths": [
            {"path": "info.contact.email", "key": "email", "reason": "Test reason"}
        ],
        "allowed_exceptions": [
            {"key": "session_token", "path_prefix": "components.schemas.Session"}
        ]
    }
    file_path = os.path.join(FIXTURES_DIR, "valid_config.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_path

@pytest.fixture
def empty_config_file(tmp_path):
    file_path = os.path.join(FIXTURES_DIR, "empty_config.yaml")
    with open(file_path, "w") as f:
        f.write("") # Empty file
    return file_path

@pytest.fixture
def malformed_config_file(tmp_path):
    file_path = os.path.join(FIXTURES_DIR, "malformed_config.yaml")
    with open(file_path, "w") as f:
        f.write("forbidden_keys: [key1, key2]: # Invalid YAML, extra colon")
    return file_path

@pytest.fixture
def wrong_type_config_file(tmp_path):
    content = {"forbidden_keys": "not_a_list"} # forbidden_keys should be a list
    file_path = os.path.join(FIXTURES_DIR, "wrong_type_config.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_path

@pytest.fixture
def unknown_keys_config_file(tmp_path):
    content = {
        "forbidden_keys": ["key1"],
        "unknown_top_level_key": "some_value",
        "forbidden_key_patterns": [] # ensure other valid keys are still processed
    }
    file_path = os.path.join(FIXTURES_DIR, "unknown_keys_config.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_path

def test_load_config_valid(valid_config_file):
    config = load_config(valid_config_file)
    assert config is not None
    assert config["forbidden_keys"] == ["key1", "secretKey"]
    assert config["forbidden_key_patterns"] == [".*_token$"]
    assert len(config["forbidden_keys_at_paths"]) == 1
    assert len(config["allowed_exceptions"]) == 1

def test_load_config_non_existent_file(capsys):
    config = load_config("non_existent_config.yaml")
    assert config is None
    captured = capsys.readouterr()
    assert "Error: Configuration file not found" in captured.out

def test_load_config_empty_file(empty_config_file, capsys):
    config = load_config(empty_config_file)
    assert config is not None
    assert config["forbidden_keys"] == []
    assert config["forbidden_key_patterns"] == []
    assert config["forbidden_keys_at_paths"] == []
    assert config["allowed_exceptions"] == []
    captured = capsys.readouterr()
    assert "Warning: Configuration file" in captured.out and "is empty" in captured.out

def test_load_config_malformed_yaml(malformed_config_file, capsys):
    config = load_config(malformed_config_file)
    assert config is None
    captured = capsys.readouterr()
    assert "Error parsing configuration file" in captured.out

def test_load_config_wrong_type(wrong_type_config_file, capsys):
    config = load_config(wrong_type_config_file)
    assert config is not None
    # The loader should default to an empty list for mistyped keys
    assert config["forbidden_keys"] == [] 
    captured = capsys.readouterr()
    assert "Warning: Configuration key 'forbidden_keys'" in captured.out
    assert "is not of expected type list" in captured.out

def test_load_config_unknown_top_level_keys(unknown_keys_config_file, capsys):
    config = load_config(unknown_keys_config_file)
    assert config is not None
    assert "unknown_top_level_key" not in config # Unknown keys should be ignored
    assert config["forbidden_keys"] == ["key1"]
    assert config["forbidden_key_patterns"] == [] # Check other keys are still there
    captured = capsys.readouterr()
    assert "Warning: Unknown top-level key 'unknown_top_level_key'" in captured.out

def test_load_config_default_path_non_existent(monkeypatch, capsys):
    # Ensure no .forbidden_keys.yaml exists in the test run directory for this test
    monkeypatch.setattr("os.path.exists", lambda x: False if x == ".forbidden_keys.yaml" else os.path.exists(x))
    # The load_config function has its own default path logic, 
    # this test is more about what happens if that default file isn't found.
    config = load_config() # Call with no arguments to use default path
    assert config is None
    captured = capsys.readouterr()
    assert "Error: Configuration file not found at .forbidden_keys.yaml" in captured.out

def test_load_config_missing_section(tmp_path):
    content = {
        "forbidden_keys": ["key1"]
        # forbidden_key_patterns is missing
    }
    file_path = os.path.join(FIXTURES_DIR, "missing_section_config.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    config = load_config(file_path)
    assert config is not None
    assert config["forbidden_keys"] == ["key1"]
    assert config["forbidden_key_patterns"] == [] # Should default to empty list
    assert config["forbidden_keys_at_paths"] == []
    assert config["allowed_exceptions"] == []

