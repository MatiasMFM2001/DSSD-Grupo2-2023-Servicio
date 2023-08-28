from wtforms import StringField, IntegerField, DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, NumberRange, Optional
from src.web.views.forms.__init__ import *
from src.web.helpers.view_helpers import format_price, format_date


"""Formulario de consultas de Pagos."""
class FormPaymentSearch(FlaskForm):

    surname = StringField("Apellido", render_kw=default_class)
    associate_id = IntegerField(
        "Número de socio",
        validators=[Optional(), NumberRange(min=1)],
        render_kw=default_class,
    )

    def validate(self):
        """Valida el formulario.

        Returns:
            bool: True si el formulario es válido, False en caso contrario.
        """
        if not FlaskForm.validate(self):
            return False

        if not (self.surname.data) or not (self.associate_id.data):
            return True

        for field in [self.surname, self.associate_id]:
            field.errors.append("Sólo se puede usar un criterio")

        return False

    def __init__(self, surname, associate_id):
        super().__init__()
        self.surname.default = surname
        self.associate_id.default = associate_id


"""Formulario de confirmaciones de Pagos."""
class FormConfirm(FlaskForm):
    associate = StringField("Socio", render_kw=default_class)
    service_name = StringField("", render_kw=default_class)
    date = DateField("Fecha de pago", render_kw=default_class)
    original_price = StringField("Monto original", render_kw=default_class)
    late_fee = StringField("Monto de recargo", render_kw=default_class)
    total_price = StringField("Monto total", render_kw=default_class)

    def __init__(self, cuote, today, late_fee_amount):
        super().__init__()
        self.associate.default = cuote.associate.full_name
        self.service_name.default = cuote.service.name
        self.service_name.label.text = cuote.service.spanish_name()
        self.date.default = today
        self.original_price.default = format_price(cuote.price)
        self.late_fee.default = format_price(late_fee_amount)
        self.total_price.default = format_price(cuote.total_price)
