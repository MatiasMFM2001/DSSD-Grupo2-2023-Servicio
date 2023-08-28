from src.web.views.forms.account import *
from src.web.views.forms.__init__ import *


"""Formulario base de Usuarios."""
class FormUser(FormAccount):
    username = StringField(
        "Nombre de usuario",
        validators=[DataRequired()],
        description="Ingresa el nombre de usuario",
        render_kw=default_class,
    )
    active = SelectField(
        "Estado",
        choices=[
            ("", "Seleccionar estado"),
            ("True", "Activo"),
            ("False", "Bloqueado"),
        ],
        render_kw=select,
        validators=[InputRequired()],
        coerce=lambda result: result == "True",
    )
    roles = SelectMultipleField(
        "Roles", choices=[], render_kw=select, validators=[InputRequired()], coerce=int
    )

    def __init__(self, roles):
        super().__init__()
        self.roles.choices = [
            (role.id, role.name) for role in roles if role.name != "No autenticado"
        ]


"""Formulario de altas de Usuarios."""
class CreateUser(FormUser, PasswordField):
    pass


"""Formulario de modificaciones de Usuarios."""
class EditUser(FormUser):
    def __init__(self, edit, roles):
        super().__init__(roles)
        self.first_name.default = edit.first_name
        self.last_name.default = edit.last_name
        self.email.default = edit.email
        self.username.default = edit.username
        self.active.default = str(edit.active)
        self.roles.default = [role.id for role in edit.roles]
