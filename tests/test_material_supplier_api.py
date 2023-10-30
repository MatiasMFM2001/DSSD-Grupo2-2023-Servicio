import pytest
from src.core.business.user_manager import auth_m
from tests import app, client, template_api_test, db_login, db_token

def test_create(db_token):
    path = "/api/material_supplier/create"
    
    
    # Caso 1: Material_supplier creado correctamente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "arrival_date": "2024-02-22",
                "stock": 100,
                "material_id": 4,
                "supplier_id": 1
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "global_success": ["Material_supplier creado correctamente"]
        }
    )
    
    # Caso 2: Material_supplier de material no existente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "arrival_date": "2024-02-22",
                "stock": 100,
                "material_id": 999,
                "supplier_id": 1
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "field_errors": {},
            "global_errors": ["El material de ID 999 no existe."]
        },
        expected_status=400
    )
    
    # Caso 3: Material_supplier de proveedor no existente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "arrival_date": "2024-02-22",
                "stock": 100,
                "material_id": 1,
                "supplier_id": 999
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "field_errors": {},
            "global_errors": ["El proveedor de ID 999 no existe."]
        },
        expected_status=400
    )
    
    # Caso 4: Reserva demasiado grande
    #template_api_test(
    #    lambda: client.post(
    #        path,
    #        json={
    #            "arrival_date": "2024-02-22",
    #            "stock": 999,
    #            "material_id": 4,
    #            "supplier_id": 1
    #        },
    #        headers={"Authorization": f"Bearer {db_token}"}
    #    ),
    #    {
    #        "field_errors": {},
    #        "global_errors": ["El productor de ID 999 no existe."]
    #    }
    #)
    
def test_all(db_token):
    # Caso 1: Lista obtenida
    template_api_test(
        lambda: client.get(
            "/api/material_supplier/all",
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "material": 4,
                "arrival_date": "2024-02-27",
                "stock": 20
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": [
                {
                    "id": 4,
                    "arrival_date": "Thu, 22 Feb 2024 00:00:00 GMT",
                    "material_id": 4,
                    "stock": 100,
                    "supplier_id": 1
                }
            ]
        }
    )
    
    # Caso 2: Lista vacía por stock insuficiente
    template_api_test(
        lambda: client.get(
            "/api/material_supplier/all",
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "material": 4,
                "arrival_date": "2024-02-27",
                "stock": 999
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": []
        }
    )
    
    # Caso 3: Lista vacía por no llegar a la fecha pedida
    template_api_test(
        lambda: client.get(
            "/api/material_supplier/all",
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "material": 4,
                "arrival_date": "2024-02-20",
                "stock": 20
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": []
        }
    )
    
    # Caso 3: Lista fallida por material no existente
    template_api_test(
        lambda: client.get(
            "/api/material_supplier/all",
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "material": 999,
                "arrival_date": "2024-02-27",
                "stock": 20
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El material de ID 999 no existe"]
        },
        expected_status=404
    )

def test_reserve(db_token):
    path = "/api/material_supplier/reserve"
    
    
    # Caso 1: Material_supplier reservado correctamente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 4,
            }
        ),
        {
            "global_success": ["Material_supplier reservado correctamente"],
        }
    )
    
    # Caso 2: Material_supplier ya reservado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 4
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El material_supplier de ID 4 ya estaba reservado"]
        },
        expected_status=400
    )
    
    # Caso 3: Material_supplier no encontrado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 999
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El material_supplier de ID 999 no existe"]
        },
        expected_status=404
    )
