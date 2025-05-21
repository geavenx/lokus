#!/usr/bin/env python3
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class LGPDIssueSeverity(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class LGPDIssue:
    rule_id: str
    title: str
    description: str
    severity: LGPDIssueSeverity
    path: str
    recommendation: str
    reference: Optional[str] = None


class LGPDValidator:
    def __init__(self):
        self.issues: List[LGPDIssue] = []

        # Define regex patterns for sensitive data
        self.sensitive_patterns = {
            "cpf": re.compile(
                r"\d{3}\.\d{3}\.\d{3}-\d{2}"
            ),  # CPF format: XXX.XXX.XXX-XX
            "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
            "phone": re.compile(r"\+?(\d{2})?\s*\(?\d{2}\)?\s*\d{4,5}-?\d{4}"),
            "rg": re.compile(r"\d{2}\.\d{3}\.\d{3}-?\d"),
            "cnpj": re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"),
        }

        # Define sensitive field names
        self.sensitive_field_names = {
            "cpf",
            "cnpj",
            "rg",
            "email",
            "telefone",
            "phone",
            "celular",
            "mobile",
            "endereco",
            "address",
            "cep",
            "postal_code",
            "data_nascimento",
            "birth_date",
            "nome",
            "name",
            "sobrenome",
            "surname",
            "nome_completo",
            "full_name",
            "biometrico",
            "biometric",
            "saude",
            "health",
            "prontuario",
            "medical_record",
            "dados_sensiveis",
            "sensitive_data",
            "dados_pessoais",
            "personal_data",
        }

    def validate_spec(self, spec: Dict[str, Any]) -> List[LGPDIssue]:
        """Main validation method that runs all LGPD compliance checks"""
        self.issues = []

        # Run all LGPD compliance checks
        self._check_sensitive_data_in_examples(spec)
        self._check_sensitive_data_in_descriptions(spec)
        self._check_sensitive_field_names(spec)
        self._check_direct_identifiers_in_paths(spec)
        self._check_data_minimization(spec)
        self._check_purpose_limitation(spec)

        return self.issues

    def _check_sensitive_data_in_examples(self, spec: Dict[str, Any]) -> None:
        """Check for sensitive data in example values"""

        def check_value(value: str, path: str) -> None:
            for pattern_name, pattern in self.sensitive_patterns.items():
                if pattern.search(value):
                    self.issues.append(
                        LGPDIssue(
                            rule_id="LGPD-001",
                            title="Sensitive Data in Example",
                            description=f"Example contains {pattern_name} data: {value}",
                            severity=LGPDIssueSeverity.HIGH,
                            path=path,
                            recommendation=f"Replace the {pattern_name} with a placeholder value",
                            reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                        )
                    )

        def traverse_examples(data: Any, current_path: str) -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    if key == "example" and isinstance(value, str):
                        check_value(value, new_path)
                    traverse_examples(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    traverse_examples(item, f"{current_path}[{i}]")

        traverse_examples(spec, "")

    def _check_sensitive_data_in_descriptions(self, spec: Dict[str, Any]) -> None:
        """Check for sensitive data in descriptions"""

        def check_value(value: str, path: str) -> None:
            for pattern_name, pattern in self.sensitive_patterns.items():
                if pattern.search(value):
                    self.issues.append(
                        LGPDIssue(
                            rule_id="LGPD-002",
                            title="Sensitive Data in Description",
                            description=f"Description contains {pattern_name} data: {value}",
                            severity=LGPDIssueSeverity.HIGH,
                            path=path,
                            recommendation=f"Remove the {pattern_name} from the description",
                            reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                        )
                    )

        def traverse_descriptions(data: Any, current_path: str) -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    if key == "description" and isinstance(value, str):
                        check_value(value, new_path)
                    traverse_descriptions(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    traverse_descriptions(item, f"{current_path}[{i}]")

        traverse_descriptions(spec, "")

    def _check_sensitive_field_names(self, spec: Dict[str, Any]) -> None:
        """Check for sensitive field names in schemas and parameters"""

        def check_field_name(name: str, path: str) -> None:
            name_lower = name.lower()
            if name_lower in self.sensitive_field_names:
                self.issues.append(
                    LGPDIssue(
                        rule_id="LGPD-003",
                        title="Sensitive Field Name",
                        description=f"Field name '{name}' suggests sensitive data",
                        severity=LGPDIssueSeverity.MEDIUM,
                        path=path,
                        recommendation="Consider using a more generic field name or documenting the data protection measures",
                        reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                    )
                )

        def traverse_fields(data: Any, current_path: str) -> None:
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    if key == "name" and isinstance(value, str):
                        check_field_name(value, new_path)
                    traverse_fields(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    traverse_fields(item, f"{current_path}[{i}]")

        traverse_fields(spec, "")

    def _check_direct_identifiers_in_paths(self, spec: Dict[str, Any]) -> None:
        """Check for direct identifiers in API paths"""
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            # Check for common identifier patterns in path
            if any(
                pattern in path.lower()
                for pattern in ["/cpf/", "/cnpj/", "/rg/", "/email/"]
            ):
                self.issues.append(
                    LGPDIssue(
                        rule_id="LGPD-004",
                        title="Direct Identifier in Path",
                        description=f"Path '{path}' contains direct identifier",
                        severity=LGPDIssueSeverity.HIGH,
                        path=f"paths.{path}",
                        recommendation="Use indirect identifiers (e.g., UUID) instead of direct identifiers in paths",
                        reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                    )
                )

    def _check_data_minimization(self, spec: Dict[str, Any]) -> None:
        """Check for data minimization principle compliance"""

        def check_schema_properties(schema: Dict[str, Any], path: str) -> None:
            properties = schema.get("properties", {})
            required = schema.get("required", [])

            # Check if all properties are necessary
            for prop_name, prop in properties.items():
                if prop_name not in required and not prop.get("description"):
                    self.issues.append(
                        LGPDIssue(
                            rule_id="LGPD-005",
                            title="Missing Property Justification",
                            description=f"Optional property '{prop_name}' lacks justification",
                            severity=LGPDIssueSeverity.MEDIUM,
                            path=f"{path}.properties.{prop_name}",
                            recommendation="Add a description explaining why this property is necessary",
                            reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                        )
                    )

        def traverse_schemas(data: Any, current_path: str) -> None:
            if isinstance(data, dict):
                if "type" in data and data["type"] == "object":
                    check_schema_properties(data, current_path)
                for key, value in data.items():
                    new_path = f"{current_path}.{key}" if current_path else key
                    traverse_schemas(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    traverse_schemas(item, f"{current_path}[{i}]")

        traverse_schemas(spec, "")

    def _check_purpose_limitation(self, spec: Dict[str, Any]) -> None:
        """Check for purpose limitation principle compliance"""

        def check_operation_purpose(operation: Dict[str, Any], path: str) -> None:
            if not operation.get("description"):
                self.issues.append(
                    LGPDIssue(
                        rule_id="LGPD-006",
                        title="Missing Operation Purpose",
                        description=f"Operation at '{path}' lacks purpose description",
                        severity=LGPDIssueSeverity.MEDIUM,
                        path=path,
                        recommendation="Add a description explaining the purpose of data collection and processing",
                        reference="https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd",
                    )
                )

        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() in ["post", "put", "patch"]:
                    check_operation_purpose(operation, f"paths.{path}.{method}")
