from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db
from src.core.database.auth.role_permission import role_permission
from src.core.database.auth.user_role import user_role
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", secondary=user_role, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permission)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Role)
