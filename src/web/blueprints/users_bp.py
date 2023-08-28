from xmlrpc.client import Boolean
from flask import Blueprint, url_for, redirect, request, flash
from src.web.templates import super_templates
from src.web.views.forms.user import *
from src.core.business.user_manager import UserManager
from src.web.helpers.controller_helpers import generate_url, validate_id
from src.core.database.auth.role import Role
from src.core.business.user_manager import auth_m

user_m = UserManager()
role_rm = Role.resource_manager()


users_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@users_bp.route("/alta", methods=["GET", "POST"])
@auth_m.permission_required("user_create")
def form_new():
    """Muestra el formulario de alta de usuario.

    Returns:
        str: formulario de alta de usuario renderizado.
    """
    roles = role_rm.query().all()
    form = CreateUser(roles)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores de formulario de alta de usuario.

        Returns:
            Response: mensaje de Nueva pagina.
        """
        roles_int = values["roles"]
        del values["roles"]
        roles = [role_rm.get(role) for role in roles_int]
        try:
            user_m.create(roles=roles, **values)
            flash(
                f"El usuario {values['first_name']} {values['last_name']} ha sido creado correctamente",
                "success",
            )
            return redirect("/usuarios/listado")
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Alta de usuario",
        form=form,
        submit_display_name="Crear usuario",
        on_success_with_data=on_success_with_data,
        cancel_button_url="/usuarios/listado",
    )


@users_bp.route("/listado", methods=["GET", "POST"])
@auth_m.permission_required("user_list")
def list():
    """Muestra el listado de usuarios.

    Returns:
        str: listado de usuarios renderizado.
    """

    def return_edit_button(user):
        return super_templates.Button(
            "Editar",
            url=generate_url("/usuarios/listado/editar", id=user.id),
            permission="user_update",
            btn_class="btn btn-outline-primary",
        )

    def return_delete_button(user):
        return super_templates.Button(
            "Eliminar",
            url=generate_url("/usuarios/listado/eliminar", id=user.id),
            permission="user_destroy",
            btn_class="btn btn-outline-danger",
        )

    return super_templates.render_list_view(
        title="Listado de usuarios"
        + (
            " activos"
            if request.args.get("estado") == "True"
            else " bloqueados"
            if request.args.get("estado") == "False"
            else ""
        )
        + (
            " con email similar a " + request.args.get("email")
            if request.args.get("email")
            else ""
        ),
        columns=[
            super_templates.Column(
                "Nombre completo", object_to_value=lambda user: user.full_name
            ),
            super_templates.Column("Email", object_to_value=lambda user: user.email),
            super_templates.Column(
                "Estado",
                object_to_value=lambda user: "Activo" if user.active else "Bloqueado",
            ),
            super_templates.Column(
                "Roles", object_to_value=lambda user: user.roles_names
            ),
        ],
        menu_global_buttons=[
            super_templates.Button(
                "Agregar usuario",
                url="/usuarios/alta",
                permission="user_create",
                btn_class="btn btn-outline-secondary",
            )
        ],
        row_buttons=[
            super_templates.CustomButton(return_edit_button),
            super_templates.CustomButton(return_delete_button),
        ],
        filter_global_buttons=[
            super_templates.Button(
                "Activo",
                url=generate_url(
                    url_for("privada.usuarios.list"), request.args, estado=True
                ),
                value="True",
            ),
            super_templates.Button(
                "Bloqueado",
                url=generate_url(
                    url_for("privada.usuarios.list"), request.args, estado=False
                ),
                value="False",
            ),
            super_templates.Button(
                "Ambos",
                url=generate_url(
                    url_for("privada.usuarios.list"), request.args, estado=""
                ),
                value="",
            ),
        ],
        paginator=user_m.filter_like_get_paginator(
            request.args.get("email"),
            request.args.get("estado"),
            request.args.get("page", "1"),
        ),
        actual_page="users",
        searchbar=[True, "Buscar por email", "email"],
    )


@users_bp.route("/listado/editar", methods=["GET", "POST"])
@auth_m.permission_required("user_update")
def form_edit():
    """Muestra el formulario de edición de usuario.

    Returns:
        str: formulario de edición de usuario renderizado.
    """
    user = validate_id(user_m, request.args, True)
    roles = role_rm.query().all()
    form = EditUser(user, roles)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores de formulario de edición de usuario.

        Returns:
            Resposnse: pagina a redireccionar.
        """

        roles_int = values["roles"]
        del values["roles"]
        active_value = values["active"]
        del values["active"]
        roles = [role_rm.get(role) for role in roles_int]
        try:
            user_m.update(id=user.id, **values)
            user_m.set_state(user.id, active_value)
            user_m.set_roles(user.id, roles)
            flash(
                f"El usuario {values['first_name']} {values['last_name']} ha sido actualizado correctamente",
                "success",
            )
            return redirect("/usuarios/listado")
        except Exception as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Editar usuario",
        form=form,
        on_success_with_data=on_success_with_data,
        cancel_button_url="/usuarios/listado",
    )


@users_bp.route("/listado/eliminar", methods=["GET", "POST"])
@auth_m.permission_required("user_destroy")
def delete():
    """Eliminación de usuario.

    Returns:
        Response: listado con flash.
    """
    user = validate_id(user_m, request.args, True)
    try:
        user_m.set_state(user.id, False)
        flash(
            f"El usuario {user.first_name} {user.last_name} ha sido bloqueado correctamente",
            "success",
        )
    except Exception as e:
        flash(str(e), "danger")
    finally:
        return redirect(request.referrer)
