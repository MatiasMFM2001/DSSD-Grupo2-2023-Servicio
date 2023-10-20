from flask import Blueprint, request

from src.core.business.slot_manager import SlotManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

slot_api_bp = Blueprint("slot_api_bp", __name__, url_prefix="/slots")
slots_m = SlotManager()


@slot_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("slot_create")
def create_slot():
    values, error = get_json({"beginning", "price", "end", "businessName"})

    if error:
        return error

    slots_m.create(**values)
    return SimpleOKResponse("Slot creado correctamente")

@slot_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("slot_list")
def all_slots():
    """Obtiene todos los slots."""

    slots = to_json(slots_m.filter_get_list())
    
    return SimpleOKResponse(slots=slots)

@slot_api_bp.route("/get", methods=["GET"])
@auth_m.permission_required("slot_show")
def slot_by_id():
    """Obtiene un slot según su ID."""
    
    slot, error = api_validate_id(slots_m, request.args, tuple_name="El slot")

    if error:
        return error

    return SimpleOKResponse(slot=slot.get_json())

@slot_api_bp.route("/reserve", methods=["GET"])
@auth_m.permission_required("slot_show")
def reserve_slot():
    """Reserva un slot de fabricación"""
    slot, error = api_validate_id(slots_m, request.args, tuple_name="El slot")

    if error:
        return error

    slots_m.update(slot.id, reserved=True)

    return SimpleOKResponse(slot=slot.get_json())