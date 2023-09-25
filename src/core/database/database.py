from re import A
from src.core.database.db_instance import db
import src.core.database.custom_drop_table
from datetime import date

from src.core.database.auth import *
from src.core.database.board import *

def init_app(app):
    """
    Registra las funciones de inicialización de la base de datos en la aplicación Flask.

    Args:
        app (Flask): Aplicación Flask.
    """
    db.init_app(app)


def config_db(app):
    """Configura la base de datos para la aplicación Flask.

    Args:
        app (Flask): Aplicación Flask.
    """

    @app.before_first_request
    def init_db():
        """Inicializa la base de datos."""
        db.create_app()

    @app.teardown_request
    def close_sesion(exception=None):
        """Cierra la sesión de la base de datos."""
        db.session.remove()


def reset_db():
    """Resetea la base de datos."""
    print("Reseting database")
    db.drop_all()
    print("Creating tables")
    db.create_all()
    print("Reset finished")


permission_rm = Permission.resource_manager()
role_rm = Role.resource_manager()
user_rm = User.resource_manager()


def populate_db():
    """Crea datos de prueba en la base de datos."""
    role_admin = role_rm.create(name="Administrador")  # auth.Role
    role_operario = role_rm.create(name="Operario")  # auth.Role

    perm_member_index = permission_rm.create(name="member_index")  # auth.permission

    user1 = user_rm.create(  # auth.User
        email="user1@a.com",
        username="user1",
        password="1234",
        first_name="Usuario",
        last_name="Numero 1",
    )

    user1.roles.append(role_admin)
    role_admin.permissions.append(perm_member_index)

    

def list_db():
    """Lista los datos de la base de datos."""
    print(role_rm.get(1))
    print(permission_rm.get(1))
    print(user_rm.get(1))


def delete_db():
    """Elimina los datos de la base de datos."""
    print(role_rm.remove(1))
    print(permission_rm.remove(1))
    print(user_rm.remove(1))


def db_test_everything():
    """Ejecuta todas las funciones de prueba de la base de datos."""
    reset_db()
    populate_db()
    list_db()
    # delete_db()


def initializate_prod_db():
    """Inicializa la base de datos para producción."""
    print("Started initializing BD")
    db.create_all()
    print("Finished resetting BD")

   
    # Permissions
    action_modules = {
        "login": ["private"],
        "logout": ["private"],
        "list": ["user", "associate", "discipline", "payment"],
        "show": ["associate", "discipline", "home"],
        "update": ["config", "user", "associate", "discipline", "payment"],
        "export": ["associate", "payment"],
        "create": ["user", "associate", "discipline", "payment"],
        "destroy": ["user", "associate", "discipline", "payment"],
        "inscribe_discipline": ["associate"],
        "unscribe_discipline": ["associate"],
    }

    name_permissions = {}

    for action, modules in action_modules.items():
        for module in modules:
            role_name = f"{module}_{action}"
            name_permissions[role_name] = permission_rm.create(name=role_name)

    # Roles and its permissions
    role_admin = role_rm.create(name="Administrador")
    role_operator = role_rm.create(name="Operador")
    null_role = role_rm.create(name="No autenticado")

    operator_has_not_permissions = {
        "private_login",
        "config_update",
        "user_list",
        "user_create",
        "user_update",
        "user_destroy",
        "associate_create",
    }

    role_has_permissions = {
        role_admin: name_permissions.keys() - {"private_login"},
        null_role: ["private_login"],
        role_operator: [
            p
            for p in name_permissions.keys()
            if not "destroy" in p and p not in operator_has_not_permissions
        ],
    }

    for role, permissions in role_has_permissions.items():
        for permission in permissions:
            role.permissions.append(name_permissions[permission])

    # Users
    admin = user_rm.create(
        email="admin@a.com",
        username="admin",
        password="1234",
        first_name="Admin",
        last_name="Numero 1",
        roles=[role_admin],
    )

    operator = user_rm.create(
        email="operador@a.com",
        username="operador",
        password="1234",
        first_name="Operador",
        last_name="Numero 1",
        roles=[role_operator],
    )

    print("Finished initializing BD")
