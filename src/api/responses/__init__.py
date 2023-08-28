from __future__ import annotations
from src.api.responses.ok_response import OKResponse
from src.api.responses.error_response import ErrorResponse


def SimpleOKResponse(
    success_message: string = "", http_code: int = 200, **data: any
) -> Response:
    return OKResponse(success_message, **data).to_flask_response(http_code)


def SimpleErrorResponse(
    http_code: int, *global_errors: str, **field_errors: str
) -> Response:
    return ErrorResponse(*global_errors, **field_errors).to_flask_response(http_code)
