from src.core.business.user_manager import auth_m


"""Abstracción de un botón HTML estático."""
class Button:
    def __init__(
        self,
        display_name,
        url="",
        btn_class=None,
        disabled=False,
        visible=True,
        permission=None,
        value=None,
    ):
        """Constructor de la clase Button.

        Args:
            display_name (str): Nombre del botón.
            url (str): URL del botón.
            btn_class (str): Clase del botón.
            disabled (bool): Indica si el botón está deshabilitado.
            visible (bool): Indica si el botón es visible.
            permission (str): Permiso del botón.
            value (bool): Setea la propiedad value del botón.

        """
        self.display_name = display_name
        self.url = url
        self.btn_class = btn_class
        self.disabled = disabled
        self.value = value

        if not visible:
            self.visible = False
        elif permission:
            self.visible = auth_m.current_user_has_permission(permission)
        else:
            self.visible = True

    def get_button(self, obj):
        """Retorna una instancia de Button.

        Returns:
            Button: instancia de Button.
        """
        return self


"""Placeholder de un botón HTML, para mostrar botones de distintos tipos según el estado de cada objeto (uno por fila de la tabla renderizándose) enviado a get_button()."""
class CustomButton:
    def __init__(self, object_to_button):
        """Constructor de la clase CustomButton.

        Args:
            object_to_button (function): Función que transforma el objeto a mostrar.
        """
        self.object_to_button = object_to_button

    def get_button(self, obj):
        """Retorna una instancia de Button a partir de un objeto.

        Args:
            obj (object): Objeto a transformar.

        Returns:
            Button: instancia de Button.
        """
        return self.object_to_button(obj)


"""Abstracción de un grupo de botones HTML."""
class ButtonGroup:
    def __init__(
        self,
        buttons,
        display_name="",
        base_url="",
        formatter="{button_diplay_name} de {group_diplay_name}",
    ):
        """Constructor de la clase ButtonGroup.

        Args:
            buttons (list): Lista de botones.
            display_name (str): Nombre del grupo de botones. Default: "".
            base_url (str): URL base de los botones. Default: "".
            formatter (str): Formato de los nombres de los botones. Default: "{button_diplay_name} de {group_diplay_name}".
        """
        self.buttons = buttons
        self.display_name = display_name
        self.base_url = base_url
        self.formatter = formatter

    def get_buttons(self, obj=None):
        """Retorna una lista de botones.

        Args:
            obj (object): Objeto a transformar.

        Returns:
            list: Lista de botones.
        """
        visible_buttons = []

        for custom_button in self.buttons:
            button = custom_button.get_button(obj)

            if button.visible:
                visible_buttons.append(button)

        return visible_buttons

    def get_url(self, button):
        """Retorna la URL de un botón.

        Args:
            button (Button): Botón.

        Returns:
            str: URL del botón.
        """
        return f"{self.base_url}{button.url}"

    def get_display_name(self, button):
        """Retorna el nombre de un botón.

        Args:
            button (Button): Botón.

        Returns:
            str: Nombre del botón.
        """
        if not self.display_name:
            return button.display_name

        return self.formatter.format(
            button_diplay_name=button.display_name, group_diplay_name=self.display_name
        )

    def is_active(self, current_path):
        """Retorna si el grupo de botones está activo.

        Args:
            current_path (str): URL actual.

        Returns:
            _Bool: True si el grupo de botones está activo, False de lo contrario.
        """
        return current_path.startswith(self.base_url)

    def mark_active(self, current_path):
        """Marca el botón activo.

        Args:
            current_path (str): URL actual.

        Returns:
            str: Clase del botón.
        """
        return "active" * self.is_active(current_path)

    def is_one(self, custom_buttons):
        """Retorna si el grupo de botones tiene un solo botón.

        Args:
            custom_buttons (list): Lista de botones.

        Returns:
            Bool: True si el grupo de botones tiene un solo botón, False de lo contrario.
        """
        return len(custom_buttons) == 1

    def is_more_one(self, custom_buttons):
        """Retorna si el grupo de botones tiene más de un botón.

        Args:
            custom_buttons (list): Lista de botones.

        Returns:
            Bool: True si el grupo de botones tiene más de un botón, False de lo contrario.
        """
        return len(custom_buttons) > 1

    def get_class(self, custom_buttons):
        """Retorna dropdown si el grupo de botones tiene más de un botón, de lo contrario retorna "".

        Args:
            custom_buttons (list): Lista de botones.

        Returns:
            str: dropdown si el grupo de botones tiene más de un botón, de lo contrario retorna "".
        """
        return "dropdown" * self.is_more_one(custom_buttons)


def to_button_group(list_or_group, display_name=""):
    """Retorna un grupo de botones.

    Args:
        list_or_group (list or ButtonGroup): Lista de botones o grupo de botones.
        display_name (str): Nombre del grupo de botones. Default: "".

    Returns:
        ButtonGroup: Grupo de botones.
    """
    if isinstance(list_or_group, ButtonGroup):
        return list_or_group

    return ButtonGroup(list_or_group, display_name)
