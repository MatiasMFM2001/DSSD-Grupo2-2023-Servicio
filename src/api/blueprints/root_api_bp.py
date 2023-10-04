from flask import Blueprint

from src.api.blueprints.auth_api_bp import auth_api_bp
from src.api.blueprints.user_api_bp import user_api_bp
from src.api.blueprints.category_api_bp import category_api_bp
from src.api.blueprints.collection_api_bp import collection_api_bp
from src.api.blueprints.furniture_api_bp import furniture_api_bp

root_api_bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in [
    auth_api_bp,
    user_api_bp,
    category_api_bp,
    collection_api_bp,
    furniture_api_bp,
]:
    root_api_bp.register_blueprint(blueprint)












