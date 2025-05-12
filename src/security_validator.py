from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class SecurityIssueSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class SecurityIssue:
    rule_id: str
    title: str
    description: str
    severity: SecurityIssueSeverity
    path: str
    recommendation: str
    reference: str


class SecurityValidator:
    def __init__(self):
        self.issues: List[SecurityIssue] = []

    def validate_spec(self, spec: Dict[str, Any]) -> List[SecurityIssue]:
        """Main validation method that runs all security checks"""
        self.issues = []

        # Run all security checks
        self._check_broken_object_level_auth(spec)
        self._check_broken_authentication(spec)
        self._check_broken_object_property_level_auth(spec)
        self._check_unrestricted_resource_consumption(spec)
        self._check_broken_function_level_auth(spec)
        # self._check_unrestricted_sensitive_flows(spec)
        # self._check_ssrf(spec)
        # self._check_security_misconfiguration(spec)
        # self._check_improper_inventory(spec)
        # self._check_unsafe_api_consumption(spec)

        return self.issues

    def _check_broken_object_level_auth(self, spec: Dict[str, Any]) -> None:
        """Check for Broken Object Level Authorization (BOLA)"""
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() in ["get", "put", "delete", "patch"]:
                    # Check if the endpoint has proper authorization
                    if not operation.get("security"):
                        self.issues.append(
                            SecurityIssue(
                                rule_id="BOLA-001",
                                title="Missing Authorization",
                                description=f"Endpoint {path} {method.upper()} lacks proper authorization requirements",
                                severity=SecurityIssueSeverity.HIGH,
                                path=f"paths.{path}.{method}",
                                recommendation="Add security requirements to the endpoint",
                                reference="https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/",
                            )
                        )

    def _check_broken_authentication(self, spec: Dict[str, Any]) -> None:
        """Check for Broken Authentication"""
        security_schemes = spec.get("components", {}).get("securitySchemes", {})

        # Check for weak authentication schemes
        for scheme_name, scheme in security_schemes.items():
            if scheme.get("type") == "apiKey":
                if not scheme.get("in") or scheme.get("in") not in ["header", "cookie"]:
                    self.issues.append(
                        SecurityIssue(
                            rule_id="AUTH-001",
                            title="Broken Authentication",
                            description=f"API Key '{scheme_name}' is not properly secured",
                            severity=SecurityIssueSeverity.HIGH,
                            path=f"components.securitySchemes.{scheme_name}",
                            recommendation="Configure API key to be sent in header or cookie",
                            reference="https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/",
                        )
                    )

    def _check_broken_object_property_level_auth(self, spec: Dict[str, Any]) -> None:
        """Check for Broken Object Property Level Authorization (BOPLA)"""
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() in ["put", "patch"]:
                    # Check if the operation has proper property-level authorization
                    if not operation.get("security"):
                        self.issues.append(
                            SecurityIssue(
                                rule_id="BOPLA-001",
                                title="Missing Property Level Authorization",
                                description=f"Endpoint {path} {method.upper()} lacks property-level authorization",
                                severity=SecurityIssueSeverity.HIGH,
                                path=f"paths.{path}.{method}",
                                recommendation="Implement property-level authorization checks",
                                reference="https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/",
                            )
                        )

    def _check_unrestricted_resource_consumption(self, spec: Dict[str, Any]) -> None:
        """Check for Unrestricted Resource Consumption"""
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                # Check for rate limiting headers in responses
                responses = operation.get("responses", {})
                if "429" not in responses:
                    self.issues.append(
                        SecurityIssue(
                            rule_id="RATE-001",
                            title="Missing Rate Limiting",
                            description=f"Endpoint {path} {method.upper()} lacks rate limiting configuration",
                            severity=SecurityIssueSeverity.MEDIUM,
                            path=f"paths.{path}.{method}.responses",
                            recommendation="Add rate limiting configuration and 429 response",
                            reference="https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/",
                        )
                    )

    def _check_broken_function_level_auth(self, spec: Dict[str, Any]) -> None:
        """Check for Broken Function Level Authorization (BFLA)"""
        paths = spec.get("paths", {})
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.lower() in ["post", "put", "delete"]:
                    # Check for proper function-level authorization
                    if not operation.get("security"):
                        self.issues.append(
                            SecurityIssue(
                                rule_id="BFLA-001",
                                title="Missing Function Level Authorization",
                                description=f"Endpoint {path} {method.upper()} lacks function-level authorization",
                                severity=SecurityIssueSeverity.HIGH,
                                path=f"paths.{path}.{method}",
                                recommendation="Add function-level authorization requirements",
                                reference="https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/",
                            )
                        )

    # def _check_unrestricted_sensitive_flows(self, spec: Dict[str, Any]) -> None:
    #     """Check for Unrestricted Access to Sensitive Business Flows"""
    #     paths = spec.get("paths", {})
    #     sensitive_keywords = [
    #         "admin",
    #         "user",
    #         "password",
    #         "token",
    #         "auth",
    #         "login",
    #         "register",
    #     ]
    #
    #     for path, path_item in paths.items():
    #         if any(keyword in path.lower() for keyword in sensitive_keywords):
    #             for method, operation in path_item.items():
    #                 if not operation.get("security"):
    #                     self.issues.append(
    #                         SecurityIssue(
    #                             rule_id="FLOW-001",
    #                             title="Unrestricted Sensitive Flow",
    #                             description=f"Sensitive endpoint {path} {method.upper()} lacks proper security controls",
    #                             severity=SecurityIssueSeverity.HIGH,
    #                             path=f"paths.{path}.{method}",
    #                             recommendation="Add proper security controls for sensitive operations",
    #                         )
    #                     )
    #
    # def _check_ssrf(self, spec: Dict[str, Any]) -> None:
    #     """Check for Server Side Request Forgery (SSRF)"""
    #     paths = spec.get("paths", {})
    #     for path, path_item in paths.items():
    #         for method, operation in path_item.items():
    #             # Check for URL parameters that might be vulnerable to SSRF
    #             parameters = operation.get("parameters", [])
    #             for param in parameters:
    #                 if param.get("name", "").lower() in [
    #                     "url",
    #                     "uri",
    #                     "path",
    #                     "src",
    #                     "dest",
    #                 ]:
    #                     self.issues.append(
    #                         SecurityIssue(
    #                             rule_id="SSRF-001",
    #                             title="Potential SSRF Vulnerability",
    #                             description=f"Parameter '{param['name']}' in {path} {method.upper()} might be vulnerable to SSRF",
    #                             severity=SecurityIssueSeverity.HIGH,
    #                             path=f"paths.{path}.{method}.parameters",
    #                             recommendation="Implement URL validation and whitelisting",
    #                         )
    #                     )
    #
    # def _check_security_misconfiguration(self, spec: Dict[str, Any]) -> None:
    #     """Check for Security Misconfiguration"""
    #     # Check for proper security schemes
    #     if not spec.get("components", {}).get("securitySchemes"):
    #         self.issues.append(
    #             SecurityIssue(
    #                 rule_id="CONFIG-001",
    #                 title="Missing Security Schemes",
    #                 description="No security schemes defined in the API specification",
    #                 severity=SecurityIssueSeverity.HIGH,
    #                 path="components.securitySchemes",
    #                 recommendation="Define proper security schemes",
    #             )
    #         )
    #
    # def _check_improper_inventory(self, spec: Dict[str, Any]) -> None:
    #     """Check for Improper Inventory Management"""
    #     # Check for proper API versioning
    #     if not spec.get("info", {}).get("version"):
    #         self.issues.append(
    #             SecurityIssue(
    #                 rule_id="INV-001",
    #                 title="Missing API Version",
    #                 description="API version is not specified",
    #                 severity=SecurityIssueSeverity.MEDIUM,
    #                 path="info.version",
    #                 recommendation="Add API version information",
    #             )
    #         )
    #
    # def _check_unsafe_api_consumption(self, spec: Dict[str, Any]) -> None:
    #     """Check for Unsafe API Consumption"""
    #     paths = spec.get("paths", {})
    #     for path, path_item in paths.items():
    #         for method, operation in path_item.items():
    #             # Check for proper content type validation
    #             if method.lower() in ["post", "put", "patch"]:
    #                 if not operation.get("requestBody", {}).get("content"):
    #                     self.issues.append(
    #                         SecurityIssue(
    #                             rule_id="CONS-001",
    #                             title="Missing Content Type Validation",
    #                             description=f"Endpoint {path} {method.upper()} lacks content type validation",
    #                             severity=SecurityIssueSeverity.MEDIUM,
    #                             path=f"paths.{path}.{method}.requestBody",
    #                             recommendation="Add content type validation",
    #                         )
    #                     )
