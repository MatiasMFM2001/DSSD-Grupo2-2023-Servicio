from flask import Blueprint, request

from src.core.business.fabrication_slot_manager import FabricationSlotManager

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json
from werkzeug.exceptions import HTTPException
from random import uniform

tick_api_bp = Blueprint("tick_api_bp", __name__, url_prefix="/tick")
fabrication_slots_m = FabricationSlotManager()

@tick_api_bp.route("/slot_progress", methods=["GET"])
@auth_m.permission_required("tick_show")
def tick_progreso():
    """Obtiene porcentaje de progreso."""
    
    slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    if error:
        return error
    
    if not slot.reserved:
        return SimpleErrorResponse(400, f"El slot de ID {slot.id} no está reservado")
    
    progress = slot.fabrication_progress + uniform(0.0, 10.0)
    progress = min(progress, 100.0)

    fabrication_slots_m.update(slot.id, fabrication_progress=progress)
    return SimpleOKResponse("Porcentaje de slot incrementado correctamente")

@tick_api_bp.route("/arrival", methods=["GET"])
@auth_m.permission_required("tick_show")
def tick_arrival():
    """Obtiene porcentaje de progreso."""
    
    number = round(uniform(0.7, 10.0), 2)
    #slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    #if error:
    #    return error

    return SimpleOKResponse(number=number)