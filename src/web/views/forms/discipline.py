from wtforms import StringField, SelectField, SelectMultipleField, DecimalField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired
from src.web.views.forms.__init__ import *


"""Formulario base de Disciplinas."""
class FormDiscipline(FlaskForm):
    name = StringField(
        "Nombre de la disciplina",
        description="Ejemplo: Futbol",
        render_kw=default_class,
        validators=[DataRequired()],
    )
    categories = SelectMultipleField(
        "Categoría de la disciplina",
        description="Ejemplo: Pre-mini (5 a 8 años)",
        render_kw=select,
        validators=[DataRequired()],
        coerce=int,
    )
    new_category = StringField(
        "Nueva categoría",
        description="Ejemplo: Pre-mini (5 a 8 años)",
        render_kw=default_class,
    )
    teacher = StringField(
        "Nombre de los instructores",
        description="Ejemplo: Martín Gonzalez y María Gomez",
        render_kw=default_class,
        validators=[DataRequired()],
    )
    schedule_time = StringField(
        "Días y horarios de la   disciplina",
        description="Ejemplo: Martes y Jueves 18:00 a 19:00",
        render_kw=default_class,
        validators=[DataRequired()],
    )
    mensual_cost = DecimalField(
        "Costo mensual",
        description="Ejemplo: 1300",
        render_kw=default_class,
        validators=[DataRequired()],
    )
    active = SelectField(
        "Disciplina habilitada",
        choices=[("", "Seleccionar estado"), ("True", "Si"), ("False", "No")],
        render_kw=select,
        validators=[InputRequired()],
        coerce=lambda result: result == "True",
    )

    def __init__(self, categories):
        super().__init__()
        self.categories.choices = [(cat.id, cat.name) for cat in categories]


"""Formulario de modificaciones de Disciplinas."""
class EditDiscipline(FormDiscipline):
    def __init__(self, discipline, categories):
        super().__init__(categories)
        self.name.default = discipline.name
        self.categories.default = [cat.id for cat in discipline.categories]
        self.teacher.default = discipline.teacher
        self.schedule_time.default = discipline.schedule_time
        self.mensual_cost.default = discipline.mensual_cost
        self.active.default = "True" if discipline.active else "False"
