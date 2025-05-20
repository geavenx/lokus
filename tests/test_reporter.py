#!/usr/bin/env python3
import pytest
import json
from src.reporter import report_findings


@pytest.fixture
def sample_findings_list():
    return [
        {
            "path": "info.contact.email",
            "key": "email",
            "type": "forbidden_key_at_path",
            "message": "Publicly exposing contact emails in API specs can lead to spam or phishing.",
        },
        {
            "path": "components.securitySchemes.LegacyApiKey.x-api-key",
            "key": "x-api-key",
            "type": "forbidden_key",
            "message": 'Key \t"x-api-key"\t is globally forbidden.',
        },
    ]


@pytest.fixture
def empty_findings_list():
    return []


# Test text output with findings
def test_report_findings_text_with_issues(capsys, sample_findings_list):
    exit_code = report_findings(
        sample_findings_list, "test_spec.yaml", "test_config.yaml", "text"
    )
    captured = capsys.readouterr()
    assert "STATUS: VALIDATION FAILED" in captured.out
    assert "info.contact.email" in captured.out
    assert "x-api-key" in captured.out
    assert f'Key \t"x-api-key"\t is globally forbidden.' in captured.out
    assert exit_code == 1


# Test text output with no findings
# def test_report_findings_text_no_issues(capsys, empty_findings_list):
#     exit_code = report_findings(
#         empty_findings_list, "clean_spec.yaml", "test_config.yaml", "text"
#     )
#     captured = capsys.readouterr()
#     assert "STATUS: VALIDATION PASSED" in captured.out
#     assert "No forbidden items found." in captured.out
#     assert exit_code == 0


# Test JSON output with findings
# def test_report_findings_json_with_issues(capsys, sample_findings_list):
#     exit_code = report_findings(
#         sample_findings_list, "test_spec.yaml", "test_config.yaml", "json"
#     )
#     captured = capsys.readouterr()
#     try:
#         output_json = json.loads(captured.out)
#     except json.JSONDecodeError:
#         pytest.fail("Output was not valid JSON.")
#
#     assert output_json["status"] == "failed"
#     assert output_json["swagger_file_path"] == "test_spec.yaml"
#     assert output_json["config_file_path"] == "test_config.yaml"
#     assert len(output_json["findings"]) == 2
#     assert output_json["findings"][0]["path"] == "info.contact.email"
#     assert output_json["findings"][1]["key"] == "x-api-key"
#     assert exit_code == 1
#
#
# # Test JSON output with no findings
# def test_report_findings_json_no_issues(capsys, empty_findings_list):
#     exit_code = report_findings(
#         empty_findings_list, "clean_spec.yaml", "test_config.yaml", "json"
#     )
#     captured = capsys.readouterr()
#     try:
#         output_json = json.loads(captured.out)
#     except json.JSONDecodeError:
#         pytest.fail("Output was not valid JSON.")
#
#     assert output_json["status"] == "passed"
#     assert output_json["swagger_file_path"] == "clean_spec.yaml"
#     assert len(output_json["findings"]) == 0
#     assert exit_code == 0


# Test verbose flag (currently doesn't change reporter output itself, but test it's accepted)
def test_report_findings_verbose_flag(capsys, sample_findings_list):
    exit_code = report_findings(
        sample_findings_list, "test_spec.yaml", "test_config.yaml", "text", verbose=True
    )
    captured = capsys.readouterr()  # Just ensure it runs without error
    assert "STATUS: VALIDATION FAILED" in captured.out
    assert exit_code == 1
