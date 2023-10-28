import pytest
from src.core.business.user_manager import auth_m
from tests import app, client, template_api_test, db_login, db_token


def test_login(db_login, db_token):
    path = "/api/login"
    password = "1234"
    
    
    # Caso 1 de 4: Sesión iniciada correctamente
    template_api_test(
        lambda: client.post(
            path,
            json={"email": db_login.email, "password": password}
        ),
        {
            "display_data": {"first_name": "Admin", "last_name": "Numero 1", "roles": ["Administrador"]},
            "global_success": ["La sesión ha sido iniciada correctamente"],
            "permissions": ["furniture_material_show", "furniture_file_list", "material_create", "material_show", "furniture_list", "category_create", "batch_receive", "collection_show", "slot_reserve", "furniture_show", "collection_end", "batch_show", "user_create", "category_list", "slot_create", "home_show", "private_logout", "collection_create", "furniture_file_show", "collection_list", "batch_list", "furniture_material_create", "material_reserve", "slot_list", "furniture_file_create", "private_profile_edit", "user_list", "slot_show", "batch_sell", "material_list", "furniture_create", "furniture_material_list"],
            "token": db_token,
            "username": "Admin.Admin"
        }
    )
    
    # Caso 2 de 4: Credenciales inválidas
    template_api_test(
        lambda: client.post(
            path,
            json={"email": db_login.email, "password": "12345678"}
        ),
        {
            "field_errors": {},
            "global_errors": ["Credenciales inválidas"]
        },
        expected_status=401
    )
    
    # Caso 4 de 4: JSON inválido
    template_api_test(
        lambda: client.post(
            path,
            data=f'{{"email": {db_login.email}'
        ),
        {
            "field_errors": {},
            "global_errors": ["JSON inválido, o sin Content-Type"]
        },
        expected_status=400
    )
