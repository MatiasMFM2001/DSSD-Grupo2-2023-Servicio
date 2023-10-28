from flask import Blueprint, request

from src.core.business.material_manager import MaterialManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id, api_validate_string
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

material_api_bp = Blueprint("material_api_bp", __name__, url_prefix="/materials")
materials_m = MaterialManager()


@material_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("material_create")
def create_material():
    values, error = get_json({"name", "price", "arrivalDate", "businessName"})

    if error:
        return error

    materials_m.create(**values)
    return SimpleOKResponse("Material creado correctamente")

@material_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("material_list")
def all_materials():
    """Obtiene todos los materiales."""

    materials = to_json(materials_m.filter_get_list())
    
    return SimpleOKResponse(materials=materials)

@material_api_bp.route("/getById", methods=["GET"])
@auth_m.permission_required("material_show")
def material_by_id():
    """Obtiene un material según su ID."""
    
    material, error = api_validate_id(
        materials_m,                   
        request.args,
        key="id",
        tuple_name="El material", 
    )

    if error:
        return error

    return SimpleOKResponse(material=material.get_json())

@material_api_bp.route("/getByName", methods=["GET"])
@auth_m.permission_required("material_show")
def material_by_name():
    """Obtiene un material según su nombre."""
    material, error = api_validate_string(
        materials_m,                   
        request.args,
        key="name",
        tuple_meaning="El material",
        key_meaning="nombre"
    )

    if error:
        return error

    return SimpleOKResponse(material=material[0].get_json())