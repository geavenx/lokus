import os

import pytest
from click.testing import CliRunner

from lokus.cli import main


SAMPLES_DIR = "tests/samples"


@pytest.fixture
def runner():
    """Create a Click test runner."""
    return CliRunner()


@pytest.fixture
def valid_swagger_file(tmp_path):
    """Returns a swagger specification file that is valid for swagger-validator."""
    file_path = os.path.join(SAMPLES_DIR, "sample_clean_spec.yaml")
    return file_path


@pytest.fixture
def invalid_swagger_file(tmp_path):
    """Returns a swagger specification file that is NOT valid for swagger-validator."""
    file_path = os.path.join(SAMPLES_DIR, "sample_problem_spec.yaml")
    return file_path


@pytest.fixture
def config_file(tmp_path):
    """Returns a swagger-validator valid configuration file"""
    file_path = os.path.join(SAMPLES_DIR, "config.yaml")
    return file_path


def test_basic_command(runner: CliRunner, valid_swagger_file):
    """Thest basic command with required swagger_file argument."""
    print(valid_swagger_file)
    result = runner.invoke(main, [valid_swagger_file])

    assert result.exit_code == 0
    assert "Verbose mode enabled." not in result.output


def test_with_config_option(runner: CliRunner, valid_swagger_file, config_file):
    """Test command with custom config file."""
    result = runner.invoke(main, [valid_swagger_file, "--config", config_file])

    assert result.exit_code == 0
    assert "Verbose mode enabled." not in result.output


def test_verbose_flag_short(runner: CliRunner, valid_swagger_file):
    """Test command with verbose flag (short form)."""
    result = runner.invoke(main, [valid_swagger_file, "-v"])

    assert "Verbose mode enabled." in result.output


def test_verbose_flag_long(runner: CliRunner, valid_swagger_file):
    """Test command with verbose flag (long form)."""
    result = runner.invoke(main, [valid_swagger_file, "--verbose"])

    assert "Verbose mode enabled." in result.output


def test_json_flag(runner: CliRunner, valid_swagger_file):
    """Test command with JSON output flag."""
    result = runner.invoke(main, [valid_swagger_file, "--json"])

    assert result.exit_code == 0


def test_missing_swagger_file(runner: CliRunner):
    """Test command when swagger_file is missing."""
    result = runner.invoke(main)
    assert result.exit_code == 2
    assert "Error: Missing argument 'SWAGGER_FILE'." in result.output


def test_version_flag(runner: CliRunner):
    """Test command with the version flag."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "swagger-validator, version " in result.output
