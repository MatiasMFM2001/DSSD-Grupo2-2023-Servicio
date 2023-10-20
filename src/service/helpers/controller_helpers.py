from xml.etree.ElementInclude import include
from flask import Response, abort, request
from urllib.parse import urlencode
from src.api.helpers.api_responses import SimpleErrorResponse
from io import BytesIO
import re


def PDFResponse(pdf_bytes, filename, as_attachment):
    """Crea una respuesta con un archivo PDF.

    Args:
        pdf_bytes (bytes): bytes del archivo PDF.
        filename (str): nombre del archivo.
        as_attachment (bool): si el archivo se descarga o se muestra en el navegador.

    Returns:
        Response: respuesta con el archivo PDF.
    """
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f"attachment;filename={filename}.pdf"
            if as_attachment
            else "inline"
        },
    )


def CSVResponse(csv_bytes, filename, as_attachment):
    """Crea una respuesta con un archivo CSV.

    Args:
        csv_bytes (bytes): bytes del archivo CSV.
        filename (str): nombre del archivo.
        as_attachment (bool): si el archivo se descarga o se muestra en el navegador.

    Returns:
        Response: respuesta con el archivo CSV.
    """
    return Response(
        csv_bytes,
        mimetype="application/csv",
        headers={
            "Content-Disposition": f"attachment;filename={filename}.csv"
            if as_attachment
            else "inline"
        },
    )


def generate_url(path, values={}, **more_values):
    """Genera una URL con los valores especificados.

    Args:
        path (str): ruta de la URL.
        values (dict, optional): valores de la URL. Defaults to {}.
        **more_values: mas valores de la URL.
    Returns:
        str: URL con los valores especificados.
    """
    query = dict(values)
    query.update(more_values)
    return f"{path}?{urlencode(query)}"


def is_integer(string_to_check):
    """Valida si el string ingresado es un entero.

    Args:
        string_to_check (str): String a validar.
    Returns:
        match: Devuelve el match si es un entero, None si no lo es.

    """
    if type(string_to_check) is int:
        return string_to_check

    return re.match(r"\A\d+\Z", string_to_check)


def get_int(request_args, key, error_raiser, key_meaning):
    if not key in request_args:
        return (
            None,
            error_raiser(
                400,
                f"La {key_meaning} '{key}' no fue incluída en los argumentos de la query URL",
            ),
        )

    value = request_args.get(key)

    if not is_integer(value):
        return (
            None,
            error_raiser(400, f"La {key_meaning} {value} no es un entero válido"),
        )

    return (int(value), None)

def get_string(request_args, key, error_raiser, key_meaning):
    if not key in request_args:
        return (
            None,
            error_raiser(
                400,
                f"La {key_meaning} '{key}' no fue incluída en los argumentos de la query URL",
            ),
        )

    return (request_args.get(key), None)


def internal_validate(
    manager,
    request_args,
    key,
    error_raiser,
    tuple_name,
    tuple_getter,
    tuple_finder,
    key_meaning,
    key_getter,
    **kwargs
):
    """Valida si el id ingresado es un entero y si existe en la base de datos.

    Args:
        manager (Manager): Manager de la entidad.
        request_args (dict): Diccionario con los argumentos de la request.
        include_inactive (bool): Si se incluyen los inactivos. Defaults to False.
        key (str): Clave a buscar. Defaults to 'id'.
        error_raiser (function): Función a llamar cuando hay errores.
    Returns:
        object: Devuelve el objeto si el id es válido, None si no lo es.
    """
    key, error = key_getter(request_args, key, error_raiser, key_meaning)

    if error:
        return (None, error)

    if not tuple_finder(key, **kwargs):
        return (None, error_raiser(404, f"{tuple_name} de {key_meaning} {key} no existe"))

    return (tuple_getter(key, **kwargs), None)

def internal_validate_id(
    manager,
    request_args,
    key,
    error_raiser,
    tuple_name,
    **kwargs
):
    return internal_validate(
        manager,
        request_args,
        key,
        error_raiser,
        tuple_name,
        manager.get,
        manager.exists,
        "ID",
        get_int,
        **kwargs
    )

def internal_validate_string(
    manager,
    request_args,
    key,
    error_raiser,
    tuple_name,
    tuple_getter,
    **kwargs
):
    return internal_validate(
        manager,
        request_args,
        key,
        error_raiser,
        tuple_name,
        tuple_getter,
        lambda key, **kwargs: tuple_getter(key, **kwargs),
        "string",
        get_string,
        **kwargs
    )


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_id(
    manager,
    request_args,
    key="id",
    tuple_name="La tupla",
    **kwargs
):
    result = internal_validate_id(
        manager,
        request_args,
        include_inactive,
        key,
        lambda http_code, message: abort(http_code),
        tuple_name,
        **kwargs,
    )

    return result[0]


def api_validate_id(
    manager,
    request_args,
    key="id",
    tuple_name="La tupla",
    **kwargs
):
    return internal_validate_id(
        manager,
        request_args,
        key,
        SimpleErrorResponse,
        tuple_name,
        **kwargs
    )

def api_validate_string(
    manager,
    request_args,
    tuple_getter = None,
    key="id",
    tuple_name="La tupla",
    **kwargs
):
    tuple_getter = tuple_getter or (lambda k, **kwargs: manager.filter_by_get_list(**{key: k}))
    
    return internal_validate_string(
        manager,
        request_args,
        key,
        SimpleErrorResponse,
        tuple_name,
        tuple_getter,
        **kwargs
    )

def internal_validate_file(request_files, field_name, allowed_mimes, error_raiser):
    if not field_name in request_files:
        return (
            None,
            error_raiser(
                400,
                f"La solicitud POST no incluyó el campo '{field_name}' de tipo archivo",
            ),
        )

    buffer = BytesIO(request.files[field_name].read())
   
    '''
    file_mime = magic.from_buffer(buffer.read(), mime=True)

    if not file_mime in allowed_mimes:
        return (
            None,
            error_raiser(
                400,
                f"El archivo '{field_name}' es de tipo '{file_mime}', en lugar de: {allowed_mimes}",
            ),
        )
    '''

    return (buffer, "", None)


def validate_file(
    request_files,
    field_name,
    allowed_mimes,
    error_raiser=lambda http_code, message: abort(http_code),
):
    result = internal_validate_file(
        request_files, field_name, allowed_mimes, error_raiser
    )

    return (result[0], result[1])


def api_validate_file(request_files, field_name, allowed_mimes):
    return internal_validate_file(
        request_files, field_name, allowed_mimes, SimpleErrorResponse
    )