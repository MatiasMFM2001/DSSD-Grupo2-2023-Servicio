from flask import Blueprint, request

from src.core.business.service_manager import DisciplineManager
from src.core.business.config_manager import ConfigManager

from src.api.helpers import paginator_to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.web.helpers.controller_helpers import get_int

club_api_bp = Blueprint("club_api_bp", __name__, url_prefix="/club")
disciplines_m = DisciplineManager()

config_m = ConfigManager()

@club_api_bp.route("/disciplines", methods=["GET"])
def disciplines_of_club():
    """Obtiene todas las disciplinas que se realizan en el club."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        disciplines = paginator_to_json(
            disciplines_m.filter_by_get_paginator(page_number)
        )
        return SimpleOKResponse(disciplines=disciplines)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@club_api_bp.route("/info", methods=["GET"])
def club_info():
    """Obtiene información importante y de contacto sobre el club."""

    return SimpleOKResponse(
        email=config_m.get_field("club_email"), phone=config_m.get_field("phone_number")
    )