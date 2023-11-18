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

producer_rm = Producer.resource_manager()
supplier_rm = Supplier.resource_manager()
material_rm = Material.resource_manager()
material_supplier_rm = MaterialSupplier.resource_manager()
fabrication_slot_rm = FabricationSlot.resource_manager()


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
        "profile_edit": ["private"],
        
        "list": ["user", "category", "collection", "furniture", "furniture_file", "batch", "furniture_material", "material", "slot", "material_supplier", "tick",],
        "show": ["home", "furniture_file", "collection", "furniture", "batch", "furniture_material", "slot", "material", "tick",],
        #"update": ["user", "category", "collection", "furniture", "furniture_file", "furniture_material", "slot", "tick",],
        "create": ["user", "category", "collection", "furniture", "furniture_file", "furniture_material", "material", "slot", "material_supplier", "tick",],
        #"destroy": ["user", "category", "collection", "furniture", "furniture_file", "slot", "tick",],
        
        "end": ["collection"],
        "sell": ["batch"],
        "receive": ["batch"],
        "reserve": ["slot", "material", "material_supplier",]
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

    
    # Proveedores
    supplier1 = supplier_rm.create(
        name="Maderera San Jorge",
        location="Madrid",
    )
    
    supplier2 = supplier_rm.create(
        name="Herrería Hefesto",
        location="Tarragona",
    )
    
    supplier3 = supplier_rm.create(
        name="Melamina de Nina",
        location="Barcelona",
    )
    
    # Fabricantes
    producer1 = producer_rm.create(
        name="Ensambles Don Pepe",
        location="Madrid",
    )
    
    producer2 = producer_rm.create(
        name="Fábrica Fabricio",
        location="Tarragona",
    )
    
    producer3 = producer_rm.create(
        name="Armados Armando",
        location="Barcelona",
    )

    producer4 = producer_rm.create(
        name="Industrias Inés",
        location="Valencia",
    )

    producer5 = producer_rm.create(
        name="Construcciones Carlos",
        location="Sevilla",
    )

    producer6 = producer_rm.create(
        name="Textiles Teresa",
        location="Bilbao",
    )
    
    # Materiales
    material1 = material_rm.create(
        name="Madera",
        price=465.2,
    )
    
    material2 = material_rm.create(
        name="Metal",
        price=1200.3,
    )
    
    material3 = material_rm.create(
        name="Melamina",
        price=2015.9,
    )

    material4 = material_rm.create(
        name="Plástico",
        price=800.0,
    )

    material5 = material_rm.create(
        name="Vidrio",
        price=1500.75,
    )

    material6 = material_rm.create(
        name="Cerámica",
        price=120.5,
    )

    # Many-to-Many entre Materiales y Proveedores
    association1 = material_supplier_rm.create(
        material=material1,
        supplier=supplier1,
        stock=5,
        arrival_date=date(2023, 12, 3),
    )
    
    association2 = material_supplier_rm.create(
        material=material2,
        supplier=supplier2,
        stock=10,
        arrival_date=date(2023, 11, 22),
    )
    
    association3 = material_supplier_rm.create(
        material=material3,
        supplier=supplier3,
        stock=15,
        arrival_date=date(2023, 11, 15),
    )

    association4 = material_supplier_rm.create(
        material=material4,
        supplier=supplier1,
        stock=8,
        arrival_date=date(2023, 12, 10),
    )

    association5 = material_supplier_rm.create(
        material=material5,
        supplier=supplier2,
        stock=12,
        arrival_date=date(2023, 11, 30),
    )

    association6 = material_supplier_rm.create(
        material=material6,
        supplier=supplier3,
        stock=20,
        arrival_date=date(2023, 11, 18),
    )
    
    association7 = material_supplier_rm.create(
        material=material1,
        supplier=supplier2,
        stock=3,
        arrival_date=date(2023, 12, 5),
    )

    association8 = material_supplier_rm.create(
        material=material2,
        supplier=supplier3,
        stock=7,
        arrival_date=date(2023, 12, 8),
    )

    association9 = material_supplier_rm.create(
        material=material3,
        supplier=supplier1,
        stock=10,
        arrival_date=date(2023, 12, 12),
    )

    association10 = material_supplier_rm.create(
        material=material4,
        supplier=supplier2,
        stock=5,
        arrival_date=date(2023, 12, 2),
    )

    association11 = material_supplier_rm.create(
        material=material5,
        supplier=supplier3,
        stock=15,
        arrival_date=date(2023, 12, 7),
    )

    association12 = material_supplier_rm.create(
        material=material6,
        supplier=supplier1,
        stock=18,
        arrival_date=date(2023, 12, 14),
    )

    
    
    # Slots de fabricación
    slot1 = fabrication_slot_rm.create(
        price=82015.9,
        beginning=date(2023, 10, 27),
        end=date(2024, 1, 18),
        producer=producer1,
    )
    
    slot2 = fabrication_slot_rm.create(
        price=92070.0,
        beginning=date(2023, 11, 3),
        end=date(2024, 2, 1),
        producer=producer2,
    )
    
    slot3 = fabrication_slot_rm.create(
        price=55033.5,
        beginning=date(2023, 11, 9),
        end=date(2024, 1, 30),
        producer=producer3,
    )
    
    # Vínculo entre 

    print("Finished initializing BD")
