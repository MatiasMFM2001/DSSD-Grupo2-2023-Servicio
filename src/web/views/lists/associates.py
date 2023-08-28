from flask import url_for
from src.web.templates import super_templates
from src.web.helpers.controller_helpers import generate_url


def list_associate(surname, state, page, request_args):
    return super_templates.render_list_view(
        title="Listado de asociados"
        + (" activos" if state == "True" else " inactivos" if state == "False" else "")
        + (" con apellido similar a " + surname if surname else ""),
        columns=[
            super_templates.Column("Nombre", "first_name"),
            super_templates.Column("Apellido", "last_name"),
            super_templates.Column("Email", "email"),
            super_templates.Column(
                "Estado",
                "active",
                value_to_string=lambda b: "Activo" if b else "Inactivo",
            ),
        ],
        filter_global_buttons=[
            super_templates.Button(
                "Activo",
                url=generate_url(
                    url_for("privada.socios.associates_list"), request_args, estado=True
                ),
            ),
            super_templates.Button(
                "Inactivo",
                url=generate_url(
                    url_for("privada.socios.associates_list"),
                    request_args,
                    estado=False,
                ),
            ),
            super_templates.Button(
                "Ambos",
                url=generate_url(
                    url_for("privada.socios.associates_list"), request_args, estado=""
                ),
            ),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Agregar asociado",
                url=url_for("privada.socios.register_associates"),
                permission="associate_create",
                btn_class="btn btn-outline-secondary",
            )
        ],
        other_global_buttons=[
            super_templates.Button(
                "Exportar a CSV",
                url=url_for("privada.socios.download_csv", **request_args),
                permission="associate_export",
                btn_class="bg-outline-success",
            ),
            super_templates.Button(
                "Exportar a PDF",
                url=url_for("privada.socios.download_pdf", **request_args),
                permission="associate_export",
                btn_class="btn btn-danger",
            ),
        ],
        row_buttons=[
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Editar",
                    url=generate_url("/socios/editar", id=associate.id, **request_args),
                    permission="associate_update",
                    btn_class="btn btn-outline-primary",
                )
            ),
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Ver Disciplinas",
                    url=generate_url(
                        "/socios/listado/mis_disciplinas",
                        request_args,
                        id=associate.id,
                        page=1,
                    ),
                    permission="associate_unscribe_discipline",
                    btn_class="btn btn-outline-info",
                )
            ),
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Asociar",
                    url=generate_url("/socios/listado/asociar", id=associate.id),
                    permission="associate_inscribe_discipline",
                    btn_class="btn btn-outline-primary",
                )
            ),
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Ver Carnet",
                    url=generate_url("/socios/listado/carnet", id=associate.id),
                    permission="associate_export",
                    btn_class="btn btn-outline-success",
                )
            ),
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Listar Cuotas",
                    url=generate_url(
                        "/socios/pagos/listado",
                        request_args,
                        associate_id=associate.id,
                        page=1,
                    ),
                    permission="payment_list",
                    btn_class="btn btn-outline-secondary",
                )
            ),
            super_templates.CustomButton(
                lambda associate: super_templates.Button(
                    "Eliminar",
                    url=generate_url(
                        "/socios/listado/eliminar", id=associate.id, **request_args
                    ),
                    permission="associate_destroy",
                    btn_class="btn btn-outline-danger",
                )
            ),
        ],
        paginator=page,
        searchbar=[True, "Buscar por apellido", "apellido"],
    )


def list_associate_disciplines(associate, page, request_args):
    def return_unsuscribe_button(discipline):
        """Devuelve el botón de desuscribir de disciplina asociado a id.
        Returns:
            Button: boton con caracteristicas mencionadas.
        """
        return super_templates.Button(
            "Desasociar",
            url=generate_url(
                "/socios/listado/mis_disciplinas/desasociar",
                discipline_id=discipline.id,
                associate_id=associate.id,
            ),
            permission="associate_unscribe_discipline",
            btn_class="btn btn-outline-danger",
        )

    return super_templates.render_list_view(
        title=f"Listado de disciplinas de {associate.first_name} {associate.last_name}",
        columns=[
            super_templates.Column("Nombre", object_to_value=lambda d: d.name),
            super_templates.Column(
                "Categoria",
                "categories",
                value_to_string=lambda l: ", ".join([c.name for c in l]),
            ),
            super_templates.Column("Instructores", object_to_value=lambda d: d.teacher),
            super_templates.Column(
                "Dias y horarios", object_to_value=lambda d: d.schedule_time
            ),
        ],
        row_buttons=[
            super_templates.CustomButton(return_unsuscribe_button),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Asociar",
                url=generate_url("/socios/listado/asociar", id=associate.id),
                btn_class="btn btn-outline-primary",
            ),
            super_templates.Button(
                "Volver", url="/socios/listado", btn_class="btn btn-outline-primary"
            ),
        ],
        paginator=page,
    )


def list_associate_disciplines_to_inscribe(associate, page, request_args):
    def return_inscribe_button(discipline):
        """Devuelve el botón de inscribir de disciplina asociado a id.
        Returns:
            Button: boton con caracteristicas mencionadas.
        """
        return super_templates.Button(
            "Asociar",
            url=generate_url(
                "/socios/listado/asociar/disciplina",
                discipline_id=discipline.id,
                associate_id=associate.id,
            ),
            permission="associate_inscribe_discipline",
            btn_class="btn btn-outline-primary",
        )

    return super_templates.render_list_view(
        title=f"Listado de disciplinas disponibles para el {associate.first_name} {associate.last_name}",
        columns=[
            super_templates.Column("Nombre", object_to_value=lambda d: d.name),
            super_templates.Column(
                "Categoria",
                "categories",
                value_to_string=lambda l: ", ".join([c.name for c in l]),
            ),
            super_templates.Column("Instructores", object_to_value=lambda d: d.teacher),
            super_templates.Column(
                "Dias y horarios", object_to_value=lambda d: d.schedule_time
            ),
        ],
        row_buttons=[
            super_templates.CustomButton(return_inscribe_button),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Volver", url="/socios/listado", btn_class="btn btn-outline-primary"
            ),
        ],
        paginator=page,
    )
