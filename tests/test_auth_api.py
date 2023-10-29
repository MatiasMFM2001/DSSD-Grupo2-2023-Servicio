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
            json={
                "email": db_login.email,
                "password": password
            }
        ),
        {
            "display_data": {"first_name": "Admin", "last_name": "Numero 1", "roles": ["Administrador"]},
            "global_success": ["La sesión ha sido iniciada correctamente"],
            "token": db_token,
            "username": "Admin.Admin"
        },
        ignore_keys={"permissions"}
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
