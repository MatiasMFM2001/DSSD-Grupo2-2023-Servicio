import pytest
from src.core.business.user_manager import auth_m
from src.core.business.fabrication_slot_manager import FabricationSlotManager
from tests import app, client, template_api_test, db_login, db_token

fabrication_slots_m = FabricationSlotManager()

def test_create(db_token):
    path = "/api/slots/create"
    
    
    # Caso 1: Slot creado correctamente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "beginning": "2024-02-22",
                "end": "2024-03-22",
                "price": 100,
                "producer_id": 4
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "global_success": ["Slot creado correctamente"]
        }
    )
    
    # Caso 2: Slot de productor no existente
    template_api_test(
        lambda: client.post(
            path,
            json={
                "beginning": "2024-02-22",
                "end": "2024-03-22",
                "price": 100,
                "producer_id": 999
            },
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "field_errors": {},
            "global_errors": ["El productor de ID 999 no existe."]
        },
        expected_status=400
    )
    
def test_all(db_token):
    # Caso 1: Lista obtenida
    template_api_test(
        lambda: client.get(
            "/api/slots/all",
            headers={"Authorization": f"Bearer {db_token}"}
        ),
        {
            "global_success": [""],
            "slots": [
                {
                    "beginning": "Fri, 27 Oct 2023 00:00:00 GMT",
                    "end": "Thu, 18 Jan 2024 00:00:00 GMT",
                    "id": 1, "price": 82015.9,
                    "producer": {
                        "id": 4,
                        "location": "Madrid",
                        "name": "Ensambles Don Pepe"
                    }
                },
                {
                    "beginning": "Fri, 03 Nov 2023 00:00:00 GMT",
                    "end": "Thu, 01 Feb 2024 00:00:00 GMT",
                    "id": 2, "price": 92070.0,
                    "producer": {
                        "id": 5,
                        "location": "Tarragona",
                        "name": "Fábrica Fabricio"
                    }
                },
                {
                    "beginning": "Thu, 09 Nov 2023 00:00:00 GMT",
                    "end": "Tue, 30 Jan 2024 00:00:00 GMT",
                    "id": 3, "price": 55033.5,
                    "producer": {
                        "id": 6,
                        "location": "Barcelona",
                        "name": "Armados Armando"
                    }
                },
                {
                    "beginning": "Thu, 22 Feb 2024 00:00:00 GMT",
                    "end": "Fri, 22 Mar 2024 00:00:00 GMT",
                    "id": 4, "price": 100.0,
                    "producer": {
                        "id": 4,
                        "location": "Madrid",
                        "name": "Ensambles Don Pepe"
                    }
                }
            ]
        }
    )

def test_get_by_id(db_token):
    path = "/api/slots/get"
    
    
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
            "slot": {
                "beginning": "Fri, 27 Oct 2023 00:00:00 GMT",
                "end": "Thu, 18 Jan 2024 00:00:00 GMT",
                "id": 1,
                "price": 82015.9,
                "producer": {
                    "id": 4,
                    "location": "Madrid",
                    "name": "Ensambles Don Pepe"
                }
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
            "global_errors": ["El slot de ID 999 no existe"]
        },
        expected_status=404
    )
    
def test_reserve(db_token):
    path = "/api/slots/reserve"
    
    
    # Caso 1: Slot reservada correctamente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            query_string={
                "id": 4
            }
        ),
        {
            "global_success": ["Slot reservado correctamente"],
            "slot": {
                "beginning": "Thu, 22 Feb 2024 00:00:00 GMT",
                "end": "Fri, 22 Mar 2024 00:00:00 GMT",
                "id": 4, "price": 100.0,
                "producer": {
                    "id": 4,
                    "location": "Madrid",
                    "name": "Ensambles Don Pepe"
                }
            }
        }
    )
    
    # Caso 2: Slot ya reservada
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
            "global_errors": ["El slot de ID 4 ya estaba reservado"]
        },
        expected_status=400
    )
    
    # Caso 3: Slot no encontrado
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
            "global_errors": ["El slot de ID 999 no existe"]
        },
        expected_status=404
    )

