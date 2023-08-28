from wtforms import (
    StringField,
    TextAreaField,
    DecimalField,
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
from src.web.views.forms.__init__ import *
from wtforms.validators import NumberRange, InputRequired, Length, Regexp


"""Formulario de modificaciones de la Configuración."""
class FormConfig(FlaskForm):

    rows_per_page = IntegerField(
        "Cantidad de elementos por página",
        render_kw=default_class,
        validators=[InputRequired(), NumberRange(min=1)],
    )

    show_payment_table = SelectField(
        "Habilitar tabla de pagos",
        choices=[(True, "Sí"), (False, "No")],
        render_kw=select,
        validators=[InputRequired()],
        coerce=lambda x: str(x) == "True",
    )

    phone_number = StringField(
        "Número de teléfono",
        render_kw=default_class,
        validators=[InputRequired(), Length(min=8, max=20), Regexp(r"^\d+$")],
    )

    club_email = StringField(
        "Email del club",
        render_kw=default_class,
        validators=[InputRequired(), Length(min=8, max=50), Regexp(r"^\S+@\S+$")],
    )

    payment_text = TextAreaField(
        "Texto a mostrar en el encabezado del Recibo de Pago",
        render_kw=default_class,
        validators=[InputRequired()],
    )

    price_format = StringField(
        "Formato de moneda",
        render_kw=default_class,
        validators=[InputRequired(), Length(max=32), Regexp(".*<valor>.*")],
    )

    base_price = DecimalField(
        "Valor de la cuota mensual base",
        render_kw=default_class,
        validators=[InputRequired(), NumberRange(min=0.0)],
    )

    late_fee_percentage = DecimalField(
        "Porcentaje de recargo para cuotas adeudadas",
        render_kw=default_class,
        validators=[InputRequired(), NumberRange(min=0.0, max=100.0)],
    )

    def __init__(self, config, base_price):
        super().__init__()
        self.rows_per_page.default = config.rows_per_page
        self.show_payment_table.default = config.show_payment_table
        self.phone_number.default = config.phone_number
        self.club_email.default = config.club_email
        self.payment_text.default = config.payment_text
        self.price_format.default = config.price_format
        self.base_price.default = base_price
        self.late_fee_percentage.default = config.late_fee_percentage
