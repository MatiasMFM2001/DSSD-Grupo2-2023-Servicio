from flask import url_for
from src.core.database.board.cuote import CuoteState
from src.web.helpers.controller_helpers import generate_url
from src.web.helpers.view_helpers import format_date
from src.web.templates import super_templates


def list_payments(page, request_args, title, button_url):
    def main_button(cuote):
        """Genera un botón para la cuota.

        Args:
            cuote (Cuote): cuota a la que se le genera el botón.

        Returns:
            Button: botón para la cuota.
        """

        if cuote.state == CuoteState.PAID:
            return super_templates.Button(
                "Generar PDF",
                url=generate_url(
                    "/socios/pagos/descargar-pdf", id=cuote.id, **request_args
                ),
                permission="payment_export",
                visible=cuote.active,
                btn_class="btn btn-outline-success",
            )

        if cuote.state == CuoteState.PENDING:
            return super_templates.Button(
                "Registrar pago",
                url=generate_url(
                    "/socios/pagos/registrar", id=cuote.id, **request_args
                ),
                permission="payment_update",
                visible=cuote.active,
                btn_class="btn btn-outline-primary",
            )

        return super_templates.Button("", visible=False)

    def receipt_button(cuote):
        return super_templates.Button(
            "Ver comprobante",
            url=generate_url("/socios/pagos/comprobante", id=cuote.id, **request_args),
            permission="payment_export",
            visible=(cuote.active and cuote.file_extension),
            btn_class="btn btn-outline-secondary",
        )

    def delete_button(cuote):
        if cuote.active:
            return super_templates.Button(
                "Eliminar",
                url=generate_url("/socios/pagos/eliminar", id=cuote.id, **request_args),
                permission="payment_destroy",
                btn_class="btn btn-outline-danger",
            )

        return super_templates.Button(
            "Restaurar",
            url=generate_url("/socios/pagos/restaurar", id=cuote.id, **request_args),
            permission="payment_destroy",
            btn_class="btn btn-outline-secondary",
        )

    return super_templates.render_list_view(
        title=title,
        columns=[
            super_templates.Column(
                "Nº socio", object_to_value=lambda c: c.associate.id
            ),
            super_templates.Column(
                "Nombre", object_to_value=lambda c: c.associate.first_name
            ),
            super_templates.Column(
                "Apellido", object_to_value=lambda c: c.associate.last_name
            ),
            super_templates.Column("Servicio", object_to_value=lambda c: c.service),
            super_templates.Column(
                "Fecha",
                object_to_value=lambda c: c.expiration_date,
                value_to_string=lambda d: format_date(d, "%B %Y"),
            ),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Buscar / Filtrar", url=button_url, btn_class="btn btn-outline-primary"
            ),
            super_templates.Button(
                "Generar cuotas del mes",
                url="/socios/pagos/generar-cuotas",
                permission="payment_create",
                btn_class="btn btn-outline-secondary",
            ),
        ],
        row_buttons=[
            super_templates.CustomButton(main_button),
            super_templates.CustomButton(receipt_button),
            super_templates.CustomButton(delete_button),
        ],
        paginator=page,
        paginator_url=url_for("privada.socios.pagos.cuotes_list"),
    )
