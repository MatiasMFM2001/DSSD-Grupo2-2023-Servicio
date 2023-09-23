import os
from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db
from src.core.database.resource_managers.account_resource_manager import (
    AccountResourceManager,
)
from src.core.database.board.associate_service import associate_service
from src.core.business.service_manager import MembershipManager

membership_m = MembershipManager()


class Associate(db.Model):
    __tablename__ = "associates"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    doc_type = db.Column(db.String(8), nullable=False)
    doc_number = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    home_address = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    services = db.relationship(
        "Service", secondary=associate_service, back_populates="associates"
    )
    cuotes = db.relationship("Cuote", back_populates="associate")
    file_extension = db.Column(db.String(4), nullable=True, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = [membership_m.get_by_name("base")]

    def relative_path(self, file_extension=None):
        extension = file_extension or self.file_extension
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], "associates")

        if self.file_extension is None:
            return os.path.join(path, "pfp0.jpg")

        return os.path.join(path, f"{self.id}.{extension}")

    def absolute_path(self, file_extension=None):
        root_path = os.path.dirname(current_app.instance_path)
        return os.path.join(root_path, self.relative_path(file_extension))

    @property
    def full_name(self):
        """Retorna el nombre completo del socio.

        Returns:
            str: Nombre completo del socio.
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def full_document(self):
        """Retorna el tipo y número de documento del socio.

        Returns:
            str: Tipo y número de documento del socio.
        """
        return f"{self.doc_type} {self.doc_number}"

    @property
    def pfp_path(self):
        """Retorna el tipo y número de documento del socio.

        Returns:
            str: Tipo y número de documento del socio.
        """
        root_path = os.path.dirname(current_app.instance_path)
        base_path = current_app.config["UPLOAD_FOLDER"]
        path = lambda id: f"{base_path}/associates/pfp{id}.jpg"

        if os.path.exists(f"{root_path}/{path(self.id)}"):
            return path(self.id)
        else:
            return path(0)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            AccountResourceManager: Resource manager para este modelo.
        """
        return AccountResourceManager(db.session, Associate)

    def get_json(self):
        """Retorna la representación JSON del socio.

        Returns:
            dict: Representación JSON del socio.
        """
        return {
            "user": self.full_name,
            "email": self.email,
            "document_type": self.doc_type,
            "document_number": self.doc_number,
            "gender": self.genre,
            "address": self.home_address,
            "phone": self.phone_number,
        }
