from flask import Blueprint, request
from src.core.business.associate_manager import auth_m
from src.api.responses import SimpleOKResponse, SimpleErrorResponse
from src.api.auth.jwt import encode
from src.api import requests

auth_bp = Blueprint("autenticación", __name__, url_prefix="")


@auth_bp.route("/login/", methods=["POST"])
def login():
    values, error = requests.get_json({"user", "password"})

    if error:
        return error

    associate = auth_m.login(values["user"], values["password"])

    if associate is None:
        return SimpleErrorResponse(401, "Credenciales inválidas")

    token = auth_m.token_of(associate)
    return SimpleOKResponse("La sesión ha sido iniciada correctamente", token=token)


@auth_bp.route("/me/editar_perfil", methods=["POST"])
@auth_m.login_required(True)
def profile(associate):
    values, error = requests.get_json({"new_pass"})

    if error:
        return error

    new_pass = values["new_pass"]

    auth_m.update(associate.id, password=new_pass)
    return SimpleOKResponse("Tu contraseña ha sido actualizada correctamente")
