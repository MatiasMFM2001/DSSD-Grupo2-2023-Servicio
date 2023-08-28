from src.core.business.crud_manager import CRUDManager


"""Capa de negocio de alto nivel base, para la tabla de Usuarios o Socios de la BD, donde se requiere hacer CRUDs sobre sus tuplas."""
class AccountManager(CRUDManager):
    # Nota: Hasta ahora no sabemos cómo es el login de Socios;
    # si lo llamás desde AssociateManager explota
    def login(self, email, plain_password):
        """Verifica si un usuario y contraseña son válidos.

        Args:
            email (str): Correo electrónico del usuario.
            plain_password (str): Contraseña del usuario.

        Returns:
            user: Usuario si es válido, None en caso contrario.
        """
        return self.database.login(email, plain_password)

    def validate(self, **kwargs):
        if "email" in kwargs:
            search = self.database.filter_by(True, email=kwargs["email"]).first()
            if (search is not None) and (search.email == kwargs["email"]):
                raise ValueError(f"El email {search.email} ya esta en uso.")

    def validate_update(self, id, **kwargs):
        if "email" in kwargs:
            search = self.database.filter_by(True, email=kwargs["email"]).first()
            if (
                (search is not None)
                and (search.email == kwargs["email"])
                and (search.id != id)
            ):
                raise ValueError(f"El email {search.email} ya esta en uso.")
