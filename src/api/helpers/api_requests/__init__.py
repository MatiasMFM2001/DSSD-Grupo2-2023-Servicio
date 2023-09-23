from __future__ import annotations
from typing import Tuple, Optional, Set, TypeVar
from flask import request
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse

T = TypeVar("T")


def value_tuple(value: T) -> Tuple[T, None]:
    return (value, None)


def error_tuple(error: SimpleErrorResponse) -> Tuple[None, SimpleErrorResponse]:
    return (None, error)


def get_json(
    required_fields: Set[str] = set(),
) -> Tuple[Optional[object], Optional[SimpleErrorResponse]]:
    values = request.get_json(silent=True)

    if values is None:
        return error_tuple(
            SimpleErrorResponse(400, "JSON inválido, o sin Content-Type")
        )

    keys = values.keys()

    if not required_fields <= keys:
        keys_str = "{{{keys}}}".format(keys=", ".join(keys))
        return error_tuple(
            SimpleErrorResponse(
                400,
                f"El JSON debe contener las claves {required_fields}, pero tiene {keys_str}",
            )
        )

    return value_tuple(values)


def get_int(base: int = 10) -> Tuple[Optional[int], Optional[SimpleErrorResponse]]:
    values = request.data

    try:
        return value_tuple(int(values, base))
    except ValueError:
        return error_tuple(
            SimpleErrorResponse(
                400,
                f"Los datos POST deben ser un número entero en base {base}, pero son {values}",
            )
        )
