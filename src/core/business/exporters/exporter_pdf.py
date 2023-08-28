from src.web.templates.super_templates import render_pdf_list
from flask import render_template, current_app
import pdfkit
import os


def export_list(columns=[], items=[]):
    """Exporta una lista a un archivo PDF.

    Args:
        columns (list, optional): Lista de columnas. Defaults to [].
        items (list, optional): Lista de filas. Defaults to [].


    Returns:
        bytes: Archivo PDF.
    """

    html = render_pdf_list(columns=columns, items=items)
    css = ["public/css/pdf_list.css"]

    return pdfkit.from_string(html, css=css)


def export_receipt(cuote):
    """Exporta un recibo a un archivo PDF.

    Args:
        cuote (Cuote): Cuota.

    Returns:
        bytes: Archivo PDF.
    """
    root_path = os.path.dirname(current_app.instance_path)
    html = render_template("pdf_receipt.html", cuote=cuote, root_path=root_path)
    css = ["public/css/pdf_receipt.css"]
    options = {"enable-local-file-access": ""}

    return pdfkit.from_string(html, css=css, options=options)


def export_card(associate, state):
    """Exporta un recibo a un archivo PDF.

    Args:
        cuote (Cuote): Cuota.

    Returns:
        bytes: Archivo PDF.
    """
    root_path = os.path.dirname(current_app.instance_path)
    html = render_template(
        "card_export.html", associate=associate, state=state, root_path=root_path
    )
    css = ["public/css/license.css"]
    options = {
        "enable-local-file-access": "",
        "orientation": "landscape",
        "disable-smart-shrinking": "",
    }

    return pdfkit.from_string(html, css=css, options=options)
