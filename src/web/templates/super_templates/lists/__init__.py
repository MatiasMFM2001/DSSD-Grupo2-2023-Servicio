from flask import render_template
from src.web.templates.super_templates.lists.button import to_button_group


"""Abstracción de una columna estática de una tabla HTML."""
class Column:
    def __init__(
        self, display_name, object_key="", object_to_value=None, value_to_string=str
    ):
        """Representa una columna de una tabla.

        Args:
            display_name (str): Nombre de la columna.
            object_key (str): Llave del objeto a mostrar.
            object_to_value (function): Función que transforma el objeto a mostrar.
            value_to_string (function): Función que transforma el valor a mostrar.
        """
        self.display_name = display_name
        self.object_to_value = (
            object_to_value
            if callable(object_to_value)
            else (lambda o: getattr(o, object_key))
        )
        self.value_to_string = value_to_string


def render_list(
    columns=[],
    row_buttons=[],
    items=[],
    template_path="super_templates/lists/list_only.html",
):
    """Renderiza una lista con los parámetros recibidos.

    Args:
        columns (list): Lista de Column.
        row_buttons (list): Lista de Button.
        items (list): Lista de objetos a mostrar.
        template_path (str): Ruta del archivo HTML a renderizar.

    Returns:
        str: codigo HTML renderizado de la lista.
    """
    return render_template(
        template_path,
        columns=columns,
        row_buttons=to_button_group(row_buttons),
        items=items,
    )


def render_list_view(
    title="",
    columns=[],
    filter_global_buttons=[],
    menu_global_buttons=[],
    other_global_buttons=[],
    row_buttons=[],
    paginator=None,
    paginator_url="",
    actual_page=None,
    searchbar=[None, "", ""],
):
    """Renderiza una vista de lista con los parámetros recibidos.

    Args:
        title (str): Título de la vista.
        columns (list): Lista de Column.
        filter_global_buttons (list): Lista de Button.
        menu_global_buttons (list): Lista de Button.
        other_global_buttons (list): Lista de Button.
        row_buttons (list): Lista de Button.
        paginator (Paginator): Paginador.
        paginator_url (str): URL del paginador.
        actual_page (str): Valor de la pagina actual, se usa para setear active el elemento en navbar layout.
        searchbar (list): Contiene placeholder de searchbar y name a utilizar.

    Returns:
        str: codigo HTML renderizado de la vista.
    """

    class NullPaginator:
        items = []
        page = 0
        pages = 0
        total = 0
        prev_num = 0
        next_num = 0
        has_next = False
        has_prev = False
        per_page = 10

    return render_template(
        "super_templates/lists/list_view.html",
        title=title,
        filter_global_buttons=to_button_group(filter_global_buttons),
        menu_global_buttons=to_button_group(menu_global_buttons),
        other_global_buttons=to_button_group(other_global_buttons),
        paginator=paginator,
        paginator_url=paginator_url,
        actual_page=actual_page,
        searchbar=searchbar,
        rendered_list=render_list(
            columns=columns,
            row_buttons=row_buttons,
            items=(paginator or NullPaginator()).items,
        ),
    )


def render_pdf_list(columns=[], items=[]):
    return render_list(
        columns=columns,
        items=items,
        template_path="super_templates/lists/pdf_list.html",
    )
