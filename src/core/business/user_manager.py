from src.core.business.account_manager import AccountManager
from src.core.database.auth import User
from src.api.helpers.jwt_helpers import try_decode, encode
from src.api.helpers.api_responses import SimpleErrorResponse
from flask import request
import functools
import re
from typing import Optional


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
    def token_of(self, user) -> str:
        return encode(id=user.id)

    def current_token(self) -> Optional[str]:
        full_header = request.headers.get("Authorization", "")
        header_args = full_header.split(" ")

        if len(header_args) != 2:
            return None

        auth_type = header_args[0]
        auth_credentials = header_args[1]

        if auth_type != "Bearer":
            return None

        return auth_credentials

    def current_id(self) -> Optional[int]:
        token = self.current_token()

        if token is None:
            return None

        return try_decode(token).get("id")

    def current_user(self) -> Optional[User]:
        user_id = self.current_id()

        if user_id is None:
            return None

        return self.database.get(user_id)
    
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

    def is_current_logged_in(self) -> bool:
        user_id = self.current_id()

        if user_id is None:
            return False

        return self.database.exists(user_id)
    
    def permission_required(self, permit_name, login_required=True, call_with_current_user=False):
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
                if login_required and not self.is_current_logged_in():
                    return SimpleErrorResponse(
                        401, "El usuario no tiene una sesión iniciada"
                    )

                if not self.has_permission(self.current_id(), permit_name):
                    return SimpleErrorResponse(
                        403, f"El usuario no tiene el permiso {permit_name}"
                    )

                if not call_with_current_user:
                    return func(*args, **kwargs)

                return func(self.current_user(), *args, **kwargs)

            return wrapper

        return decorator


auth_m = AuthManager()
