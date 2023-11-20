import pytest
from src.core.business.user_manager import auth_m
from tests import app, client, template_api_test, db_login, db_token

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
    
def test_all(db_token):
    # Caso 1: Lista obtenida
    template_api_test(
        lambda: client.get(
            "/api/materials/all",
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "global_success": [""],
            "materials": [
                {
                    "id": 1,
                    "name": "Madera",
                    "price": 465.2,
                    "short_unit": "unit"
                },
                {
                    "id": 2,
                    "name": "Metal",
                    "price": 1200.3,
                    "short_unit": "unit"
                },
                {
                    "id": 3,
                    "name": "Melamina",
                    "price": 2015.9,
                    "short_unit": "unit"
                },
                {
                    "id": 4,
                    "name": "Plástico",
                    "price": 800.0,
                    "short_unit": "unit"
                },
                {
                    "id": 5,
                    "name": "Vidrio",
                    "price": 1500.75,
                    "short_unit": "unit"
                },
                {
                    "id": 6,
                    "name": "Cerámica",
                    "price": 120.5,
                    "short_unit":
                    "unit"
                }, 
                {
                    "id": 7,
                    "name": "Test",
                    "price": 100.0,
                    "short_unit": "v"
                }
            ]
        }
    )
    
def test_get_by_id(db_token):
    path = "/api/materials/getById"
    
    
    # Caso 1: Objeto encontrado
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 1
            }
        ),
        {
            "global_success": [""],
            "material": {
                "id": 1,
                "name": "Madera",
                "price": 465.2,
                "short_unit": "unit"
            }
        }
    )
    
    # Caso 2: Objeto no encontrado
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 999
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El material de ID 999 no existe"]
        },
        expected_status=404
    )

def test_get_by_name(db_token):
    path = "/api/materials/getByName"
    
    
    # Caso 1: Objeto encontrado
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "name": "Madera"
            }
        ),
        {
            "global_success": [""],
            "material": {
                "id": 1,
                "name": "Madera",
                "price": 465.2,
                "short_unit": "unit"
            }
        }
    )
    
    # Caso 2: Objeto no encontrado
    template_api_test(
        lambda: client.get(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "name": "AGUANTE EL PINCHA"
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El material de nombre AGUANTE EL PINCHA no existe"]
        },
        expected_status=404
    )