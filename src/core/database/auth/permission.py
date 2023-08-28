from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db
from src.core.database.auth.role_permission import role_permission
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)


class Permission(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Permission)
