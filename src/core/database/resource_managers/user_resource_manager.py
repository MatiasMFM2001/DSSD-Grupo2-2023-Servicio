from src.core.database.resource_managers.account_resource_manager import (
    AccountResourceManager,
)
from src.core.database.auth.role import Role
from src.core.database.auth.permission import Permission

role_rm = Role.resource_manager()


"""Abstracción de accesos a la tabla de Usuarios de la BD, donde se realizan bajas lógicas."""
class UserResourceManager(AccountResourceManager):
    def get_permissions(self, user_id):
        roles = role_rm.filter_by(name="No autenticado")

        if user_id is not None:
            roles = self.query_for(user_id).join(self.model_class.roles)

        return roles.join(Role.permissions)

    def has_role(self, user_id, role_name):
        if user_id is None:
            return role_name == "No autenticado"

        query = (
            self.query_for(user_id)
            .join(self.model_class.roles)
            .filter(Role.name == role_name)
        )

        return self.exists(query)

    def has_permission(self, user_id, permit_name, role_name=""):
        if permit_name is None:
            return False

        query = self.get_permissions(user_id).filter(Permission.name == permit_name)

        return self.exists(query)
