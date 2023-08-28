from src.web.views.forms.account import *
from src.web.views.forms.__init__ import *
from flask_wtf.file import FileField, FileRequired, FileAllowed


"""Formulario base de Socios."""
class FormAssociate(FormAccount):
    home_address = StringField(
        "Direccion",
        validators=[DataRequired()],
        description="Ingresa la direccion de la persona",
        render_kw=default_class,
    )
    genre = SelectField(
        "Género",
        choices=[
            ("default", "Seleccione el genero"),
            ("Masc", "Masculino"),
            ("Fem", "Femenino"),
            ("Otro", "Otro"),
        ],
        default="default",
        validators=[NoneOf(["default"])],
        render_kw=select,
    )
    doc_type = SelectField(
        "Tipo de documento",
        choices=[
            ("default", "Seleccione un documento"),
            ("DNI", "DNI"),
            ("LE", "Libreta Enrolamiento"),
            ("LC", "Libreta Civica"),
        ],
        default="default",
        validators=[NoneOf(["default"])],
        render_kw=select,
    )
    doc_number = IntegerField(
        "Numero de documento",
        validators=[DataRequired()],
        description="Ingresa el numero de documento de la persona",
        render_kw=default_class,
    )
    phone_number = IntegerField(
        "Numero de telefono",
        description="Ingresa el numero de telefono de la persona",
        render_kw=default_class,
    )
    image = FileField(
        "Foto de perfil",
        validators=[
            FileAllowed(
                ["jpg", "png", "bmp"], "Archivo inválido, sólo se permite JPG, PNG, BMP"
            )
        ],
        render_kw=default_class,
    )


"""Formulario de altas de Socios."""
class CreateAssociate(FormAssociate, PasswordField):
    pass


"""Formulario de modificaciones de Socios."""
class EditAssociate(FormAssociate):
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

    def __init__(self, edit):
        super().__init__()
        if edit is not None:
            self.first_name.default = edit.first_name
            self.last_name.default = edit.last_name
            self.email.default = edit.email
            self.home_address.default = edit.home_address
            self.genre.default = edit.genre
            self.doc_type.default = edit.doc_type
            self.doc_number.default = edit.doc_number
            self.phone_number.default = edit.phone_number
            self.active.default = str(edit.active)
