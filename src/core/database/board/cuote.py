from datetime import datetime
from flask import Flask, current_app
from src.core.database.db_instance import db
from src.core.database.resource_managers.logical_resource_manager import (
    LogicalResourceManager,
)
from src.web.helpers.view_helpers import format_date, format_price
from enum import Enum
import os


class CuoteState(Enum):
    PAID = "Pagada y con recibo aceptado"
    UNPAID = "No pagada o recibo no enviado"
    PENDING = "Recibo enviado pero no verificado"

    def get_json(self):
        return {"name": self.name, "description": self.value}


class Cuote(db.Model):
    __tablename__ = "cuotes"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    late_fee = db.Column(db.Float, nullable=False, default=0.0)
    active = db.Column(db.Boolean, nullable=False, default=True)
    paid_date = db.Column(db.Date, nullable=True, default=None)
    expiration_date = db.Column(db.Date, nullable=False)
    file_extension = db.Column(db.String(4), nullable=True, default=None)
    # cuote_number = db.Column(db.Integer, nullable=False)

    associate_id = db.Column(db.Integer, db.ForeignKey("associates.id"))
    associate = db.relationship("Associate", back_populates="cuotes")

    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    service = db.relationship("Service")

    def get_json(self):
        return {
            "id": self.id,
            "state": self.state.get_json(),
            "date": format_date(self.expiration_date, "%B %Y"),
            "amount": format_price(self.price + self.late_fee),
            "service": self.service.get_json(),
        }

    def get_detail(self):
        return {"service": self.service.name, "price": self.price + self.late_fee}

    def relative_path(self, file_extension=None):
        extension = file_extension or self.file_extension
        return os.path.join(
            current_app.config["UPLOAD_FOLDER"], "cuotes", f"{self.id}.{extension}"
        )

    def absolute_path(self, file_extension=None):
        root_path = os.path.dirname(current_app.instance_path)
        return os.path.join(root_path, self.relative_path(file_extension))

    @property
    def total_price(self):
        """Retorna el precio total de la cuota.

        Returns:
            float: Precio total de la cuota.
        """
        return self.price + self.late_fee

    @property
    def state(self):
        if self.paid_date:
            return CuoteState.PAID

        if self.file_extension:
            return CuoteState.PENDING

        return CuoteState.UNPAID

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            LogicalResourceManager: Resource manager para este modelo.
        """
        return LogicalResourceManager(db.session, Cuote)
