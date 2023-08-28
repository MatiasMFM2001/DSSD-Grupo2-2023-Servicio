from flask import render_template
from src.web.templates.super_templates.lists.button import to_button_group
from src.web.templates.super_templates.navbar.dropdowns import get_left, get_right


def render_navbar():
    """Renderiza el navbar.

    Returns:
        str: Navbar renderizado en HTML.
    """
    return render_template(
        "super_templates/navbar/navbar.html",
        left_dropdowns=get_left(),
        right_dropdowns=get_right(),
    )
