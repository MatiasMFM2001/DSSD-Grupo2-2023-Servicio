from flask import Blueprint, request

from src.core.business.collection_manager import CollectionManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

collection_api_bp = Blueprint("collection_api_bp", __name__, url_prefix="/collections")
collections_m = CollectionManager()


@collection_api_bp.route("/list", methods=["GET"])
@auth_m.permission_required("collection_list")
def collections_of_club():
    """Obtiene todas las categorias que se realizan en el club."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        collections = paginator_to_json(
            collections_m.get_collections_paginator(page_number)
        )
        return SimpleOKResponse(collections=collections)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@collection_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("collection_create")
def create_collection():
    values, error = get_json({"name", "initial_fabrication_term", "final_fabrication_term", "estimated_launch_date"})

    if error:
        return error

    collection = collections_m.create(**values)
    return SimpleOKResponse("Colección creada correctamente", collection_id=collection.id)

@collection_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("collection_list")
def all_collections():
    """Obtiene todas las categorias que se realizan en el club."""

    collections = to_json(collections_m.filter_get_list())
    
    return SimpleOKResponse(collections=collections)