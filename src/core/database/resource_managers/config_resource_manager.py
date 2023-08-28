from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)


"""Abstracción de accesos a la tabla de Configuración de la BD, implementando el patrón Singleton."""
class ConfigResourceManager(PhysicalResourceManager):
    def create(self, **kwargs):
        """Crea una instancia de este modelo en la base de datos.

        Args:
            **kwargs: Argumentos para crear la instancia.
        """
        if self.query().first() is None:
            super().create(**kwargs)

    def query_for(self, id):
        """Retorna la query para obtener una instancia de este modelo.

        Args:
            id (int): Identificador de la instancia.

        Returns:
            Query: Query para obtener una instancia de este modelo.
        """
        self.create()
        return self.query()

    def remove(self, id):
        """Elimina una instancia de este modelo de la base de datos.

        Args:
            id (int): Identificador de la instancia.
        """
        pass

    def get_instance(self):
        """Retorna la instancia de este modelo.

        Returns:
            Model: Instancia de este modelo.
        """
        return self.get(None)

    def get_value(self, key):
        """Retorna el valor de la configuración para la clave dada.

        Args:
            key (str): Clave de la configuración.

        Returns:
            str: Valor de la configuración.
        """
        return getattr(self.get_instance(), key)

    def update(self, **kwargs):
        """Actualiza una instancia de este modelo en la base de datos.

        Args:
            **kwargs: Argumentos para actualizar la instancia.
        """
        super().update(None, **kwargs)
