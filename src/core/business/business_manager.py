"""Capa de negocio de alto nivel base, para una tabla de la BD."""
class BusinessManager:
    def __init__(self, table):
        """Constructor de la clase BusinessManager.

        Args:
            table (Base): Clase de la tabla a administrar.
        """
        self.database = table.resource_manager()
