from datetime import date
from flask import Blueprint, request, abort, jsonify
from werkzeug.exceptions import HTTPException
from src.core.business.service_manager import DisciplineManager
from src.core.business.cuote_manager import CuoteManager
from src.core.business.associate_manager import AssociateManager, auth_m
from src.core.business.config_manager import ConfigManager
from src.web.helpers.controller_helpers import (
    api_validate_id,
    get_int,
    api_validate_file,
)
from io import BytesIO
import re, magic
from src.api import requests
from src.api.responses import SimpleOKResponse, SimpleErrorResponse
from src.api.auth import jwt
from src.api.auth.auth_bp import auth_bp

api_disciplines_bp = Blueprint("api_disciplines_bp", __name__, url_prefix="/api")
api_cuotes_bp = Blueprint("api_cuotes_bp", __name__, url_prefix="/api")
api_info_bp = Blueprint("api_info_bp", __name__, url_prefix="/api")

api_disciplines_bp.register_blueprint(auth_bp)

disciplines_m = DisciplineManager()
cuote_m = CuoteManager()
associate_m = AssociateManager()
config_m = ConfigManager()


def to_json(rows):
    """Convierte los datos de una lista o consulta a JSON."""
    return [row.get_json() for row in rows]


def paginator_to_json(paginator):
    """Convierte una página y sus items a JSON."""
    return dict(
        has_next=paginator.has_next,
        has_prev=paginator.has_prev,
        items=to_json(paginator.items),
        next_num=paginator.next_num,
        page=paginator.page,
        pages=paginator.pages,
        per_page=paginator.per_page,
        prev_num=paginator.prev_num,
        total=paginator.total,
    )


@api_disciplines_bp.route("/club/disciplines", methods=["GET"])
def disciplines_of_club():
    """Obtiene todas las disciplinas que se realizan en el club."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        disciplines = paginator_to_json(
            disciplines_m.filter_by_get_paginator(page_number)
        )
        return SimpleOKResponse(disciplines=disciplines)
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")


@api_disciplines_bp.route("/me/disciplines", methods=["GET"])
@auth_m.login_required(True)
def disciplines_of_user(associate):
    """Obtiene la lista de las disciplinas a las que está inscripto el usuario."""

    disciplines = to_json(associate_m.get_disciplines_of_associate(associate.id))
    return SimpleOKResponse(disciplines=disciplines)


@api_cuotes_bp.route("/me/payments", methods=["GET"])
@auth_m.login_required(True)
def associate_cuotes_list(associate):
    """Obtiene la lista de cuotas pagadas, pendientes o impagas del asociado."""

    page_number, error = get_int(request.args, "page", SimpleErrorResponse, "página")

    if error:
        return error

    try:
        paginator = cuote_m.get_associate_cuotes(associate.id, page_number)
        return SimpleOKResponse(paginator=paginator_to_json(paginator))
    except HTTPException:
        return SimpleErrorResponse(404, f"La página {page_number} no existe")


@api_cuotes_bp.route("/me/defaulter", methods=["GET"])
@auth_m.login_required(True)
def associate_is_defaulter(associate):
    """Retorna TRUE si el socio es moroso."""

    return SimpleOKResponse(is_defaulter=cuote_m.is_defaulter(associate.id))


@api_cuotes_bp.route("/me/payments", methods=["POST"])
@auth_m.login_required(True)
def associate_register_receipt(associate):
    """Registra un nuevo pago para el usuario."""

    cuote, error = api_validate_id(cuote_m, request.args, tuple_name="La cuota")

    if error:
        return error

    if cuote.associate_id != associate.id:
        return SimpleErrorResponse(
            401,
            f"La cuota de ID {cuote.id} no pertenece al socio {associate.full_name}",
        )

    if cuote.paid_date:
        return SimpleErrorResponse(400, f"La cuota de ID {cuote.id} ya fue pagada")

    allowed_mimes = {"image/bmp", "image/jpeg", "image/png"}

    buffer, file_mime, error = api_validate_file(
        request.files, "receipt", allowed_mimes
    )

    if error:
        return error

    file_extension = file_mime[(file_mime.find("/") + 1) :]

    with open(cuote.relative_path(file_extension), "wb") as out_file:
        out_file.write(buffer.getbuffer())

    cuote_m.update(cuote.id, file_extension=file_extension)
    return SimpleOKResponse(cuote=cuote.get_json())


@api_cuotes_bp.route("/me/license", methods=["POST"])
@auth_m.login_required(True)
def associate_license(associate):
    """Obtiene información necesaria para renderizar el carnet en el Front-End."""

    description = (
        "El socio no registra deuda ni sanción."
        if associate_m.is_defaulter(associate.id)
        else "El socio es moroso"
    )
    return SimpleOKResponse(description=description, profile=associate.get_json())


@api_info_bp.route("/club/info", methods=["GET"])
def club_info():
    """Obtiene información importante y de contacto sobre el club."""

    return SimpleOKResponse(
        email=config_m.get_field("club_email"), phone=config_m.get_field("phone_number")
    )


@api_info_bp.route("me/profile", methods=["GET"])
@auth_m.login_required(True)
def associate_profile(associate):
    """Obtiene información del perfil del asociado."""
    return SimpleOKResponse(associate=associate.get_json())


@api_info_bp.route("me/cuote_detail", methods=["POST"])
@auth_m.login_required(True)
def cuote_detail(associate):
    """Obtiene información de de la cuota del mes del socio."""
    dato, error = requests.get_json({"month", "year"})

    if error:
        return error

    mes, error = get_int(dato, "month", SimpleErrorResponse, "mes")

    if error:
        return error

    año, error = get_int(dato, "year", SimpleErrorResponse, "año")

    if error:
        return error

    if not mes in range(1, 13):
        return SimpleErrorResponse(400, f"El mes {mes} no es válido")

    if año > date.today().year:
        return SimpleErrorResponse(400, f"El año {año} no es válido")

    consulta = cuote_m.cuote_detail_month(associate.id, date(año, mes, 10))

    dict = [row.get_detail() for row in consulta]
    return SimpleOKResponse(cuote_detail=dict)
