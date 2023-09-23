from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db
from src.core.database.auth.user_role import user_role
from src.core.database.resource_managers.user_resource_manager import (
    UserResourceManager,
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(db.DateTime, nullable=True, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    roles = db.relationship("Role", secondary=user_role, back_populates="users")

    def __repr__(self):
        """Retorna una representación del objeto.

        Returns:
            str: Representación del objeto.
        """
        return f"Usuario con nombre {self.first_name} {self.last_name}, con email {self.email}, roles {self.roles}"

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            UserResourceManager: Resource manager para este modelo.
        """
        return UserResourceManager(db.session, User)

    @property
    def full_name(self):
        """Retorna el nombre completo del usuario.

        Args:
            User: Usuario.
        Returns:
            str: Nombre completo del usuario.
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def roles_names(self):
        """Retorna el nombre de los roles del usuario.

        Args:
            User: Usuario.
        Returns:
            str: Nombre de los roles del usuario.
        """
        names = [role.name for role in self.roles]
        return ", ".join(names)
