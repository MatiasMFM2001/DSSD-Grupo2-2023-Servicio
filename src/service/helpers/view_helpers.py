from num2words import num2words
from src.core.business.config_manager import ConfigManager

config_m = ConfigManager()


def disable_if(condition: bool) -> str:
    """Deshabilita un elemento HTML si condition es True.
        Usarlo dentro de templates, por ejemplo: <button {{ disable_if(True) }}>Botón deshabilitado</button>.

    Args:
        condition (bool): condición a evaluar.

    Returns:
        str: atributo "disabled" si la condición es verdadera, cadena vacía en caso contrario.
    """
    return "disabled" if condition else ""


def num_to_spanish_words(num: int) -> str:
    """Convierte un número a palabras en español.

    Args:
        num (int): número a convertir.

    Returns:
        str: número convertido a palabras.
    """

    return num2words(num, lang="es")


def format_price(price):
    """Aplica el formato de moneda a un precio.

    Args:
        price (float): precio a cambiar de formato.

    Returns:
        str: precio con formato aplicado.
    """
    return config_m.get_field("price_format").replace("<valor>", f"{price:.2f}")


def format_date(date, format_str):
    """Formatea una fecha a un formato dado.

    Args:
        date (datetime): fecha a formatear.
        format_str (str): formato a aplicar.
    Returns:
        str: fecha formateada.
    """
    formatted = date.strftime(format_str)

    months = [
        ("January", "Enero"),
        ("February", "Febrero"),
        ("March", "Marzo"),
        ("April", "Abril"),
        ("May", "Mayo"),
        ("June", "Junio"),
        ("July", "Julio"),
        ("August", "Agosto"),
        ("September", "Septiembre"),
        ("October", "Octubre"),
        ("November", "Noviembre"),
        ("December", "Diciembre"),
    ]

    for english, spanish in months:
        formatted = formatted.replace(english, spanish)

    return formatted