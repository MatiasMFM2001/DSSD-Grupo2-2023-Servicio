from flask import render_template


def render_error(name, description, error_code):
    """Renderizador genérico de errores.

    Args:
        name (str): recibe un nombre del error.
        description (str): recibe una descripcipción del error.
        error_code (int): recibe un código de estado.

    Returns:
        tuple: tupla con el codigo de error.html renderizado y el codigo de error 404.
    """

    return (
        render_template(
            "error.html", name=name, description=description, code=error_code
        ),
        error_code,
    )


def bad_request_error(exception):
    """Renderizador de errores de peticiones validas.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "Solicitud mal realizada",
        "El sistema no cargará la página porque recibió datos erróneos. Avisale a los desarrolladores.",
        400,
    )


def unauthorized_error(exception):
    """Renderizador de errores por no estar autorizado.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "Acceso sin credenciales",
        "El sistema no cargará la página porque no has iniciado sesión.",
        401,
    )


def forbidden_error(exception):
    """Renderizador de errores por no tener permisos.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "Acceso no autorizado",
        "El sistema no cargará la página porque no tenés permisos suficientes para accederla.",
        403,
    )


def not_found_error(exception):
    """Renderizador de errores por no encontrar la peticion.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "No se encontró la página",
        "La página a la que intentaste acceder no existe.",
        404,
    )


def unprocessable_entity_error(exception):
    """Renderizador de errores por una entidad que no se puede procesar.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "Solicitud no procesable",
        "El sistema no cargará la página porque recibió datos inválidos. Avisale a los desarrolladores.",
        422,
    )


def internal_server_error(exception):
    """Renderizador de errores dentro del servidor.

    Args:
        exception (exception): recibe una excepcion.
    Returns:
        str: devuelve un string con el error.
    """
    return render_error(
        "El servidor tuvo un error",
        "El sistema sufrió un error interno. Avisale a los desarrolladores.",
        500,
    )
