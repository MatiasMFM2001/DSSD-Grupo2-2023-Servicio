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
                    "id": 13,
                    "arrival_date": "Thu, 22 Feb 2024 00:00:00 GMT",
                    "material_id": 4,
                    "stock": 100,
                    "supplier": {
                        "id": 1,
                        "location": "Madrid",
                        "name": "Maderera San Jorge"
                    }
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
    
def test_multiple_single(db_token):
    path = "/api/material_supplier/multiple"
    
    
    # Caso 1: Lista obtenida
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {"4": 20},
                "arrival_date": "2024-02-27",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "4": [
                    {
                        "id": 13,
                        "arrival_date": "Thu, 22 Feb 2024 00:00:00 GMT",
                        "material_id": 4,
                        "stock": 100,
                        "supplier": {
                            "id": 1,
                            "location": "Madrid",
                            "name": "Maderera San Jorge"
                        }
                    }
                ]
            }
        }
    )
    
    # Caso 2: Lista vacía por stock insuficiente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {"4": 999},
                "arrival_date": "2024-02-27",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "4": []
            }
        }
    )
    
    # Caso 3: Lista vacía por no llegar a la fecha pedida
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {"4": 20},
                "arrival_date": "2024-02-20",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "4": []
            }
        }
    )

def test_multiple_multiple(db_token):
    path = "/api/material_supplier/multiple"
    
    
    # Caso 1: Lista obtenida
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {
                    "1": 2,
                    "3": 4,
                },
                "arrival_date": "2221-11-24",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "1": [
                    {
                        "arrival_date": "Sun, 03 Dec 2023 00:00:00 GMT",
                        "id": 1,
                        "material_id": 1,
                        "stock": 5,
                        "supplier": {
                            "id": 1,
                            "location": "Madrid",
                            "name": "Maderera San Jorge"
                        }
                    },
                    {
                        "arrival_date": "Tue, 05 Dec 2023 00:00:00 GMT",
                        "id": 7,
                        "material_id": 1,
                        "stock": 3,
                        "supplier": {
                            "id": 2,
                            "location": "Tarragona",
                            "name": "Herrería Hefesto"
                        }
                    }
                ],
                "3": [
                    {
                        "arrival_date": "Wed, 15 Nov 2023 00:00:00 GMT",
                        "id": 3,
                        "material_id": 3,
                        "stock": 15,
                        "supplier": {
                            "id": 3,
                            "location": "Barcelona",
                            "name": "Melamina de Nina"
                        }
                    },
                    {
                        "arrival_date": "Tue, 12 Dec 2023 00:00:00 GMT",
                        "id": 9,
                        "material_id": 3,
                        "stock": 10,
                        "supplier": {
                            "id": 1,
                            "location": "Madrid",
                            "name": "Maderera San Jorge"
                        }
                    }
                ]
            }
        }
    )
    
    # Caso 2: Lista vacía por stock insuficiente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {
                    "1": 2,
                    "3": 400,
                },
                "arrival_date": "2024-02-27",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "1": [
                    {
                        "arrival_date": "Sun, 03 Dec 2023 00:00:00 GMT",
                        "id": 1,
                        "material_id": 1,
                        "stock": 5,
                        "supplier": {
                            "id": 1,
                            "location": "Madrid",
                            "name": "Maderera San Jorge"
                        }
                    },
                    {
                        "arrival_date": "Tue, 05 Dec 2023 00:00:00 GMT",
                        "id": 7,
                        "material_id": 1,
                        "stock": 3,
                        "supplier": {
                            "id": 2,
                            "location": "Tarragona",
                            "name": "Herrería Hefesto"
                        }
                    }
                ],
                "3": []
            }
        }
    )
    
    # Caso 3: Lista vacía por no llegar a la fecha pedida
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_stocks": {
                    "1": 2,
                    "3": 4,
                },
                "arrival_date": "2023-02-20",
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "1": [],
                "3": []
            }
        }
    )


def test_reserve(db_token):
    path = "/api/material_supplier/reserve"
    
    
    # Caso 1.A: Material_supplier reservado correctamente
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
    
    # Caso 1.B: Ese Material_supplier ya no aparece en la lista
    template_api_test(
        lambda: client.post(
            "/api/material_supplier/multiple",
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "arrival_date": "2024-02-22",
                "material_stocks": {
                    "4": 100,
                },
            }
        ),
        {
            "global_success": [""],
            "material_suppliers": {
                "4": [
                    {
                        "arrival_date": "Thu, 22 Feb 2024 00:00:00 GMT",
                        "id": 13,
                        "material_id": 4,
                        "stock": 100,
                        "supplier": {
                            "id": 1,
                            "location": "Madrid",
                            "name": "Maderera San Jorge"}
                    }
                ]
            }
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

def test_reserve_all(db_token):
    path = "/api/material_supplier/reserve_all"
    
    # Caso 1: Todos reservados correctamente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [1, 3],
                "slot_ids": [3],
            }
        ),
        {
            "global_success": ["Todo reservado correctamente"],
        }
    )
    
    # Caso 2: Material_supplier ya reservado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [1],
                "slot_ids": [],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El MaterialSupplier de ID 1 ya estaba en el estado de reserva True"]
        },
        expected_status=400
    )
    
    # Caso 3: Slot ya reservado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [],
                "slot_ids": [3],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El Slot de fabricación de ID 3 ya estaba en el estado de reserva True"]
        },
        expected_status=400
    )
    
    # Caso 4: Material_supplier no encontrado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [999],
                "slot_ids": [],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El MaterialSupplier de ID 999 no existe"]
        },
        expected_status=404
    )
    
    # Caso 4: Slot no encontrado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [],
                "slot_ids": [999],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El Slot de fabricación de ID 999 no existe"]
        },
        expected_status=404
    )

def test_unreserve_all(db_token):
    path = "/api/material_supplier/un_reserve_all"
    
    # Caso 1.A: Todos reservados correctamente
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [1, 3],
                "slot_ids": [3],
            }
        ),
        {
            "global_success": ["Todo cancelado correctamente"],
        }
    )
    
    # Caso 2: Material_supplier ya reservado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [1],
                "slot_ids": [],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El MaterialSupplier de ID 1 ya estaba en el estado de reserva False"]
        },
        expected_status=400
    )
    
    # Caso 3: Slot ya reservado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [],
                "slot_ids": [3],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El Slot de fabricación de ID 3 ya estaba en el estado de reserva False"]
        },
        expected_status=400
    )
    
    # Caso 4: Material_supplier no encontrado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [999],
                "slot_ids": [],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El MaterialSupplier de ID 999 no existe"]
        },
        expected_status=404
    )
    
    # Caso 4: Slot no encontrado
    template_api_test(
        lambda: client.post(
            path,
            headers={"Authorization": f"Bearer {db_token}"},
            json={
                "material_ids": [],
                "slot_ids": [999],
            }
        ),
        {
            "field_errors": {},
            "global_errors": ["El Slot de fabricación de ID 999 no existe"]
        },
        expected_status=404
    )