from src.core.business.account_manager import AccountManager
from src.core.database.auth import User
from flask import session, abort
import functools
import re


"""Capa de negocio de alto nivel, para la tabla de Usuarios de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class UserManager(AccountManager):
    def __init__(self):
        """Constructor de la clase UserManager."""
        super().__init__(User)

    def has_role(self, user_id, role_name):
        """Verifica si un usuario tiene un rol.

        Args:
            user_id (int): Identificador del usuario.
            role_name (str): Nombre del rol.

        Returns:
            bool: True si tiene el rol, False en caso contrario.
        """
        return self.database.has_role(user_id, role_name)

    def set_state(self, user_id, active):
        """Activa o desactiva un usuario.

        Args:
            user_id (int): Identificador del usuario.
            active (bool): Nuevo estado del usuario

        Raises:
            ValueError: Si el usuario no existe.
        """
        if not active and (self.has_role(user_id, "Administrador")):
            raise ValueError(f"El usuario es Administrador, no puede bloquearse")

        def toggle_user_active(user):
            user.active = active

        query = self.database.query_for(user_id, True)
        self.database.for_each(query, toggle_user_active)

    def current_user_has_role(self, role_name):
        """Verifica si el usuario actual tiene un rol.

        Args:
            role_name (str): Nombre del rol.

        Returns:
            bool: True si tiene el rol, False en caso contrario.
        """
        return self.has_role(self.current_id(), role_name)

    def set_roles(self, user_id, role_list):
        """Asigna los roles a un usuario.

        Args:
            user_id (int): Identificador del usuario.

        Raises:
            ValueError: Si el usuario no existe.
        """
        if not role_list:
            raise ValueError("Role list is empty")

        def set_user_roles(user):
            user.roles = role_list

        query = self.database.query_for(user_id, True)
        # true es para q anden los q estan bloqueados tmb,
        # que son los que tomamos como baja logica
        self.database.for_each(query, set_user_roles)

    def filter_like_get_paginator(self, email, active, page):
        if re.match(r"\d+", page):
            return self.get_paginator(self.filter_like(email, active), int(page))
        else:
            return self.get_paginator(self.filter_like(email, active), 1)

    def filter_like(self, email, active):
        query = self.database.query(True)
        if email is not None:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if active is not None and active.lower() in ["true", "false"]:
            query = query.filter(User.active == active)
        return query

    def current_id(self):
        return session.get("id")

    def current_user(self):
        """Obtiene el usuario actual.

        Returns:
            User: Usuario actual.
        """
        if not "id" in session:
            return None

        user_id = self.current_id()

        if not self.database.exists(user_id):
            return None

        return self.get(user_id)

    def validate(self, **kwargs):
        super().validate(**kwargs)
        if "username" in kwargs:
            search = self.database.filter_by(True, username=kwargs["username"]).first()
            if (search is not None) and (search.username == kwargs["username"]):
                raise ValueError(f"El usuario {search.username} ya esta en uso.")

    def validate_update(self, id, **kwargs):
        super().validate_update(id, **kwargs)
        if "username" in kwargs:
            search = self.database.filter_by(True, username=kwargs["username"]).first()
            if (
                (search is not None)
                and (search.username == kwargs["username"])
                and (search.id != id)
            ):
                raise ValueError(f"El usuario {search.username} ya esta en uso.")


"""Capa de negocio de alto nivel, para la tabla de Usuarios de la BD, donde se requiere hacer CRUDs sobre sus tuplas, y manejar autenticación, sesiones y permisos."""
class AuthManager(UserManager):
    def has_permission(self, user_id, permit_name):
        """Verifica si un usuario tiene un permiso.

        Args:
            user_id (int): Identificador del usuario.
            permit_name (str): Nombre del permi

        Returns:
            bool: True si tiene el permiso, False en caso contrario.
        """
        return self.database.has_permission(user_id, permit_name)

    def current_user_has_permission(self, permit_name):
        """Verifica si el usuario actual tiene un permiso.

        Args:
            permit_name (str): Nombre del permiso.

        Returns:
            bool: True si tiene el permiso, False en caso contrario.
        """
        return self.has_permission(self.current_id(), permit_name)

    def permission_required(self, permit_name, login_required=True):
        """Verifica si el usuario está logueado y tiene un permiso.

        Args:
            permit_name (str): Nombre del permiso.
            login_required (bool, optional): Si es True, se verifica que el usuario esté logueado. Defaults to True.
        """

        def decorator(func):
            """Recibe una función y la retorna con la validación de permisos.
            Args:
                func (function): Función a validar.

            Returns:
                any: Resultado de la función.
            """

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                """Verifica si el usuario está logueado y tiene un permiso.

                Returns:
                    any: Resultado de la función.
                """
                if login_required and not "id" in session:
                    abort(401)

                if not self.has_permission(self.current_id(), permit_name):
                    abort(403)

                return func(*args, **kwargs)

            return wrapper

        return decorator


auth_m = AuthManager()
