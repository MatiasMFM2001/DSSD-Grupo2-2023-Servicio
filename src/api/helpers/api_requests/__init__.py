from __future__ import annotations
from typing import Tuple, Optional, Set, TypeVar
from flask import request
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse

T = TypeVar("T")


def value_tuple(value: T) -> Tuple[T, None]:
    return (value, None)

def error_tuple(error: SimpleErrorResponse) -> Tuple[None, SimpleErrorResponse]:
    return (None, error)

def to_string(keys: Set[str]):
    return f"{{{', '.join(keys)}}}"


def force_fields(
    entries: Dict[str, str],
    required_fields: Set[str] = set(),
    allow_extra_keys: bool = False,
):
    keys = entries.keys()
    keys_str = to_string(keys)
    
    if not required_fields <= keys:
        diff_str = to_string(required_fields - keys)
        
        return error_tuple(
            SimpleErrorResponse(
                400,
                f"El JSON debe contener las claves {to_string(required_fields)}, pero tiene {keys_str} (le falta {diff_str})",
            )
        )

    if not allow_extra_keys and keys != required_fields:
        diff_str = to_string(keys - required_fields)
        
        return error_tuple(
            SimpleErrorResponse(
                400,
                f"El JSON debe contener exactamente las claves {to_string(required_fields)}, pero tiene {keys_str} (le sobra {diff_str})",
            )
        )
    
    return value_tuple(entries)

def get_json(
    required_fields: Set[str] = set(),
    allow_extra_keys: bool = False,
) -> Tuple[Optional[object], Optional[SimpleErrorResponse]]:
    values = request.get_json(silent=True)

    if values is None:
        return error_tuple(
            SimpleErrorResponse(400, "JSON inválido, o sin Content-Type")
        )

    if not isinstance(values, dict):
        return error_tuple(
            SimpleErrorResponse(400, f"El JSON enviado no es un diccionario: {values}")
        )
    
    return force_fields(values, required_fields, allow_extra_keys)


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
