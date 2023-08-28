from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from src.core.database.db_instance import db
from src.core.database.auth.user_role import user_role
from src.core.database.resource_managers.config_resource_manager import (
    ConfigResourceManager,
)


class Configuration(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    rows_per_page = db.Column(db.Integer, default=10)
    show_payment_table = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(512), nullable=False, default="02214870193")
    club_email = db.Column(
        db.String(512), nullable=False, default="clubdeportivovillaelisa@gmail.com"
    )
    payment_text = db.Column(
        db.String(512), nullable=False, default="Club Deportivo Villa Elisa"
    )
    price_format = db.Column(db.String(32), nullable=False, default="ARS $<valor>")
    late_fee_percentage = db.Column(db.Float, nullable=False, default=10.0)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            ConfigResourceManager: Resource manager para este modelo.
        """
        return ConfigResourceManager(db.session, Configuration)

    @staticmethod
    def get(key):
        """Retorna el valor de la configuración para la clave dada.

        Args:
            key (str): Clave de la configuración.

        Returns:
            str: Valor de la configuración.
        """
        return Configuration.resource_manager().get_value(key)

    @staticmethod
    def update(key, value):
        """Actualiza el valor de la configuración para la clave dada.

        Args:
            key (str): Clave de la configuración.
            value (str): Valor de la configuración.

        Returns:
            Any: Valor de la configuración actualizado.
        """
        return Configuration.resource_manager().update_value(key, value)
