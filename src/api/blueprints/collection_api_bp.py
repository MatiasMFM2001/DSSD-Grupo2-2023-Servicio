from flask import Blueprint, request

from src.core.business.collection_manager import CollectionManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
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
            collections_m.filter_by_get_paginator(page_number)
        )
        return SimpleOKResponse(collections=collections)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@collection_api_bp.route("/get", methods=["GET"])
@auth_m.permission_required("collection_show")
def collection_by_id():
    """Obtiene una colección por ID."""

    collection, error = api_validate_id(collections_m, request.args, tuple_name="El mueble")

    if error:
        return error

    return SimpleOKResponse(collection=collection.get_json())
    
@collection_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("collection_create")
def create_collection():
    values, error = get_json({"name", "initial_fabrication_term", "final_fabrication_term", "estimated_launch_date", "bonita_process_id", "bd_or_drive"})

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

@collection_api_bp.route("/end", methods=["POST"])
@auth_m.permission_required("collection_end")
def collection_end():
    collection, error = api_validate_id(collections_m, request.args, tuple_name="El mueble")

    if error:
        return error
    
    if not collection.editable:
        return SimpleErrorResponse(400, "La colección no es editable")
    
    collections_m.update(collection.id, editable=False)
    
    return SimpleOKResponse(collection=collection.get_json())