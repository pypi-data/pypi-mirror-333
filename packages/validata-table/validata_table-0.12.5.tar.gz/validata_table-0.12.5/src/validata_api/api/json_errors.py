"""Respond JSON general_errors instead of HTML. Useful for HTTP/JSON APIs."""

# From https://coderwall.com/p/xq88zg/json-exception-handler-for-flask

import logging
from typing import Any, NoReturn, Optional, Type, Union

import ujson as json
from flask import Flask, Response, abort
from werkzeug.exceptions import HTTPException, default_exceptions

from validata_core.domain.types import ErrType, TypedException
from validata_core.domain.types.metadata import AutoMetadata

log = logging.getLogger(__name__)


def abort_with_operation_error(
    operation_error: TypedException,
    status_code: int,
    args: dict,
) -> NoReturn:
    args = {**args, **operation_error.metadata.to_dict()}
    abort_json(status_code, args, str(operation_error), operation_error.type)


def abort_json(
    status_code: int,
    args: dict,
    message: Optional[str] = None,
    type: Optional[ErrType] = None,
) -> NoReturn:
    if message is None:
        exc = default_exceptions.get(status_code)
        if exc is not None:
            message = exc.description

    metadata_dict = AutoMetadata().to_dict()

    body = {**metadata_dict, "error": {"message": message}}

    if type:
        body["error"]["type"] = type.value

    response = make_json_response(body, args, status_code=status_code)

    if status_code == 500:
        log.error((message, args, status_code))

    abort(response)


def error_handler(error: Exception) -> Response:
    status_code = error.code if isinstance(error, HTTPException) else 500
    message = (
        str(error) if isinstance(error, HTTPException) else "Internal server error"
    )
    return make_json_response({"message": message}, args=None, status_code=status_code)


def make_json_response(
    data: dict, args: Optional[dict], status_code: Optional[int] = None
) -> Response:
    formatted_report = {**format_args(args), **data}
    return Response(
        json.dumps(formatted_report, default=lambda x: str(x)),
        mimetype="application/json",
        status=status_code,
    )


def format_args(args: Optional[dict]) -> dict:
    if args:
        return {
            "schema": args.get("schema"),
            "url": args.get("url"),
            "options": {
                "ignore_header_case": args.get("ignore_header_case"),
                "include_resource_data": args.get("include_resource_data"),
            },
        }
    else:
        return {}


class JsonErrors:
    """
    Respond JSON general_errors.
    Register error handlers for all HTTP exceptions.

    Special case: when FLASK_DEBUG=1 render HTTP 500 general_errors as HTML instead of JSON.
    """

    def __init__(self, app: Optional[Flask] = None):
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        self.register(HTTPException)
        for code in default_exceptions:
            self.register(code)

    def register(
        self, exception_or_code: Union[Type[Exception], int], handler: Any = None
    ):
        self.app.errorhandler(exception_or_code)(handler or error_handler)
