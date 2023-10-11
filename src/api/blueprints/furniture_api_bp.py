from flask import Blueprint, request

from src.core.business.furniture_manager import FurnitureManager
from src.core.business.collection_manager import CollectionManager
from src.core.business.category_manager import CategoryManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

furniture_api_bp = Blueprint("furniture_api_bp", __name__, url_prefix="/furnitures")
furnitures_m = FurnitureManager()
collection_m = CollectionManager()
categories_m = CategoryManager()


@furniture_api_bp.route("/list", methods=["GET"])
@auth_m.permission_required("furniture_list")
def furnitures_of_club():
    """Obtiene todos los muebles de la colección."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")
    
    if error:
        return error

    collection, error = api_validate_id(collection_m, request.args, tuple_name="La colección", key="collection_id")

    if error:
        return error
    
    try:
        furnitures = paginator_to_json(
            furnitures_m.filter_by_get_paginator(page_number, collection=collection)
        )
        return SimpleOKResponse(furnitures=furnitures)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")

@furniture_api_bp.route("/get", methods=["GET"])
@auth_m.permission_required("furniture_show")
def furniture_by_id():
    """Obtiene todos los muebles de la colección."""

    furniture, error = api_validate_id(furnitures_m, request.args, tuple_name="El mueble")

    if error:
        return error

    return SimpleOKResponse(furniture=furniture.get_json())

@furniture_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("furniture_create")
def create_furniture():
    values, error = get_json({"name", "description", "image", "collection_id", "categories", "image"})
    
    if error:
        return error
    
    if not values["collection_id"]:
        return SimpleErrorResponse(400, "El atributo collection_id está vacío")
    
    collection = collection_m.get(int(values["collection_id"]))
    
    del values["collection_id"]
    values["categories"] = [categories_m.get(id) for id in values["categories"]]
    del values["image"]
    
    furniture = furnitures_m.create(collection=collection, **values)
    return SimpleOKResponse("Colección creada correctamente", furniture_id=furniture.id)

@furniture_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("furniture_list")
def all_furnitures():
    """Obtiene todos los muebles de la colección."""

    furnitures = to_json(furnitures_m.filter_get_list())
    
    return SimpleOKResponse(furnitures=furnitures)