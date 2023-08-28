from src.core.business.business_manager import BusinessManager
from src.core.database.board import Configuration


"""Capa de negocio de alto nivel, para la tabla de Configuración de la BD."""
class ConfigManager(BusinessManager):
    def __init__(self):
        """Constructor de la clase ConfigManager."""
        super().__init__(Configuration)

    def get_field(self, key):
        """Obtiene el valor de un campo de la configuración.

        Args:
            key (str): Nombre del campo.

        Returns:
            str: Valor del campo.
        """

        return self.database.get_value(key)

    def update(self, **kwargs):
        """Actualiza la configuración.

        Args:
            **kwargs: Claves y valores a actualizar.

        Returns:
            bool: True si la configuración se actualizó correctamente, False en caso contrario.
        """
        return self.database.update(**kwargs)

    def get_instance(self):
        """Obtiene la instancia de la configuración.

        Returns:
            Configuration: Instancia de la configuración.
        """
        return self.database.get_instance()

    def get_dict(self):
        """Obtiene la configuración como un diccionario.

        Returns:
            dict: Configuración como un diccionario.
        """
        output = {}

        for key in instance.__table__.columns.keys():
            output[key] = self.get_field(key)

        return output
