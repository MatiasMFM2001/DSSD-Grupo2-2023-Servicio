from __future__ import annotations
from src.api.responses.base_response import BaseResponse
from typing import Iterable


"""Respuesta JSON exitosa a enviar como respuesta de la API REST."""
class OKResponse(BaseResponse):
    def __init__(self, *global_success: str, **fields: any) -> None:
        super().__init__(global_success=global_success, **fields)

    @property
    def global_success(self):
        return self.data["global_success"]

    @property
    def fields(self):
        return self.data["fields"]

    def to_flask_response(self, http_code: int = 200) -> Response:
        return super().to_flask_response(http_code)
