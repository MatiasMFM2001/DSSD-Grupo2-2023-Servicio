from src.core.database.resource_managers.logical_resource_manager import (
    LogicalResourceManager,
)
from src.core.business.helpers.sha512_helper import verify, encrypt_if_present


"""Abstracción de accesos a la tabla de Usuarios o Socios de la BD, donde se realizan bajas lógicas."""
class AccountResourceManager(LogicalResourceManager):
    # Usar "password=plain_password" en el filter_by() no lo encontraba
    def login(self, email, plain_password):
        for user in self.filter_by(email=email):
            if verify(plain_password, user.password):
                return user

        return None

    def create(self, **kwargs):
        kwargs = encrypt_if_present("password", **kwargs)
        return super().create(**kwargs)

    def update(self, id, *args, **kwargs):
        kwargs = encrypt_if_present("password", **kwargs)
        return super().update(id, *args, **kwargs)
