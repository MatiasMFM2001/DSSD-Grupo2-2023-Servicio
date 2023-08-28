from src.web.templates import super_templates
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.business.associate_manager import AssociateManager
from dateutil.relativedelta import relativedelta
from src.core.business.cuote_manager import CuoteManager
from src.core.business.user_manager import auth_m
from src.web.views.forms.graphics import *

graphics_bp = Blueprint("graphics_bp", __name__, url_prefix="/estadisticas")

associate_m = AssociateManager()
cuote_m = CuoteManager()


def diff_month(d1, d2):
    """Calcula el número de meses entre dos fechas.

    Args:
        d1 (datetime): Fecha inicial.
        d2 (datetime): Fecha end_dateal.

    Returns:
        int: Número de meses entre las dos fechas.
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month + 1


def dates_range(start_date, month_amount):
    """Genera una lista de fechas de meses partiendo de una fecha de inicio.

    Args:
        ininio (datetime): Fecha de inicio.
        cant_month (int): Cantidad de meses a generar.

    Returns:
        list: Lista de meses.
    """
    return [start_date + relativedelta(months=i) for i in range(month_amount)]


def add_keys_and_values(query_dict, date_range):
    """Agrega las claves y valores faltantes a un diccionario con una lista de fechas.

    Args:
        consulta (dict): Diccionario con las claves y valores.
        rangofechas (list): Lista de fechas."""
    for fecha in date_range:
        value = query_dict.get(fecha, 0)
        query_dict[fecha] = value


def remove_items_out_of_range(query_dict, date_range):
    """Elimina los items que no pertenecen al rango de fechas
    Args:
    consulta (dict): Diccionario con las claves y valores.
    rango_fechas (list): Lista de fechas.
    """
    listSub = [elem for elem in query_dict.keys() if elem not in date_range]
    [query_dict.pop(key) for key in listSub]


def sort_dictionary(query_dict):
    """Ordena un diccionario por su clave."""
    return {key: query_dict[key] for key in sorted(query_dict.keys())}


def on_success_data(values, query_dict, title, chart_type):
    start_date = values["start_date"]
    end_date = values["end_date"]
    month_amount = diff_month(end_date, start_date)
    date_range = dates_range(start_date, month_amount)
    add_keys_and_values(query_dict, date_range)
    remove_items_out_of_range(query_dict, date_range)
    sorted_query_dict = sort_dictionary(query_dict)
    labels = [key.strftime("%m/%Y") for key in sorted_query_dict.keys()]
    values = [str(value) for value in sorted_query_dict.values()]

    return render_template(
        "chart.html", title=title, labels=labels, values=values, chart_type=chart_type
    )


@graphics_bp.route("/socios_nuevos_mes", methods=["GET", "POST"])
@auth_m.permission_required("private_logout")
def line():
    """Grafica de lineas."""

    def on_success_with_data(values):
        query_dict = associate_m.new_associates_by_month()
        return on_success_data(values, query_dict, "Socios nuevos por mes", "line")

    return super_templates.render_form_view(
        title="Socios nuevos por mes",
        form=DateRange(),
        on_success_with_data=on_success_with_data,
        cancel_button_url="/estadisticas/socios_nuevos_mes",
    )


@graphics_bp.route("/recaudacion_mes", methods=["GET", "POST"])
@auth_m.permission_required("private_logout")
def bar():
    """Grafica de barras."""

    def on_success_with_data(values):
        query_dict = cuote_m.income_by_month()
        return on_success_data(values, query_dict, "Recaudacion por mes", "bar")

    return super_templates.render_form_view(
        title="Recaudacion por mes",
        form=DateRange(),
        on_success_with_data=on_success_with_data,
        cancel_button_url="/estadisticas/recaudacion_mes",
    )
