from flask import Blueprint, render_template, redirect, url_for
from src.web.templates import super_templates

from src.web.blueprints.associates_bp import associates_bp
from src.web.blueprints.disciplines_bp import disciplines_bp
from src.web.blueprints.sysconfig_bp import sysconfig_bp
from src.web.blueprints.users_bp import users_bp
from src.web.blueprints.auth_bp import auth_bp
from src.core.business.user_manager import auth_m
from src.api.root_api_bp import root_api_bp
from src.web.blueprints.graphics_bp import graphics_bp

root_bp = Blueprint(
    "privada", __name__, url_prefix="/", template_folder="templates/private/"
)

for blueprint in [
    auth_bp,
    associates_bp,
    disciplines_bp,
    sysconfig_bp,
    users_bp,
    graphics_bp,
    root_api_bp,
]:
    root_bp.register_blueprint(blueprint)


@root_bp.route("/inicio")
def home():
    """Muestra la página de inicio.

    Returns:
        str: página de inicio renderizada.
    """
    return render_template(
        "/index.html",
        user=auth_m.current_user(),
        get_roles=lambda user: [role.name for role in user.roles],
    )


@root_bp.route("/")
def home_redirect():
    """Redirecciona a la página de inicio.

    Returns:
        Response: redirecciona a la página de inicio.
    """
    return redirect(url_for("privada.home"))
