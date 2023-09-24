from flask import Blueprint

from src.api.blueprints.auth_api_bp import auth_api_bp
from api.blueprints.user_api_bp import associates_api_bp
from src.api.blueprints.club_api_bp import club_api_bp

root_api_bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in [
    auth_api_bp,
    associates_api_bp,
    club_api_bp,
]:
    root_api_bp.register_blueprint(blueprint)












