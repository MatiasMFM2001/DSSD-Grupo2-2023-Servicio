from flask import Blueprint

from src.api.blueprints.auth_api_bp import auth_api_bp
from src.api.blueprints.material_api_bp import material_api_bp
from src.api.blueprints.fabrication_slot_api_bp import fabrication_slot_api_bp
from src.api.blueprints.material_requests_api_bp import material_requests_api_bp
from src.api.blueprints.material_supplier_api_bp import material_supplier_api_bp
from src.api.blueprints.tick_api_bp import tick_api_bp

root_api_bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in [
    auth_api_bp,
    material_api_bp,
    fabrication_slot_api_bp,
    material_requests_api_bp,
    material_supplier_api_bp,
    tick_api_bp,
]:
    root_api_bp.register_blueprint(blueprint)












