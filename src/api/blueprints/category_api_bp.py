from flask import Blueprint, request

from src.core.business.category_manager import CategoryManager

from src.api.helpers import paginator_to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

category_api_bp = Blueprint("category_api_bp", __name__, url_prefix="/categories")
categories_m = CategoryManager()


@category_api_bp.route("/list", methods=["GET"])
@auth_m.permission_required("category_list")
def categories_of_club():
    """Obtiene todas las categorias que se realizan en el club."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        categories = paginator_to_json(
            categories_m.get_categories_paginator(page_number)
        )
        return SimpleOKResponse(categories=categories)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@category_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("category_create")
def create_category():
    values, error = get_json({"name"})

    if error:
        return error

    categories_m.create(**values)
    return SimpleOKResponse("Tu contraseña ha sido actualizada correctamente")
