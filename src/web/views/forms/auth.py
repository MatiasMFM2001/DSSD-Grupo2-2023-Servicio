from wtforms import StringField, PasswordField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Regexp, InputRequired, EqualTo
from src.web.views.forms.__init__ import default_class


"""Formulario de inicio de sesión de Usuarios."""
class FormLogIn(FlaskForm):

    email = EmailField(
        "Correo electrónico",
        validators=[DataRequired()],
        description="Ingresa tu correo electrónico",
        render_kw=default_class,
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired()],
        description="Ingresa tu contraseña",
        render_kw=default_class,
    )

    def __init__(self, email):
        super().__init__()
        self.email.default = email


"""Formulario de modificación de contraseña de Usuarios."""
class ChangePasswordForm(FlaskForm):
    new_pass = PasswordField(
        "Nueva contraseña",
        validators=[
            InputRequired(),
            EqualTo("confirm_pass", message="Las contraseñas deben ser iguales"),
        ],
        render_kw=default_class,
    )

    confirm_pass = PasswordField("Confirmar contraseña", render_kw=default_class)
