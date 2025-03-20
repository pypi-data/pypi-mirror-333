#!/usr/bin/env python3

"""Validate tabular file (CSV, XLS, etc.) against a table schema and custom validators,
and adding pre-checks which can fix automatically some errors to reach the real checks.
"""

import argparse
import json
import logging
import sys

import validators

from validata_core import resource_service as resource
from validata_core import validation_service
from validata_core.domain.table_resource import TableResource


def transform_args_source(args_source: str) -> TableResource:
    # Deal with url
    if validators.url(args_source):
        validata_resource = resource.from_remote_file(args_source)
    else:
        # Deal with Path
        with open(args_source, "rb") as file:
            content = file.read()
        validata_resource = resource.from_file_content(args_source, content)
    return validata_resource


def cli():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "source", help="URL or path to tabular file (CSV, XLS, etc.) to validate"
    )
    parser.add_argument("--log", default="WARNING", help="level of logging messages")
    parser.add_argument("--schema", help="URL or path to table schema JSON file")
    parser.add_argument(
        "--ignore_header_case",
        action="store_false",
        help="Cancel header case sensitivity",
        required=False,
    )
    args = parser.parse_args()

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: {}".format(args.log))
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s",
        level=numeric_level,
        stream=sys.stderr,  # script outputs data
    )
    try:
        validata_resource = transform_args_source(args.source)
        report = validation_service.validate_resource(
            validata_resource, args.schema, args.ignore_header_case
        )
        validata_formatted_report = report.to_dict()

        json.dump(
            validata_formatted_report,
            sys.stdout,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    except Exception as err:
        logging.error(err)

    return 0
