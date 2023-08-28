import pytest
from src.web import create_app
from src.core.business.config_manager import ConfigManager
from src.core.business.associate_manager import AssociateAuthManager
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)
from src.core.database.auth import Associate
from src.core.database.db_instance import db


app = create_app(env="testing")    # Obtener una instancia de la aplicación
app.testing = True                 # Indicarle funcionar en modo de pruebas
client = app.test_client()         # Solicitarle un mock-client

# Crear gestores de las entidades del sistema
config_m = ConfigManager()
auth_m = AssociateAuthManager()
physical_m = PhysicalResourceManager(db.session, Associate)


@pytest.fixture
def db_club_info():
    with app.app_context():
        new_values = {
            "club_email": "a@b.com",
            "phone_number": "1234"
        }
        
        # Actualizar el correo electrónico y el número de teléfono del Club
        config_m.update(**new_values)

        # Enviarlos al llamador
        yield new_values

        # Luego de la prueba, deshacer los cambios en la BD
        config_m.update(
            club_email="clubdeportivovillaelisa@gmail.com",
            phone_number="02214870193"
        )


@pytest.fixture
def db_login():
    with app.app_context():
        # Crear un nuevo socio
        associate = auth_m.create(
            first_name="John",
            last_name="Doe",
            doc_type="DNI",
            doc_number="12345678",
            email="johndoe@example.com",
            genre="M",
            home_address="Calle Falsa 123",
            phone_number="231124142",
            password="12345678",
        )

        # Enviarlo al llamador
        yield associate

        # Luego de la prueba, borrarlo de la BD
        physical_m.remove(associate.id)

        
@pytest.fixture
def db_token(db_login):
    # Obtener y retornar el token JWT del socio
    return auth_m.token_of(db_login)


def data_of(response, convert_json):
    # Si no hay que convertir los datos a JSON, retornarlos
    if not convert_json:
        return response.data
    
    # Verificar que los datos de la respuesta sean un JSON válido
    json = response.get_json(silent=True)
    assert json is not None
    
    # Si no hay errores, retornarlos
    return json
        
        
def template_api_test(send_request, expected_data = {}, expected_objects = [], expected_status = 200):
    # Verificar parámetros de la función
    if expected_data and expected_objects:
        raise ValueError("Usar sólamente expected_data o expected_objects")
    
    # Hacer la solicitud HTTP y obtener la respuesta
    response = send_request()
    
    # Verificar que el código de estado sea el esperado
    assert response.status_code == expected_status
    
    # Si hay múltiples objetos esperados, o los datos esperados son un
    # diccionario o lista, convertir los contenidos en la respesta a JSON.
    # Sino, usar los originales
    data = data_of(response,
        expected_objects or
        isinstance(expected_data, (dict, list))
    )
    
    # Si hay un único objeto esperado, guardarlo en una lista
    if expected_data and not expected_objects:
        expected_objects = [expected_data]
    
    # Verificar que los datos recibidos sean iguales a los esperados
    assert data in expected_objects
    

def test_club_info(db_club_info):
    # Caso 1 de 1: Datos obtenidos satisfactoriamente
    template_api_test(
        lambda: client.get("/api/club/info"),
        {
            "global_success": [""],
            "email": db_club_info.get("club_email"),
            "phone": db_club_info.get("phone_number")
        }
    )


def test_profile(db_login, db_token):
    path = "/api/me/profile"
    
    unauthenticated = {
        "expected_data": {
            "field_errors": {},
            "global_errors": ["El socio no tiene una sesión iniciada"]
        },
        "expected_status": 401
    }
    
    
    # Caso 1 de 3: Datos obtenidos satisfactoriamente
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "associate": {
                "user": db_login.full_name,
                "email": db_login.email,
                "document_type": db_login.doc_type,
                "document_number": db_login.doc_number,
                "gender": db_login.genre,
                "address": db_login.home_address,
                "phone": db_login.phone_number,
            },
            "global_success": [""],
        }
    )
    
    # Caso 2 de 3: Token inválido
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": "Bearer 1234"}
        ),
        **unauthenticated
    )
    
    # Caso 3 de 3: Sin token
    template_api_test(
        lambda: client.get(path),
        **unauthenticated
    )


def test_login(db_login, db_token):
    path = "/api/login/"
    password = "12345678"
    
    # Función que permite generar objetos esperados, teniendo en cuenta las
    # posibles permutaciones dentro de un conjunto de claves JSON
    def generate_expected(*keys):
        return {
            "field_errors": {},
            "global_errors": [
                "El JSON debe contener las claves {'user', 'password'}, " +
                f"pero tiene {{{', '.join(keys)}}}""
            ]
        }
    
    
    # Caso 1 de 4: Sesión iniciada correctamente
    template_api_test(
        lambda: client.post(
            path,
            json={"user": db_login.email, "password": password}
        ),
        {
            "global_success": ["La sesión ha sido iniciada correctamente"],
            "token": db_token
        }
    )
    
    # Caso 2 de 4: Credenciales inválidas
    template_api_test(
        lambda: client.post(
            path,
            json={"user": db_login.email, "password": "1234"}
        ),
        {
            "field_errors": {},
            "global_errors": ["Credenciales inválidas"]
        },
        expected_status=401
    )
    
    # Caso 3 de 4: Claves inválidas
    template_api_test(
        lambda: client.post(
            path,
            json={"usuario": db_login.email, "contraseña": password}
        ),
        expected_objects = [
            generate_expected("user", "password"),
            generate_expected("password", "user")
        ],
        expected_status=400
    )
    
    # Caso 4 de 4: JSON inválido
    template_api_test(
        lambda: client.post(
            path,
            data=f'{{"user": {db_login.email}'
        ),
        {
            "field_errors": {},
            "global_errors": ["JSON inválido, o sin Content-Type"]
        },
        expected_status=400
    )
