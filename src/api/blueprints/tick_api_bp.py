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

@tick_api_bp.route("/percentage", methods=["GET"])
@auth_m.permission_required("tick_show")
def tick_progreso():
    """Obtiene porcentaje de progreso."""
    
    for slot in fabrication_slots_m.filter_by_get_list(reserved=True):
        progress = slot.fabrication_progress + uniform(0.0, 10.0)
        progress = min(progress, 100.0)
        
        fabrication_slots_m.update(slot.id, fabrication_progress=progress)
    
    #slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    #if error:
    #    return error

    return SimpleOKResponse()

@tick_api_bp.route("/arrival", methods=["GET"])
@auth_m.permission_required("tick_show")
def tick_arrival():
    """Obtiene porcentaje de progreso."""
    
    number = round(uniform(0.7, 10.0), 2)
    #slot, error = api_validate_id(fabrication_slots_m, request.args, tuple_name="El slot")

    #if error:
    #    return error

    return SimpleOKResponse(number=number)