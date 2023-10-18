from re import A
from src.core.database.db_instance import db
import src.core.database.custom_drop_table
from datetime import date
import re

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
categ_rm = Category.resource_manager()


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
        
        "list": ["user", "category", "collection", "furniture", "furniture_file", "batch", "furniture_material", "material"],
        "show": ["home", "furniture_file", "collection", "furniture", "batch", "furniture_material"],
        #"update": ["user", "category", "collection", "furniture", "furniture_file", "furniture_material"],
        "create": ["user", "category", "collection", "furniture", "furniture_file", "furniture_material", "material"],
        #"destroy": ["user", "category", "collection", "furniture", "furniture_file"],
        
        "end": ["collection"],
        "sell": ["batch"],
        "receive": ["batch"],
    }

    name_permissions = {}

    for action, modules in action_modules.items():
        for module in modules:
            role_name = f"{module}_{action}"
            name_permissions[role_name] = permission_rm.create(name=role_name)

    # Roles and its permissions
    null_role = role_rm.create(name="No autenticado")
    admin_role = role_rm.create(name="Administrador")
    
    creative_role = role_rm.create(name="Área Creativa")
    operational_role = role_rm.create(name="Área Operativa")
    commercial_role = role_rm.create(name="Área Comercial")

    creative_regex = re.compile(r"^(category)|(collection)|(furniture)_[^_]+$")
    operational_regex = re.compile(r"^(furniture_material)_[^_]+")
    commercial_regex = re.compile(r"^(batch)_[^_]+")
    
    role_has_permissions = {
        admin_role: name_permissions.keys() - {"private_login"},
        null_role: ["private_login"],
        
        creative_role: [
            name for name in name_permissions.keys()
            if creative_regex.match(name)
        ],
        
        operational_role: [
            name for name in name_permissions.keys()
            if operational_regex.match(name)
        ],
        
        commercial_role: [
            name for name in name_permissions.keys()
            if commercial_regex.match(name)
        ],
    }
    
    extra_permissions = {
        commercial_role: [
            "collection_list",
            "collection_show",
            
            "furniture_list",
            "furniture_show",
        ],
    }
    
    for role in [creative_role, operational_role, commercial_role]:
        role.permissions.append(name_permissions["private_logout"])

    for role, permissions in extra_permissions.items():
        role_has_permissions[role].extend(permissions)
    
    for role, permissions in role_has_permissions.items():
        for permission in permissions:
            role.permissions.append(name_permissions[permission])

    # Users
    admin_1 = user_rm.create(
        email="admin@a.com",
        username="admin",
        password="1234",
        first_name="Admin",
        last_name="Numero 1",
        roles=[admin_role],
    )
    
    admin_2 = user_rm.create(
        email="adm@a.com",
        username="admin2",
        password="1234",
        first_name="Admin",
        last_name="Numero 2",
        roles=[admin_role],
    )
    
    creative = user_rm.create(
        email="cre@a.com",
        username="creativo",
        password="1234",
        first_name="Creativo",
        last_name="Numero 1",
        roles=[creative_role],
    )
    
    operational = user_rm.create(
        email="ope@a.com",
        username="operacional",
        password="1234",
        first_name="Operacional",
        last_name="Numero 1",
        roles=[operational_role],
    )
    
    commercial = user_rm.create(
        email="com@a.com",
        username="comercial",
        password="1234",
        first_name="Comercial",
        last_name="Numero 1",
        roles=[commercial_role],
    )

    

    # Category
    category = categ_rm.create(name="Palmeiras New York Enano")

    print("Finished initializing BD")
