import pytest
from src.service import create_app
from src.core.database.db_instance import db
from src.core.business.user_manager import auth_m


app = create_app(env="testing")    # Obtener una instancia de la aplicación
app.testing = True                 # Indicarle funcionar en modo de pruebas
client = app.test_client()         # Solicitarle un mock-client


@pytest.fixture
def db_login():
    with app.app_context():
        return auth_m.filter_by_get_list(username="admin")[0]

        
@pytest.fixture
def db_token(db_login):
    with app.app_context():
        # Obtener y retornar el token JWT del usuario
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
        
        
def template_api_test(
    send_request,
    expected_data = {},
    expected_objects = [],
    expected_status = 200
):
    # Verificar parámetros de la función
    if expected_data and expected_objects:
        raise ValueError("Usar sólamente expected_data o expected_objects")
    
    # Hacer la solicitud HTTP y obtener la respuesta
    response = send_request()
    
    #print(response.status_code, expected_status)
    # Verificar que el código de estado sea el esperado
    assert response.status_code == expected_status
    
    # Si hay múltiples objetos esperados, o los datos esperados son un
    # diccionario o lista, convertir los contenidos en la respesta a JSON.
    # Sino, usar los originales
    data = data_of(response,
        expected_objects or
        isinstance(expected_data, (dict, list))
    )
    print(data)
    # Si hay un único objeto esperado, guardarlo en una lista
    if expected_data and not expected_objects:
        expected_objects = [expected_data]
    
    # Verificar que los datos recibidos sean iguales a los esperados
    assert data in expected_objects