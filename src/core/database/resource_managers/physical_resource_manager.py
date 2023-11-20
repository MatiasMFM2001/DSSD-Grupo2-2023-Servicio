from sqlalchemy.sql.elements import BinaryExpression

"""Abstracción de accesos a una tabla de la BD, donde se realizan bajas físicas."""
class PhysicalResourceManager:
    def __init__(self, dbsession, model_class, instantiator=None):
        """Constructor de PhysicalResourceManager.

        Args:
            dbsession (Session): Sesión de la base de datos.
            model_class (Model): Clase del modelo.
            instantiator (function, optional): Función para instanciar el modelo. Defaults to None.
        """
        self.dbs = dbsession
        self.model_class = model_class
        self.instantiator = instantiator or model_class

    def query(self, model_class=None):
        """Retorna la query para obtener una instancia de este modelo.

        Returns:
            Query: Query para obtener una instancia de este modelo.
        """
        return self.dbs.query(model_class or self.model_class)

    def filter(self, model_class=None, *predicates):
        """Retorna la query para obtener instancias de este modelo que cumplan con los predicados dados.

        Returns:
            Query: Query para obtener instancias de este modelo que cumplan con los predicados dados.
        """
        if isinstance(model_class, BinaryExpression):
            return self.filter(None, model_class, *predicates)
        
        return self.query(model_class).filter(*predicates)

    def filter_by(self, model_class=None, **kwargs):
        """Retorna la query para obtener instancias de este modelo que cumplan con los criterios dados.

        Returns:
            Query: Query para obtener instancias de este modelo que cumplan con los criterios dados.
        """
        return self.query(model_class).filter_by(**kwargs)

    def query_for(self, id, include_inactives=False, model_class=None):
        """Retorna la query para obtener una instancia de este modelo con el identificador dado.

        Args:
            id (int): Identificador de la instancia.

        Returns:
            Query: Query para obtener una instancia de este modelo con el identificador dado.
        """
        return self.filter_by(model_class, id=id)

    def commit(self):
        """Realiza el commit de la sesión de la base de datos."""
        self.dbs.commit()

    def add(self, obj):
        """Agrega un objeto a la sesión de la base de datos.

        Args:
            obj (Model): Objeto a agregar.
        """
        self.dbs.add(obj)
        self.commit()

    def create(self, **kwargs):
        """Crea una instancia de este modelo.

        Returns:
            Model: Instancia de este modelo.
        """
        created = self.instantiator(**kwargs)
        self.add(created)

        return created

    def get(self, id, include_inactives=False, model_class=None):
        """Retorna una instancia de este modelo con el identificador dado.

        Args:
            id (int): Identificador de la instancia.

        Returns:
            Model: Instancia de este modelo con el identificador dado.
        """
        return self.query_for(id, include_inactives, model_class).one()

    def get_all(self, id_list, include_inactives=False, model_class=None):
        return [self.get(id, include_inactives, model_class) for id in id_list]
    
    def for_each(self, query, function):
        """Ejecuta la función dada para cada elemento de la query dada.

        Args:
            query (Query): Query para obtener los elementos.
            function (function): Función a ejecutar.
        """
        for item in query.all():
            function(item)

        self.commit()

    def update_each(self, query, **kwargs):
        """Actualiza los elementos de la query dada con los argumentos dados.

        Args:
            query (Query): Query para obtener los elementos.
        """
        query.update(kwargs, synchronize_session="fetch")
        self.commit()

    def remove_each(self, query):
        """Elimina los elementos de la query dada.

        Args:
            query (Query): Query para obtener los elementos.
        """
        self.for_each(query, self.dbs.delete)

    def exists(self, query, include_inactives=False, model_class=None):
        """Retorna si existe al menos un elemento en la query dada.

        Args:
            query (Query): Query para obtener los elementos.

        Returns:
            bool: True si existe al menos un elemento en la query dada, False en caso contrario.
        """
        if type(query) == int:
            query = self.query_for(query, include_inactives, model_class)

        return query.first() is not None

    def exists_all(self, id_list, include_inactives=False, model_class=None):
        return {
            id: self.exists(id, include_inactives, model_class) 
            for id in id_list
        }
    
    def update(self, id, include_inactives=False, **kwargs):
        """Actualiza una instancia de este modelo con el identificador dado.

        Args:
            id (int): Identificador de la instancia.
        """
        self.update_each(self.query_for(id), **kwargs)

    def remove(self, id, include_inactives=False):
        """Elimina una instancia de este modelo con el identificador dado.

        Args:
            id (int): Identificador de la instancia.
        """
        self.remove_each(self.query_for(id))
