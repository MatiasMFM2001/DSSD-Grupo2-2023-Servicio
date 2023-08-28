from attr import validate
from core.business.service_manager import DisciplineManager
from core.database.board import Category
from flask import Blueprint, request, url_for, flash, redirect
from src.web.templates import super_templates
from src.core.business.user_manager import auth_m
from src.web.helpers.controller_helpers import generate_url, validate_id
from src.web.views.forms.discipline import *
from src.web.views.lists.discipline import *


disciplines_bp = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")

disciplines_m = DisciplineManager()
categories_rm = Category.resource_manager()


@disciplines_bp.route("/listado")
@auth_m.permission_required("discipline_list")
def list():
    """Muestra el listado de disciplinas.

    Returns:
        str: listado de disciplinas renderizado.
    """
    page = disciplines_m.filter_like_get_paginator(
        request.args.get("nombre"),
        request.args.get("estado"),
        request.args.get("page", "1"),
    )
    request_args = request.args
    return list_disciplines(page, request_args)


@disciplines_bp.route("/listado/editar", methods=["GET", "POST"])
@auth_m.permission_required("discipline_update")
def form_edit():
    """Muestra el formulario de edición de disciplinas.

    Returns:
        str: formulario de edición de disciplinas renderizado.
    """

    discipline = validate_id(disciplines_m, request.args, True)
    categories = categories_rm.filter_by().all()
    form = EditDiscipline(discipline, categories)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values:valores formulario de edición de disciplinas.

        Returns:
            Response: pagina a redirigir
        """

        categories_int = values["categories"]
        del values["categories"]
        active_value = values["active"]
        del values["active"]
        categories = [categories_rm.get(cat) for cat in categories_int]
        if values.get("new_category"):
            categories.append(categories_rm.create(name=values.get("new_category")))
        del values["new_category"]
        try:
            disciplines_m.update(id=discipline.id, **values)
            disciplines_m.set_categories(discipline.id, categories)
            disciplines_m.set_state(discipline.id, active_value)
            flash(
                f"La disciplina {values['name']} ha sido actualizada correctamente",
                "success",
            )
            return redirect("/disciplinas/listado")
        except Exception as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Editar disciplina",
        form=form,
        on_success_with_data=on_success_with_data,
        cancel_button_url="/disciplinas/listado",
    )


@disciplines_bp.route("/listado/eliminar", methods=["GET", "POST"])
@auth_m.permission_required("discipline_destroy")
def delete():
    """Eliminación de disciplina.

    Returns:
        Response: listado con flash.
    """
    discipline = validate_id(disciplines_m, request.args, True)
    try:
        disciplines_m.set_state(discipline.id, False)
        flash(
            f"La disciplina {discipline.name} ha sido deshabilitada correctamente",
            "success",
        )
    except Exception as e:
        flash(str(e), "danger")
    finally:
        return redirect(request.referrer)


@disciplines_bp.route("/alta", methods=["GET", "POST"])
@auth_m.permission_required("discipline_create")
def form_new():
    """Muestra el formulario de alta de disciplinas.

    Returns:
        str: formulario de alta de disciplinas renderizado.
    """
    categories = categories_rm.filter_by().all()
    form = FormDiscipline(categories)

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

            Args:
            values:valores formulario de alta de disciplinas.

        Returns:
            Response: pagina a redirigir
        """
        categories_int = values["categories"]
        del values["categories"]
        categories = [categories_rm.get(cat) for cat in categories_int]
        if values.get("new_category"):
            categories.append(categories_rm.create(name=values.get("new_category")))
        del values["new_category"]
        try:
            disciplines_m.create(categories=categories, **values)
            flash(
                f"La disciplina {values['name']} ha sido dada de alta correctamente",
                "success",
            )
            return redirect("/disciplinas/listado")
        except Exception as e:
            flash(str(e), "danger")
            return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Alta de disciplina",
        form=form,
        on_success_with_data=on_success_with_data,
        submit_display_name="Crear disciplina",
        cancel_button_url="/disciplinas/listado",
    )
