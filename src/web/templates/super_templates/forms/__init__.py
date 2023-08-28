from flask import render_template, request


def render_form_view(
    title="",
    form=None,
    submit_display_name="Guardar",
    on_success=lambda the_form: "",
    on_success_with_data=lambda values: "",
    on_success_with_file=lambda values, form: "",
    cancel_button_url=None,
    read_only=False,
):
    """Renderiza una vista de formulario con los parámetros recibidos.

    Args:
        title (str): Título de la vista.
        form (Form): Formulario a renderizar.
        submit_display_name (str): Nombre del botón de submit.
        on_success (function): Función a ejecutar.
        on_success_with_data (function): Función a ejecutar.
        read_only (bool): Indica si el formulario es de solo lectura.

    Returns:
        str: HTML de la vista.

    """
    if form.validate_on_submit():
        values = form.data
        del values["csrf_token"]

        return (
            on_success(form)
            or on_success_with_data(values)
            or on_success_with_file(values, form)
        )

    elif request.method == "GET":
        form.process()

    return render_template(
        "super_templates/forms/form_view.html",
        title=title,
        form=form,
        submit_display_name=submit_display_name,
        read_only=read_only,
        cancel_button_url=cancel_button_url,
    )
