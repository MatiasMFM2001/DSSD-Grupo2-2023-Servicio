from __future__ import annotations
from flask import json, current_app


"""Respuesta JSON base a enviar como respuesta de la API REST."""
class BaseResponse:
    def __init__(self, **initial_data: any) -> None:
        self.data = initial_data

    def add_data(self, key: str, value: any) -> None:
        self.data[key] = value

    def to_flask_response(self, http_code: int) -> Response:
        return current_app.response_class(
            response=json.dumps(self.data),
            status=http_code,
            mimetype="application/json",
        )
