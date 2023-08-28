from re import A
from src.core.database.db_instance import db
import src.core.database.custom_drop_table
from datetime import date

from src.core.database.auth import Permission, Role, User, Associate
from src.core.database.board import (
    Category,
    Discipline,
    Cuote,
    Configuration,
    Membership,
)
from src.core.business.associate_manager import AssociateManager

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
associate_rm = Associate.resource_manager()
category_rm = Category.resource_manager()
discipline_rm = Discipline.resource_manager()
membership_rm = Membership.resource_manager()
cuote_rm = Cuote.resource_manager()
config_rm = Configuration.resource_manager()

associate_m = AssociateManager


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

    membership_base = membership_rm.create(name="Base", mensual_cost=100.0)

    user2 = associate_rm.create(  # auth.Associate
        email="user2@a.com",
        password="5678",
        first_name="Socio",
        last_name="Numero 2",
        doc_type="DNI",
        doc_number=12345678,
        genre="Otro",
        home_address="1 y 60",
        phone_number="0221 342-6675",
        services=[membership_base],
    )

    user1.roles.append(role_admin)
    role_admin.permissions.append(perm_member_index)

    cat_futbol = category_rm.create(name="Fútbol")  # board.Category

    dis_futbol_5 = discipline_rm.create(  # board.Discipline
        name="Fútbol 5",
        teacher="Santiago, Catalina",
        shedule_time="Lunes y Viernes, 8:00 a 12:00",
        mensual_cost=546.23,
        categories=[cat_futbol],
        associates=[user2],
    )

    cuote1 = cuote_rm.create(
        price=200,
        associate=user2,
        service=dis_futbol_5,
        paid_date=date.today(),
        expiration_date=date.fromisoformat("2023-12-04"),
        # cuote_number=3
    )

    cuote2 = cuote_rm.create(
        price=200,
        associate=user2,
        service=dis_futbol_5,
        expiration_date=date.fromisoformat("2023-12-04"),
        # cuote_number=3
    )

    config_rm.update(rows_per_page=20)
    config_rm.update(rows_per_page=15)
    config_rm.update(rows_per_page=10)


def list_db():
    """Lista los datos de la base de datos."""
    print(role_rm.get(1))
    print(permission_rm.get(1))
    print(user_rm.get(1))
    print(associate_rm.get(1))
    print(category_rm.get(1))
    print(discipline_rm.get(1))
    print(cuote_rm.get(1))
    print(config_rm.get(None))


def delete_db():
    """Elimina los datos de la base de datos."""
    print(role_rm.remove(1))
    print(permission_rm.remove(1))
    print(user_rm.remove(1))
    print(associate_rm.remove(1))
    print(category_rm.remove(1))
    print(discipline_rm.remove(1))
    print(cuote_rm.remove(1))
    print(config_rm.remove(None))


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

    # Memberships
    membership_base = membership_rm.create(name="Base", mensual_cost=100.0)

    # Categories
    category_football = category_rm.create(name="Fútbol")
    category_volley = category_rm.create(name="Vóley")
    category_rugby = category_rm.create(name="Rugby")
    category_basket = category_rm.create(name="Básquet")

    # Disciplines
    discipline_1 = discipline_rm.create(
        name="Fútbol 11",
        teacher="Santiago, Catalina",
        schedule_time="Lunes y Viernes, 8:00 a 12:00",
        mensual_cost=546.23,
        categories=[category_football],
    )

    discipline_2 = discipline_rm.create(
        name="Volley",
        teacher="Santiago, Catalina",
        schedule_time="Lunes y Jueves, 8:00 a 12:00",
        mensual_cost=546.23,
        categories=[category_volley],
    )

    discipline_3 = discipline_rm.create(
        name="Rugby profesional",
        teacher="Santiago, Catalina",
        schedule_time="Lunes, 8:00 a 12:00",
        mensual_cost=546.23,
        categories=[category_rugby],
    )

    discipline_4 = discipline_rm.create(
        name="Fútbol infantil",
        teacher="Marcela, Muñoz",
        schedule_time="Martes y Viernes, 8:00 a 12:00",
        mensual_cost=546.23,
        categories=[category_football],
    )

    user3 = associate_rm.create(  # auth.Associate
        email="er2@a.com",
        password="1234",
        first_name="Sio",
        last_name="Nro 2",
        doc_type="DNI",
        doc_number=12345678,
        genre="Otro",
        home_address="1 y 60",
        phone_number="0221 342-6675",
        services=[membership_base],
    )
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

    # Associates
    associate_1 = associate_rm.create(
        first_name="Juan",
        last_name="Perez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="juanpereza@gmail.com",
        password="1234",
    )

    associate_2 = associate_rm.create(
        first_name="Maria",
        last_name="Gonzalez",
        doc_type="DNI",
        doc_number=87654321,
        genre="F",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="maria@gmail.com",
        password="1234",
        services=[
            membership_base,
            discipline_1,
            discipline_2,
            discipline_3,
            discipline_4,
        ],
    )

    associate_3 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio3@gmail.com",
        password="1234",
        services=[membership_base],
    )

    associate_4 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio4@gmail.com",
        password="1234",
        services=[membership_base],
    )
    associate_5 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio5@gmail.com",
        password="1234",
        services=[membership_base],
    )

    associate_6 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio6@gmail.com",
        password="1234",
        services=[membership_base],
    )

    associate_7 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio7@gmail.com",
        password="1234",
        services=[membership_base],
    )

    associate_8 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio8@gmail.com",
        password="1234",
        services=[membership_base],
    )
    associate_9 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio9@gmail.com",
        password="1234",
        services=[membership_base],
    )
    associate_10 = associate_rm.create(
        first_name="Pedro",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio10@gmail.com",
        password="1234",
        services=[membership_base],
    )
    associate_11 = associate_rm.create(
        first_name="Marcos",
        last_name="Rodriguez",
        doc_type="DNI",
        doc_number=12345678,
        genre="M",
        home_address="Calle Falsa 123",
        phone_number="123456789",
        email="socio11@gmail.com",
        password="1234",
        services=[membership_base],
    )

    print("Finished initializing BD")
