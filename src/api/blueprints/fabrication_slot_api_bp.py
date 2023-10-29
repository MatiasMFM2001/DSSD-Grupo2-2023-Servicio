from flask import Blueprint, request

from src.core.business.fabrication_slot_manager import FabricationSlotManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException

fabrication_slot_api_bp = Blueprint("fabrication_slot_api_bp", __name__, url_prefix="/slots")
fabrication_slots_m = FabricationSlotManager()


@fabrication_slot_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("slot_create")
def create_slot():
    values, error = get_json({"beginning", "price", "end", "producer_id"})

    if error:
        return error

    fabrication_slots_m.create(**values)
    return SimpleOKResponse("Slot creado correctamente")

@fabrication_slot_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("slot_list")
def all_slots():
    """Obtiene todos los slots."""
    slots = to_json(fabrication_slots_m.filter_get_list())
    return SimpleOKResponse(slots=slots)

@fabrication_slot_api_bp.route("/get", methods=["GET"])
@auth_m.permission_required("slot_show")
def slot_by_id():
    """Obtiene un slot según su ID."""
    
    slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    if error:
        return error

    return SimpleOKResponse(slot=slot.get_json())

@fabrication_slot_api_bp.route("/reserve", methods=["POST"])
@auth_m.permission_required("slot_reserve")
def reserve_slot():
    """Reserva un slot de fabricación"""
    slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    if error:
        return error

    if slot.reserved:
        return SimpleErrorResponse(400, f"El slot de ID {slot.id} ya estaba reservado")
      
    fabrication_slots_m.update(slot.id, reserved=True)

    return SimpleOKResponse("Slot reservado correctamente", slot=slot.get_json())