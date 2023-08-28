from logging import PlaceHolder
from flask import Blueprint, render_template, flash, redirect, request
from src.web.templates import super_templates
from wtforms import (
    SelectField,
    StringField,
    DecimalField,
    IntegerField,
    TextAreaField,
    BooleanField,
)
from wtforms.validators import NumberRange, InputRequired, Length, Regexp
from flask_wtf import FlaskForm
from src.web.views.forms.sysconfig import *
from src.core.business.config_manager import ConfigManager
from src.core.business.service_manager import MembershipManager
from src.core.business.user_manager import auth_m


sysconfig_bp = Blueprint("configuracion", __name__, url_prefix="/configuracion_sistema")

sysconfig_m = ConfigManager()
membership_m = MembershipManager()


@sysconfig_bp.route("", methods=["GET", "POST"])
@auth_m.permission_required("config_update")
def update_config():
    """Actualiza la configuración del sistema.

    Returns:
        Response: Renderiza la plantilla de configuración del sistema.
    """
    config = sysconfig_m.get_instance()
    cost = membership_m.get_by_name("Base").mensual_cost
    form = FormConfig(config, cost)

    def on_success_with_data(values):
        """Actualiza la configuración del sistema con los valores del formulario.

        Args:
            values (dict): Diccionario con los valores de los campos del formulario.

        Returns:
            Response: Redirecciona a la página de configuración del sistema.
        """
        base_price = values.get("base_price", 100.0)
        del values["base_price"]

        sysconfig_m.update(**values)
        membership_m.update_by_name("Base", mensual_cost=base_price)

        flash("Configuración actualizada correctamente", "success")
        return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Configuración del sistema",
        form=form,
        on_success_with_data=on_success_with_data,
    )
