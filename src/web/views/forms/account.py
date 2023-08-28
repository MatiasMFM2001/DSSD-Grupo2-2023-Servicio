from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    DateField,
    EmailField,
    FileField,
    RadioField,
    PasswordField,
    BooleanField,
    SelectMultipleField,
)
from flask_wtf import FlaskForm
from src.web.views.forms.__init__ import default_class
from wtforms.validators import DataRequired, InputRequired, Regexp, NoneOf


"""Formulario base de altas de Usuarios y Socios."""
class FormAccount(FlaskForm):
    first_name = StringField(
        "Nombre",
        validators=[DataRequired()],
        description="Ingresa el nombre de la persona",
        render_kw=default_class,
    )
    last_name = StringField(
        "Apellido",
        validators=[DataRequired()],
        description="Ingresa el apellido de la persona",
        render_kw=default_class,
    )
    email = EmailField(
        "Email",
        validators=[DataRequired()],
        description="Ingresa el email de la persona",
        render_kw=default_class,
    )


"""Formulario base que contiene sólamente el campo contraseña."""
class PasswordField(FlaskForm):
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired()],
        description="Ingresa la contraseña de la persona",
        render_kw=default_class,
    )
