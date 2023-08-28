from src.web.views.forms.account import *
from src.web.views.forms.__init__ import *

from wtforms import DateTimeField
from datetime import datetime


"""Formulario de rango de fechas para gráficos de Estadísticas."""
class DateRange(FlaskForm):
    start_date = DateTimeField(
        "Fecha de inicio",
        render_kw=default_class,
        validators=[InputRequired()],
        format="%m/%Y",
        description="ejemplo: 1/2022",
    )

    end_date = DateTimeField(
        "Fecha de fin",
        render_kw=default_class,
        validators=[InputRequired()],
        format="%m/%Y",
        description="ejemplo: 12/2022",
    )

    def validate(self):
        """Valida el formulario.

        Returns:
            bool: True si el formulario es válido, False en caso contrario.
        """
        if not FlaskForm.validate(self):
            return False

        start_date = self.start_date.data
        end_date = self.end_date.data
        today = datetime.today()

        if end_date > today:
            self.end_date.errors.append(
                "La fecha final no puede ser mayor a la fecha actual"
            )
            return False

        if start_date > today:
            self.start_date.errors.append(
                "La fecha inicio no puede ser mayor a la fecha actual"
            )
            return False

        if end_date < start_date:
            self.start_date.errors.append(
                "La fecha de inicio debe ser menor que la fecha de fin"
            )
            return False

        if end_date == start_date:
            self.end_date.errors.append(
                "La fecha de inicio y de fin no pueden ser iguales"
            )
            return False

        return True
