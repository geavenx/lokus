#!/usr/bin/env python3
import os

import pytest
import yaml  # For creating test fixture content

from lokus.yaml_parser import load_swagger_spec

FIXTURES_DIR = "tests/fixtures"


@pytest.fixture(scope="function", autouse=True)
def ensure_fixtures_dir():
    os.makedirs(FIXTURES_DIR, exist_ok=True)


@pytest.fixture
def valid_swagger_file(tmp_path):
    content = {
        "openapi": "3.0.0",
        "info": {"title": "Test API", "version": "1.0.0"},
        "paths": {},
    }
    file_path = os.path.join(FIXTURES_DIR, "valid_swagger.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_path


@pytest.fixture
def empty_swagger_file(tmp_path):
    file_path = os.path.join(FIXTURES_DIR, "empty_swagger.yaml")
    with open(file_path, "w") as f:
        f.write("")  # Empty file
    return file_path


@pytest.fixture
def malformed_swagger_file(tmp_path):
    file_path = os.path.join(FIXTURES_DIR, "malformed_swagger.yaml")
    with open(file_path, "w") as f:
        f.write(
            "openapi: 3.0.0\ninfo: [title: Test API: # Missing closing bracket and invalid YAML"
        )
    return file_path


@pytest.fixture
def not_dict_swagger_file(tmp_path):
    content = ["item1", "item2"]  # A list, not a dict
    file_path = os.path.join(FIXTURES_DIR, "not_dict_swagger.yaml")
    with open(file_path, "w") as f:
        yaml.dump(content, f)
    return file_path


def test_load_swagger_spec_valid(valid_swagger_file):
    spec_data = load_swagger_spec(valid_swagger_file)
    assert spec_data is not None
    assert spec_data["openapi"] == "3.0.0"
    assert spec_data["info"]["title"] == "Test API"


def test_load_swagger_spec_non_existent_file(capsys):
    spec_data = load_swagger_spec("non_existent_swagger.yaml")
    assert spec_data is None
    captured = capsys.readouterr()
    assert "Error: Swagger/OpenAPI file not found" in captured.out


def test_load_swagger_spec_empty_file(empty_swagger_file, capsys):
    spec_data = load_swagger_spec(empty_swagger_file)
    assert spec_data is None
    captured = capsys.readouterr()
    assert "Error: Swagger/OpenAPI file" in captured.out and "is empty" in captured.out


def test_load_swagger_spec_malformed_yaml(malformed_swagger_file, capsys):
    spec_data = load_swagger_spec(malformed_swagger_file)
    assert spec_data is None
    captured = capsys.readouterr()
    assert "Error parsing Swagger/OpenAPI file" in captured.out


def test_load_swagger_spec_not_a_dictionary(not_dict_swagger_file, capsys):
    spec_data = load_swagger_spec(not_dict_swagger_file)
    assert spec_data is None
    captured = capsys.readouterr()
    assert (
        "Error: Swagger/OpenAPI file" in captured.out
        and "is not a valid YAML dictionary" in captured.out
    )
