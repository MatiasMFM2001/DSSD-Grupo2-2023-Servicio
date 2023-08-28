from src.core.business.crud_manager import CRUDManager
from src.core.database.board import Service, Discipline, Membership
import re


"""Capa de negocio de alto nivel base, para la tabla de Disciplinas o Membresías de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class ServiceManager(CRUDManager):
    def __init__(self, table=Service):
        """Constructor de la clase ServiceManager.

        Args:
            table (Service, optional): Tabla de la base de datos. Defaults to Service.
        """
        super().__init__(table)


"""Capa de negocio de alto nivel, para la tabla de Disciplinas de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class DisciplineManager(ServiceManager):
    def __init__(self):
        """Constructor de la clase DisciplineManager."""
        super().__init__(Discipline)

    def filter_like_get_paginator(self, name, active, page):
        if re.match(r"\d+", page):
            return self.get_paginator(self.filter_like(name, active), int(page))
        else:
            return self.get_paginator(self.filter_like(name, active), 1)

    def filter_like(self, name, active):
        query = self.database.query(True)
        if name is not None:
            query = query.filter(Discipline.name.ilike(f"%{name}%"))
        if active is not None and active.lower() in ["true", "false"]:
            query = query.filter(Discipline.active == active)
        return query

    def set_categories(self, discipline_id, categories_list):
        if not categories_list:
            raise ValueError("Categories list is empty")

        def set_discipline_categories(discipline):
            discipline.categories = categories_list

        query = self.database.query_for(discipline_id, True)
        # true es para q anden los q estan bloqueados tmb,
        # que son los que tomamos como baja logica
        self.database.for_each(query, set_discipline_categories)

    def set_state(self, discipline_id, active):
        def toggle_discipline_active(discipline):
            discipline.active = active

        query = self.database.query_for(discipline_id, True)
        self.database.for_each(query, toggle_discipline_active)


"""Capa de negocio de alto nivel, para la tabla de Membresías de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class MembershipManager(ServiceManager):
    def __init__(self):
        """Constructor de la clase MembershipManager."""
        super().__init__(Membership)

    def get_by_name(self, name):
        """Obtiene un servicio por su nombre.

        Args:
            name (str): Nombre del servicio.

        Returns:
            Service: Servicio.
        """
        return self.database.filter(False, Membership.name.ilike(f"%{name}%")).one()

    def update_by_name(self, name, **kwargs):
        """Actualiza un servicio por su nombre.

        Args:
            name (str): Nombre del servicio.
        """
        query = self.database.filter(False, Membership.name.ilike(f"%{name}%"))
        self.database.update_each(query, **kwargs)
