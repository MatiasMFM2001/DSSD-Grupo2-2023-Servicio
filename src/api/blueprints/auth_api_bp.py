from flask import Blueprint, request
from src.core.business.user_manager import auth_m
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.api.helpers.jwt_helpers import encode
from src.api.helpers.api_requests import get_json

auth_api_bp = Blueprint("autenticación", __name__, url_prefix="")


@auth_api_bp.route("/login/", methods=["POST"])
@auth_m.permission_required("private_login", login_required=False)
def login():
    values, error = get_json({"user", "password"})

    if error:
        return error

    associate = auth_m.login(values["user"], values["password"])

    if associate is None:
        return SimpleErrorResponse(401, "Credenciales inválidas")

    token = auth_m.token_of(associate)
    return SimpleOKResponse("La sesión ha sido iniciada correctamente", token=token)


@auth_api_bp.route("/me/editar_perfil", methods=["POST"])
@auth_m.permission_required("private_profile_edit", call_with_current_user=True)
def profile(associate):
    values, error = get_json({"new_pass"})

    if error:
        return error

    new_pass = values["new_pass"]

    auth_m.update(associate.id, password=new_pass)
    return SimpleOKResponse("Tu contraseña ha sido actualizada correctamente")
