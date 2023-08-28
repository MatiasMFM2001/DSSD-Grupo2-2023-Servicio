import os
import csv
from src.web.views.forms.associate import *
from src.web.views.lists.associates import *
from io import StringIO
from flask import Blueprint, redirect, request, flash, render_template, current_app
from src.web.templates import super_templates
from src.web.helpers.controller_helpers import (
    PDFResponse,
    CSVResponse,
    validate_id,
    allowed_file,
    validate_file,
)
from src.core.business.associate_manager import AssociateManager
from src.core.business.exporters.exporter_pdf import export_list, export_card
from src.web.templates.super_templates import Column
from src.core.business.user_manager import auth_m
from src.web.blueprints.payments_bp import payments_bp
import qrcode


associates_bp = Blueprint("socios", __name__, url_prefix="/socios")

associates_bp.register_blueprint(payments_bp)
associates_m = AssociateManager()


@associates_bp.route("/alta", methods=["GET", "POST"])
@auth_m.permission_required("associate_create")
def register_associates():
    """Muestra el formulario de alta de socio.

    Returns:
        str: formulario de alta de socio renderizado.
    """
    form = CreateAssociate()

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores de formulario de alta de socio.

        Returns:
            Response: pagina a redireccionar.
        """
        try:
            del values["image"]
            allowed_mimes = {"image/bmp", "image/jpeg", "image/png"}

            def error_raiser(http_code, message):
                raise TypeError("El archivo no es una imagen")

            buffer, file_mime = validate_file(
                request.files, "image", allowed_mimes, error_raiser
            )

            file_extension = file_mime[(file_mime.find("/") + 1) :]
            associate = associates_m.create(file_extension=file_extension, **values)

            with open(associate.relative_path(file_extension), "wb") as out_file:
                out_file.write(buffer.getbuffer())

            flash(
                f"El usuario {values['first_name']} {values['last_name']} ha sido creado correctamente",
                "success",
            )

            return redirect("/socios/listado")
        except (ValueError, TypeError) as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Alta de asociado",
        form=form,
        on_success_with_data=on_success_with_data,
        cancel_button_url="/socios/listado",
    )


@associates_bp.route("/listado")
@auth_m.permission_required("associate_list")
def associates_list():
    """Muestra el listado de socios.

    Returns:
        str: pagina renderizada.
    """

    surname = request.args.get("apellido")
    state = request.args.get("estado")
    page_num = request.args.get("page", "1")
    page = associates_m.filter_like_get_paginator(surname, state, page_num)
    request_args = request.args
    return list_associate(surname, state, page, request_args)


@associates_bp.route("/listado/carnet")
@auth_m.permission_required("associate_export")
def view_card():
    """Muestra el carnet del socio.

    Returns:
        str: pagina renderizada.
    """
    associate = validate_id(associates_m, request.args, True)
    qr = qrcode.make(
        f"{current_app.config['BACKEND_URI']}/socios/listado/carnet?id={associate.id}"
    )
    qr.save(f"public/images/qr{associate.id}.png")
    card_bytes = export_card(
        associate=associate,
        state="Moroso" if associates_m.is_defaulter(associate.id) else "Al día",
    )
    return render_template(
        "card.html",
        title="Carnet de socio",
        associate=associate,
        state="Moroso" if associates_m.is_defaulter(associate.id) else "Al día",
        back_button_url="/socios/listado",
    )


@associates_bp.route("/listado/carnet/descargar")
@auth_m.permission_required("associate_export")
def download_card():
    """Descarga el listado de socios en formato PDF.

    Returns:
        Response: respuesta con el archivo PDF.
    """

    associate = validate_id(associates_m, request.args, True)

    pdf_bytes = export_card(
        associate=associate,
        state="Moroso" if associates_m.is_defaulter(associate.id) else "Al día",
    )

    return PDFResponse(
        pdf_bytes, f"{associate.first_name}_{associate.last_name}_Carnet", True
    )


@associates_bp.route("/listado/descargar-pdf")
@auth_m.permission_required("associate_export")
def download_pdf():
    """Descarga el listado de socios en formato PDF.

    Returns:
        Response: respuesta con el archivo PDF.
    """
    pdf_bytes = export_list(
        columns=[
            Column("Nombre", "first_name"),
            Column("Apellido", "last_name"),
            Column("Número de socio", "id"),
            Column(
                "Estado",
                "active",
                value_to_string=lambda b: "Activo" if b else "Bloqueado",
            ),
        ],
        items=associates_m.filter_like_get_list(
            request.args.get("apellido"), request.args.get("estado")
        ),
    )

    return PDFResponse(pdf_bytes, "Listado", True)


@associates_bp.route("/listado/descargar-csv")
@auth_m.permission_required("associate_export")
def download_csv():
    """Descarga el listado de socios en formato CSV.

    Returns:
        Response: respuesta con el archivo CSV.
    """
    with StringIO() as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Nombre",
                "Apellido",
                "Tipo De Documento",
                "Numero",
                "Genero",
                "Numero de Socio/a",
                "Direccion",
                "Email",
                "Estado",
                "Telefono",
                "Fecha de Alta",
            ]
        )
        for associate in associates_m.filter_like_get_list(
            request.args.get("apellido"), request.args.get("estado")
        ):
            writer.writerow(
                [
                    associate.first_name,
                    associate.last_name,
                    associate.doc_type,
                    associate.doc_number,
                    associate.genre,
                    associate.id,
                    associate.email,
                    "Activo" if associate.active else "Inactivo",
                    associate.phone_number,
                    associate.created_at,
                ]
            )
        csv_bytes = bytes(f.getvalue(), "utf-8")
    return CSVResponse(csv_bytes, "Listado", True)


@associates_bp.route("/editar", methods=["GET", "POST"])
@auth_m.permission_required("associate_update")
def form_edit():
    """Muestra el formulario de edición de socio.

    Returns:
        str: formulario de edición de socio renderizado.
    """
    associate = validate_id(associates_m, request.args, True)
    form = EditAssociate(associate)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores de formulario de edición de socio.

        Returns:
            Resposnse: pagina a redireccionar.
        """
        try:
            if values["image"] is not None:
                del values["image"]
                allowed_mimes = {"image/bmp", "image/jpeg", "image/png"}

                def error_raiser(http_code, message):
                    raise TypeError("El archivo no es una imagen")

                buffer, file_mime = validate_file(
                    request.files, "image", allowed_mimes, error_raiser
                )

                file_extension = file_mime[(file_mime.find("/") + 1) :]

                with open(associate.relative_path(file_extension), "wb") as out_file:
                    out_file.write(buffer.getbuffer())

                associates_m.update(associate.id, file_extension=file_extension)

            associates_m.update(id=associate.id, include_inactives=True, **values)

            flash(
                f"El usuario {values['first_name']} {values['last_name']} ha sido actualizado correctamente",
                "success",
            )

            return redirect("/socios/listado")
        except (ValueError, TypeError) as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Editar Asociado",
        form=form,
        on_success_with_data=on_success_with_data,
        cancel_button_url="/socios/listado",
    )


@associates_bp.route("/listado/eliminar", methods=["GET", "POST"])
@auth_m.permission_required("associate_destroy")
def delete():
    """Eliminación de socio.

    Returns:
        Response: listado con flash.
    """
    associate = validate_id(associates_m, request.args, True)
    try:
        associates_m.remove(associate.id)
        flash(
            f"El socio {associate.first_name} {associate.last_name} ha sido puesto en inactivo correctamente",
            "success",
        )
    except Exception as e:
        flash(str(e), "danger")
    finally:
        return redirect(request.referrer)


@associates_bp.route("/listado/mis_disciplinas")
@auth_m.permission_required("associate_unscribe_discipline")
def list_disciplines():
    """Muestra el listado de disciplinas del asociado.

    Returns:
        str: pagina renderizada.
    """
    associate = validate_id(associates_m, request.args, True)
    page = associates_m.filter_id_get_paginator(
        request.args.get("id"), request.args.get("page", "1")
    )
    return list_associate_disciplines(associate, page, request.args)


@associates_bp.route("/listado/mis_disciplinas/desasociar", methods=["GET", "POST"])
@auth_m.permission_required("associate_unscribe_discipline")
def unsuscribe():
    """Desuscribe al asociado de la disciplina.

    Returns:
        Response: pagina renderizada de listado disciplinas con flash de success/error.
    """
    associate = validate_id(associates_m, request.args, key="associate_id")
    discipline = validate_id(
        associates_m.discipline_m, request.args, key="discipline_id"
    )
    try:
        associates_m.unsubscribe_from_discipline(associate, discipline)
        flash(
            f"El socio {associate.first_name} {associate.last_name} ha sido desasociado de la disciplina {discipline.name} correctamente",
            "success",
        )
    except Exception as e:
        flash(str(e), "danger")
    finally:
        return redirect(request.referrer)


@associates_bp.route("/listado/asociar/", methods=["GET", "POST"])
@auth_m.permission_required("associate_inscribe_discipline")
def list_associate_to_new_discipline():
    """Muestra el listado de disciplinas disponibles para asociar.

    Returns:
        str: pagina renderizada.
    """
    associate = validate_id(associates_m, request.args, True)
    page = associates_m.get_paginator_except_inscribed(
        request.args.get("id"), request.args.get("page", "1")
    )
    return list_associate_disciplines_to_inscribe(associate, page, request.args)


@associates_bp.route("/listado/asociar/disciplina", methods=["GET", "POST"])
@auth_m.permission_required("associate_inscribe_discipline")
def inscribe():
    """Inscribe al asociado de la disciplina.

    Returns:
        Response: pagina renderizada de listado disciplinas con flash de success/error.
    """
    associate = validate_id(associates_m, request.args, key="associate_id")
    discipline = validate_id(
        associates_m.discipline_m, request.args, key="discipline_id"
    )
    try:
        associates_m.inscribe_to_discipline(associate, discipline)
        flash(
            f"El socio {associate.first_name} {associate.last_name} ha sido asociado a la disciplina {discipline.name} correctamente",
            "success",
        )
    except Exception as e:
        flash(str(e), "danger")
    finally:
        return redirect(request.referrer)
