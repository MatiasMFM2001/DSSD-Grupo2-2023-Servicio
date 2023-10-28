import pytest
from src.core.business.user_manager import auth_m
from src.core.business.material_manager import MaterialManager
from tests import app, client, template_api_test, db_login, db_token

materials_m = MaterialManager()

def test_create(db_token):
    path = "/api/materials/create"
    
    
    # Caso 1: Material creado correctamente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "name": "Test",
                "price": 100,
                "short_unit": "v"
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "global_success": ["Material creado correctamente"]
        }
    )
    
    # Caso 2: Material duplicado
    template_api_test(
        lambda: client.post(
            path,
            json={
                "name": "Test",
                "price": 100,
                "short_unit": "v"
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "field_errors": {},
            "global_errors": ["El nombre de material 'Test' ya está en uso."]
        },
        expected_status=400
    )
    
    #materials_m.remove()