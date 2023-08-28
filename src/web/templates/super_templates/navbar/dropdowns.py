from src.web.templates.super_templates.lists.button import Button, ButtonGroup


def get_left():
    """Retorna una lista de dropdowns del navbar para el lado izquierdo.

    Returns:
        list: Lista de dropdowns.
    """
    return [
        ButtonGroup(
            [Button("Inicio", url="", permission="home_show")], base_url="/inicio"
        ),
        ButtonGroup(
            [
                Button("Listado", url="/listado", permission="user_list"),
                Button("Alta", url="/alta", permission="user_create"),
            ],
            "Usuarios",
            "/usuarios",
        ),
        ButtonGroup(
            [
                Button("Listado", url="/listado", permission="associate_list"),
                Button("Alta", url="/alta", permission="associate_create"),
                Button("Cuotas", url="/pagos/listado", permission="payment_list"),
            ],
            "Socios",
            "/socios",
        ),
        ButtonGroup(
            [
                Button("Listado", url="/listado", permission="discipline_list"),
                Button("Alta", url="/alta", permission="discipline_create"),
            ],
            "Disciplinas",
            "/disciplinas",
        ),
        ButtonGroup(
            [
                Button(
                    "Socios nuevos por mes",
                    url="/socios_nuevos_mes",
                    permission="private_logout",
                ),
                Button(
                    "Recaudacion por mes",
                    url="/recaudacion_mes",
                    permission="private_logout",
                ),
            ],
            "Estadisticas",
            base_url="/estadisticas",
        ),
        ButtonGroup(
            [Button("Configuración", url="", permission="config_update")],
            base_url="/configuracion_sistema",
        ),
    ]


def get_right():
    """Retorna una lista de dropdowns del navbar para el lado derecho.

    Returns:
        list: Lista de dropdowns.
    """
    return [
        ButtonGroup(
            [Button("Iniciar sesión", url="", permission="private_login")],
            base_url="/iniciar_sesion",
        ),
        ButtonGroup(
            [
                Button("Editar contraseña", url="/editar", permission="private_logout"),
                Button(
                    "Cerrar sesión", url="/cerrar_sesion", permission="private_logout"
                ),
            ],
            "Mi cuenta",
            "/perfil",
        ),
    ]
