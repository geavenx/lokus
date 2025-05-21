#!/usr/bin/env python3
import pytest
from swagger_validator.cli import parse_arguments

# Test basic argument parsing


def test_parse_arguments_basic(monkeypatch):
    """Test basic argument parsing for swagger_file."""
    monkeypatch.setattr("sys.argv", ["validator.py", "test.yaml"])
    args = parse_arguments()
    assert args.swagger_file == "test.yaml"
    assert args.config == ".forbidden_keys.yaml"  # Default value
    assert not args.verbose
    assert args.format == "text"


# Test with config file specified


def test_parse_arguments_with_config(monkeypatch):
    """Test argument parsing with a specified config file."""
    monkeypatch.setattr(
        "sys.argv", ["validator.py", "test.yaml", "--config", "custom_config.yaml"]
    )
    args = parse_arguments()
    assert args.swagger_file == "test.yaml"
    assert args.config == "custom_config.yaml"


# Test verbose flag


def test_parse_arguments_verbose(monkeypatch):
    """Test argument parsing with the verbose flag."""
    monkeypatch.setattr("sys.argv", ["validator.py", "test.yaml", "-v"])
    args = parse_arguments()
    assert args.verbose
    monkeypatch.setattr("sys.argv", ["validator.py", "test.yaml", "--verbose"])
    args_long = parse_arguments()
    assert args_long.verbose


# Test format flag


def test_parse_arguments_format_json(monkeypatch):
    """Test argument parsing with the format flag set to json."""
    monkeypatch.setattr("sys.argv", ["validator.py", "test.yaml", "--format", "json"])
    args = parse_arguments()
    assert args.format == "json"


# Test missing swagger_file (should raise SystemExit)


def test_parse_arguments_missing_swagger_file(monkeypatch):
    """Test argument parsing when swagger_file is missing."""
    monkeypatch.setattr("sys.argv", ["validator.py"])
    with pytest.raises(SystemExit):
        parse_arguments()


# Test invalid format choice (should raise SystemExit)


def test_parse_arguments_invalid_format(monkeypatch):
    """Test argument parsing with an invalid format choice."""
    monkeypatch.setattr("sys.argv", ["validator.py", "test.yaml", "--format", "xml"])
    with pytest.raises(SystemExit):
        parse_arguments()


# Test version flag (should raise SystemExit and print version)


def test_parse_arguments_version(monkeypatch, capsys):
    """Test argument parsing for the version flag."""
    monkeypatch.setattr("sys.argv", ["validator.py", "--version"])
    with pytest.raises(SystemExit) as e:
        parse_arguments()
    assert e.value.code == 0  # Successful exit for --version
    captured = capsys.readouterr()
    assert "validator.py 0.1.0" in captured.out  # Check if version is printed
