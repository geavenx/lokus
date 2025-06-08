"""Swagger-Validator Module.

This module contains the main logic to parse, analyze and report all
kinds of issues in OpenAPI spec files.

"""

# This variable is only used to check for ImportErrors induced by users running as a script rather than as a module/package
import_error_var = None

__shortname__ = "Swagger-Validator"
__longname__ = "Swagger-Validator: Find issues in your APIs from the docs"
__version__ = "0.1.0"
