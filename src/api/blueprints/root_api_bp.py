from flask import Blueprint

from src.api.blueprints.auth_api_bp import auth_api_bp
from src.api.blueprints.user_api_bp import user_api_bp
from src.api.blueprints.material_api_bp import material_api_bp
from src.api.blueprints.slot_api_bp import slot_api_bp

root_api_bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in [
    auth_api_bp,
    user_api_bp,
    material_api_bp,
    slot_api_bp,
]:
    root_api_bp.register_blueprint(blueprint)












