from flask import (
    Blueprint,
    url_for,
    request,
    abort,
    redirect,
    flash,
    url_for,
    send_file,
)
from src.web.templates import super_templates
from src.core.business.cuote_manager import CuoteManager
from src.core.database.board.cuote import CuoteState
from src.core.business.associate_manager import AssociateManager
from datetime import date
from src.web.helpers.controller_helpers import PDFResponse, generate_url, validate_id
from src.core.business.exporters.exporter_pdf import export_receipt
from src.web.templates.super_templates import Column
from src.core.business.user_manager import auth_m
from src.web.views.forms.payments import *
from src.web.views.lists.payments import *


payments_bp = Blueprint("pagos", __name__, url_prefix="/pagos")

cuote_m = CuoteManager()
associate_m = AssociateManager()


@payments_bp.route("/filtros", methods=["GET", "POST"])
@auth_m.permission_required("payment_list")
def filter_list():
    """Muestra el formulario de filtros para la lista de pagos.

    Returns:
        str: formulario de filtros renderizado.
    """
    surname = request.args.get("surname")
    associate_id = request.args.get("associate_id")
    form = FormPaymentSearch(surname, associate_id)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores del formulario.

        Returns:
            Response: redirección a la lista de pagos.
        """
        return redirect(url_for("privada.socios.pagos.cuotes_list", **values))

    return super_templates.render_form_view(
        title="Filtrar cuotas", form=form, on_success_with_data=on_success_with_data
    )


@payments_bp.route("/listado")
@auth_m.permission_required("payment_list")
def cuotes_list():
    """Muestra la lista de cuotas.

    Returns:
        str: lista de cuotas renderizada.
    """
    surname = request.args.get("surname", "")
    associate_id = request.args.get("associate_id", "")
    page_num = request.args.get("page", 1)

    try:
        page_num = int(page_num)
    except ValueError:
        abort(400)

    if surname and associate_id:
        abort(422)

    title = "Listado de cuotas"
    page = cuote_m.filter_by_get_paginator(page_num, True)
    button_url = generate_url("/socios/pagos/filtros", **request.args)

    if surname:
        title += f" de socios con apellido '{surname}'"
        page = cuote_m.filter_surname_get_paginator(associate_m, surname, page_num)

    if associate_id:
        title += f" del socio #{associate_id}"
        page = cuote_m.filter_id_get_paginator(associate_m, associate_id, page_num)

    return list_payments(page, request.args, title, button_url)


@payments_bp.route("/registrar", methods=["GET", "POST"])
@auth_m.permission_required("payment_update")
def register_payment():
    """Muestra el formulario para registrar un pago.

    Returns:
        str: formulario para registrar un pago renderizado.
    """
    cuote = cuote_m.validate_and_get(request.args, False)
    today = date.today()
    late_fee_amount = cuote_m.get_late_fee(cuote, today)
    form = FormConfirm(cuote, today, late_fee_amount)

    def on_success(form):
        """Acción a realizar cuando el formulario es válido.

        Args:
            form (Form): formulario.

        Returns:
            Response: redirección a la lista de pagos.
        """
        cuote_m.register_payment(cuote)
        flash(f"Cuota #{cuote.id} pagada correctamente", "success")

        surname = request.args.get("surname")
        associate_id = request.args.get("associate_id")

        return redirect(
            url_for(
                "privada.socios.pagos.cuotes_list",
                surname=surname,
                associate_id=associate_id,
            )
        )

    return super_templates.render_form_view(
        title=f"¿Desea confirmar el pago de la cuota #{cuote.id}?",
        form=form,
        on_success=on_success,
        read_only=True,
        submit_display_name="Confirmar",
    )


@payments_bp.route("/descargar-pdf")
@auth_m.permission_required("payment_export")
def download_pdf():
    """Descarga el comprobante de pago de una cuota.

    Returns:
        Response: comprobante de pago de la cuota.
    """
    cuote = cuote_m.validate_and_get(request.args, True)
    pdf_bytes = export_receipt(cuote)
    return PDFResponse(pdf_bytes, "Recibo", True)


@payments_bp.route("/generar-cuotas")
@auth_m.permission_required("payment_create")
def generate_cuotes():
    """Genera las cuotas del mes.

    Returns:
        Response: refresca la página.
    """
    created_count = cuote_m.generate_cuotes_new_month()

    if created_count:
        flash(f"{created_count} cuotas generadas correctamente", "success")
    else:
        flash(f"Todas las cuotas del mes ya habían sido creadas", "warning")

    return redirect(request.referrer)


@payments_bp.route("/eliminar")
@auth_m.permission_required("payment_destroy")
def delete():
    """Eliminación de pago.

    Returns:
        Response: listado con flash.
    """
    cuote = validate_id(cuote_m, request.args)
    cuote_m.remove(cuote.id)

    flash(f"La cuota ha sido removida correctamente", "success")
    return redirect(request.referrer)


@payments_bp.route("/restaurar")
@auth_m.permission_required("payment_destroy")
def restore():
    """Restauración de pago.

    Returns:
        Response: listado con flash.
    """
    cuote = validate_id(cuote_m, request.args, True)
    cuote_m.update(cuote.id, True, active=True)

    flash(f"La cuota ha sido restaurada correctamente", "success")
    return redirect(request.referrer)


@payments_bp.route("/comprobante")
@auth_m.permission_required("payment_export")
def download_image():
    """Descarga el comprobante que ingresó el socio para una cuota.

    Returns:
        Response: comprobante de pago de la cuota.
    """
    cuote = validate_id(cuote_m, request.args, True)

    if not cuote.file_extension:
        abort(400)

    return send_file(cuote.absolute_path())
