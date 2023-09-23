from flask import Blueprint, request
from datetime import date

from src.core.business.user_manager import UserManager, auth_m

from src.api.helpers import to_json, paginator_to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.api.helpers.api_requests import get_json

associates_api_bp = Blueprint("associates_api_bp", __name__, url_prefix="/me")

user_m = UserManager()

@associates_api_bp.route("/profile", methods=["GET"])
@auth_m.login_required(True)
def associate_profile(associate):
    """Obtiene información del perfil del asociado."""
    return SimpleOKResponse(associate=associate.get_json())