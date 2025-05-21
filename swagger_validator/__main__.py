#! /usr/bin/env python3

"""
Swagger-Validator: Find issues in your APIs from the docs module

This module contains the main logic to parse, analyze and report all
kinds of issues in OpenAPI spec files.
"""

import sys

if __name__ == "__main__":
    # check if user is using the correct version of python
    python_version = sys.version.split()[0]

    if sys.version_info < (3, 8):
        print(
            f"Swagger-validator requires python 3.8+\nYou are using {python_version}, which is not supported by Swagger-validator."
        )
        sys.exit(1)

    from swagger_validator import main

    main.main()
