from flask import Blueprint, request

from src.core.business.furniture_manager import FurnitureManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

furniture_api_bp = Blueprint("furniture_api_bp", __name__, url_prefix="/furnitures")
furnitures_m = FurnitureManager()


@furniture_api_bp.route("/list", methods=["GET"])
@auth_m.permission_required("furniture_list")
def furnitures_of_club():
    """Obtiene todos los muebles de la colección."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        furnitures = paginator_to_json(
            furnitures_m.get_furnitures_paginator(page_number)
        )
        return SimpleOKResponse(furnitures=furnitures)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@furniture_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("furniture_create")
def create_furniture():
    values, error = get_json({"name", "initial_fabrication_term", "final_fabrication_term", "estimated_launch_date"})

    if error:
        return error

    furniture = furnitures_m.create(**values)
    return SimpleOKResponse("Colección creada correctamente", furniture_id=furniture.id)

@furniture_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("furniture_list")
def all_furnitures():
    """Obtiene todos los muebles de la colección."""

    furnitures = to_json(furnitures_m.filter_get_list())
    
    return SimpleOKResponse(furnitures=furnitures)