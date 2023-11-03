from xml.etree.ElementInclude import include
from src.core.business.business_manager import BusinessManager


"""Capa de negocio de alto nivel base, para una tabla de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class CRUDManager(BusinessManager):
    def __init__(self, table):
        """Constructor de la clase CRUDManager.

        Args:
            table (Base): Clase de la tabla a administrar.
        """
        super().__init__(table)

    @property
    def rows_per_page(self):
        """Obtiene la cantidad de filas por página.

        Returns:
            int: Cantidad de filas por página.
        """
        return 20
        
    def validate(self, **kwargs):
        pass

    def validate_update(self, id, **kwargs):
        pass

    def create(self, **kwargs):
        """Crea una instancia en la base de datos.

        Args:
            **kwargs: Valores a actualizar.

        Returns:
            any: Instancia creada.
        """
        self.validate(**kwargs)
        return self.database.create(**kwargs)

    def get(self, id, include_inactive=False):
        """Obtiene una instancia de la base de datos.

        Args:
            id (int): Identificador de la instancia.
            include_inactive (bool): Incluir elementos borrados logicamente, default to False

        Returns:
            any: Instancia de la base de datos.
        """
        return self.database.get(id, include_inactive)

    def get_all(self, id_list, include_inactive=False):
        return [self.get(id, include_inactive) for id in id_list]
    
    def update(self, id, include_inactives=False, **kwargs):
        """Actualiza una instancia en la base de datos con los valores especificados.

        Args:
            id (int): Identificador de la instancia.
            include_inactive (bool): Incluir elementos borrados logicamente, default to False
            **kwargs: Valores a actualizar.

        Returns:
            any: Instancia actualizada en la base de datos.
        """
        self.validate_update(id, **kwargs)
        return self.database.update(id, include_inactives, **kwargs)

    def remove(self, id):
        """Elimina una instancia de la base de datos con el identificador especificado.

        Args:
            id (int): Identificador de la instancia.

        Returns:
            any: Instancia eliminada de la base de datos.
        """
        return self.database.remove(id)

    def get_paginator(self, query, page=1):
        """Obtiene un paginador de una consulta.

        Args:
            query (Query): Consulta a paginar.
            page (int, optional): Página a obtener. Defaults to 1.

        Returns:
            Paginator: Paginador de la consulta.
        """
        return query.paginate(per_page=self.rows_per_page, page=page)

    def get_list(self, query):
        """Obtiene una lista de elementos de la base de datos.

        Args:
            query (Query): Consulta para obtener los elementos.

        Returns:
            list: Lista de elementos de la base de datos.
        """
        return query.all()

    def filter_by(self, *args, **kwargs):
        """Filtra una consulta por los argumentos especificados.

        Args:
            *args: Argumentos para filtrar la consulta.
            **kwargs: Argumentos para filtrar la consulta.

        Returns:
            Query: Consulta filtrada.
        """
        return self.database.filter_by(*args, **kwargs)

    def filter_by_get_paginator(self, page, *args, **kwargs):
        """Filtra una consulta por los argumentos especificados y obtiene un paginador.

        Args:
            page (int): Página a obtener.
            *args: Argumentos para filtrar la consulta.
            **kwargs: Argumentos para filtrar la consulta.

        Returns:
            Paginator: Paginador de la consulta.
        """
        return self.get_paginator(self.filter_by(*args, **kwargs), page)

    def filter_by_get_list(self, *args, **kwargs):
        """Filtra una consulta por los argumentos especificados y obtiene una lista.

        Args:
            *args: Argumentos para filtrar la consulta.
            **kwargs: Argumentos para filtrar la consulta.

        Returns:
            list: Lista de elementos de la base de datos.
        """
        return self.get_list(self.filter_by(*args, **kwargs))

    def filter(self, *args):
        """Filtra una consulta por los argumentos especificados.

        Args:
            *args: Argumentos para filtrar la consulta.

        Returns:
            Query: Consulta filtrada.
        """
        return self.database.filter(*args)

    def filter_get_paginator(self, page, *args):
        """Filtra una consulta por los argumentos especificados y obtiene un paginador.

        Args:
            page (int): Página a obtener.
            *args: Argumentos para filtrar la consulta.

        Returns:
            Paginator: Paginador de la consulta.
        """
        return self.get_paginator(self.filter(*args), page)

    def filter_get_list(self, *args):
        """Filtra una consulta por los argumentos especificados y obtiene una lista.

        Args:
            *args: Argumentos para filtrar la consulta.

        Returns:
            list: Lista de elementos de la base de datos.
        """
        return self.get_list(self.filter(*args))

    def exists(self, id, include_inactive=False):
        query = self.database.query_for(id, include_inactive)
        return self.database.exists(query)
