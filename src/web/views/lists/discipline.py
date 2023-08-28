from flask import url_for
from src.web.templates import super_templates
from src.web.helpers.controller_helpers import generate_url


def list_disciplines(page, request_args):
    def return_edit_button(user):
        return super_templates.Button(
            "Editar",
            url=generate_url("/disciplinas/listado/editar", id=user.id),
            permission="discipline_update",
            btn_class="btn btn-outline-primary",
        )

    def return_delete_button(user):
        return super_templates.Button(
            "Eliminar",
            url=generate_url("/disciplinas/listado/eliminar", id=user.id),
            permission="discipline_destroy",
            btn_class="btn btn-outline-danger",
        )

    return super_templates.render_list_view(
        title="Listado de disciplinas"
        + (
            " habilitadas"
            if request_args.get("estado") == "True"
            else " deshabilitadas"
            if request_args.get("estado") == "False"
            else ""
        )
        + (
            " con nombre similar a " + request_args.get("nombre")
            if request_args.get("nombre")
            else ""
        ),
        columns=[
            super_templates.Column("Nombre", "name"),
            super_templates.Column(
                "Categoria",
                "categories",
                value_to_string=lambda l: ", ".join([c.name for c in l]),
            ),
            super_templates.Column("Instructores", "teacher"),
            super_templates.Column("Dias y horarios", "schedule_time"),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Agregar disciplina",
                url="/disciplinas/alta",
                permission="discipline_create",
                btn_class="btn btn-outline-secondary",
            )
        ],
        row_buttons=[
            super_templates.CustomButton(return_edit_button),
            super_templates.CustomButton(return_delete_button),
        ],
        filter_global_buttons=[
            super_templates.Button(
                "Habilitada",
                url=generate_url(
                    url_for("privada.disciplinas.list"), request_args, estado=True
                ),
                value="True",
            ),
            super_templates.Button(
                "Deshabilitada",
                url=generate_url(
                    url_for("privada.disciplinas.list"), request_args, estado=False
                ),
                value="False",
            ),
            super_templates.Button(
                "Ambos",
                url=generate_url(
                    url_for("privada.disciplinas.list"), request_args, estado=""
                ),
                value="",
            ),
        ],
        paginator=page,
        actual_page="disciplines",
        searchbar=[True, "Buscar por nombre de disciplina", "nombre"],
    )
