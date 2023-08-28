from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from pyparsing import Regex
from src.web.views.forms.auth import *
from src.web.templates import super_templates
from src.core.business.user_manager import auth_m


auth_bp = Blueprint("autenticación", __name__, url_prefix="")

profile_bp = Blueprint("perfil", __name__, url_prefix="/perfil")

auth_bp.register_blueprint(profile_bp)


@auth_bp.route("/iniciar_sesion/", methods=["GET", "POST"])
@auth_m.permission_required("private_login", False)
def login():
    """Muestra el formulario de inicio de sesión.

    Returns:
        str: formulario de inicio de sesión renderizado.
    """
    email = request.args.get("email")
    form = FormLogIn(email)

    def on_success_with_data(values):
        """Función que se ejecuta si el formulario es válido.

        Args:
            values (dict): diccionario con los valores del formulario.

        Returns:
            Response: redirecciona a la página de inicio.
        """
        user = auth_m.login(values["email"], values["password"])

        if user is None:
            flash("Credenciales inválidas", "danger")
            return redirect(
                url_for("privada.autenticación.login", email=values["email"])
            )

        session["id"] = user.id
        return redirect(url_for("privada.home"))

    return super_templates.render_form_view(
        title="Iniciar Sesión",
        form=form,
        on_success_with_data=on_success_with_data,
        submit_display_name="Iniciar Sesión",
        cancel_button_url="/inicio",
    )


@profile_bp.route("/editar", methods=["GET", "POST"])
@auth_m.permission_required("private_logout")
def form_profile():
    """Muestra el formulario de edición de perfil.

    Returns:
        str: formulario de alta de usuario renderizado.
    """

    form = ChangePasswordForm()
    user_id = auth_m.current_id()

    def on_success_with_data(values):
        """Acción a realizar cuando el formulario es válido.

        Args:
            values (dict): valores de formulario de alta de usuario.

        Returns:
            Response: mensaje de Nueva pagina.
        """
        auth_m.update(user_id, password=values["new_pass"])

        flash("Tu contraseña ha sido actualizada correctamente", "success")
        return redirect(request.referrer)

    return super_templates.render_form_view(
        title="Editar contraseña",
        form=form,
        on_success_with_data=on_success_with_data,
        cancel_button_url="/usuarios/listado",
    )


@profile_bp.route("/cerrar_sesion")
@auth_m.permission_required("private_logout")
def logout():
    """Permite cerrar sesión.

    Returns:
        Response: redirecciona a la página de inicio.
    """
    del session["id"]
    session.clear()

    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("privada.home"))
