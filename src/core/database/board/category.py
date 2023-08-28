from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)
from src.core.database.board.discipline_category import discipline_category


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    disciplines = db.relationship(
        "Discipline", secondary=discipline_category, back_populates="categories"
    )

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Category)
