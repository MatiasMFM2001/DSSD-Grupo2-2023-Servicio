from __future__ import annotations
from flask import json, current_app
from werkzeug.datastructures import MultiDict
from src.api.helpers.api_responses.base_response import BaseResponse


"""Respuesta JSON errónea a enviar como respuesta de la API REST."""
class ErrorResponse(BaseResponse):
    def __init__(self, *global_errors: str, **field_errors: str) -> None:
        super().__init__(
            global_errors=global_errors, field_errors=MultiDict(field_errors)
        )

    @property
    def global_errors(self):
        return self.data["global_errors"]

    @property
    def field_errors(self):
        return self.data["field_errors"]

    def add_global_error(self, message: str) -> None:
        self.global_errors.append(message)

    def add_field_error(self, field_id: str, message: str) -> None:
        self.field_errors.add(field_id, message)
