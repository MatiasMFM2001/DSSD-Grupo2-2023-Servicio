from flask import Blueprint, request

from src.core.business.material_request_manager import MaterialRequestManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

material_requests_api_bp = Blueprint("material_requests_api_bp", __name__, url_prefix="/material_requests")
material_requests_m = MaterialRequestManager()


@material_requests_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("material_request_create")
def create_material_request():
    values, error = get_json({"amount", "arrival_date", "material_id"})

    if error:
        return error

    material_requests_m.create(**values)
    return SimpleOKResponse("Slot creado correctamente")

@material_requests_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("material_request_list")
def all_material_requests():
    """Obtiene todos los material_requests."""

    material_requests = to_json(material_requests_m.filter_get_list())
    
    return SimpleOKResponse(material_requests=material_requests)

@material_requests_api_bp.route("/get", methods=["GET"])
@auth_m.permission_required("material_request_show")
def material_request_by_id():
    """Obtiene un material_request según su ID."""
    
    material_request, error = api_validate_id(material_requests_m, request.args, tuple_name="El material_request")

    if error:
        return error

    return SimpleOKResponse(material_request=material_request.get_json())

@material_requests_api_bp.route("/reserve", methods=["POST"])
@auth_m.permission_required("material_request_reserve")
def reserve_material_request():
    """Reserva un material_request de fabricación"""
    material_request, error = api_validate_id(material_requests_m, request.args, tuple_name="El material_request")

    if error:
        return error

    if material_request.reserved:
        return SimpleErrorResponse(f"El material_request de ID {material_request.id} ya estaba reservado")
      
    material_requests_m.update(material_request.id, reserved=True)

    return SimpleOKResponse(material_request=material_request.get_json())