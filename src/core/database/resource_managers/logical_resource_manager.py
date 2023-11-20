from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)


"""Abstracción de accesos a una tabla de la BD, donde se realizan bajas lógicas."""
class LogicalResourceManager(PhysicalResourceManager):
    def query(self, include_inactives=False):
        """Retorna la query para obtener instancias de este modelo.

        Args:
            include_inactives (bool, optional): Si se incluyen o no los inactivos. Defaults to False.

        Returns:
            Query: Query para obtener instancias de este modelo.
        """
        query = super().query()

        if not include_inactives:
            query = query.filter(self.model_class.active == True)

        return query

    def get(self, id, include_inactives=False):
        return self.query_for(id, include_inactives).one()

    def update(self, id, include_inactives=False, **kwargs):
        self.update_each(self.query_for(id, include_inactives), **kwargs)

    def filter(self, include_inactives=False, *predicates):
        """Retorna la query para obtener instancias de este modelo que cumplan con los predicados dados.

        Args:
            include_inactives (bool, optional): Si se incluyen o no los inactivos. Defaults to False.
            *predicates: Predicados para filtrar las instancias.

        Returns:
            Query: Query para obtener instancias de este modelo que cumplan con los predicados dados.
        """
        return self.query(include_inactives=include_inactives).filter(*predicates)

    def filter_by(self, include_inactives=False, **kwargs):
        """Retorna la query para obtener instancias de este modelo que cumplan con los criterios dados.

        Args:
            include_inactives (bool, optional): Si se incluyen o no los inactivos. Defaults to False.
            **kwargs: Criterios para filtrar las instancias.

        Returns:
            Query: Query para obtener instancias de este modelo que cumplan con los criterios dados.
        """
        return self.query(include_inactives=include_inactives).filter_by(**kwargs)

    def query_for(self, id, include_inactives=False, model_class=None):
        """Retorna la query para obtener una instancia de este modelo con el identificador dado.

        Args:
            id (int): Identificador de la instancia.
            include_inactives (bool, optional): Si se incluyen o no los inactivos. Defaults to False.

        Returns:
            Query: Query para obtener una instancia de este modelo con el identificador dado.
        """
        return self.filter_by(include_inactives=include_inactives, id=id)

    def remove_each(self, query):
        """Elimina las instancias de este modelo que cumplan con la query dada.

        Args:
            query (Query): Query para obtener las instancias a eliminar.
        """
        self.update_each(query, active=False)
