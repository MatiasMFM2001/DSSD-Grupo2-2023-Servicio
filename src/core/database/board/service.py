from flask import Flask
from src.core.database.db_instance import db
from src.core.database.resource_managers.logical_resource_manager import (
    LogicalResourceManager,
)
from src.core.database.board.discipline_category import discipline_category
from src.core.database.board.associate_service import associate_service
from src.web.helpers.view_helpers import format_price


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    mensual_cost = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    associates = db.relationship(
        "Associate", secondary=associate_service, back_populates="services"
    )

    type = db.Column(db.String(16))

    __mapper_args__ = {"polymorphic_identity": "service", "polymorphic_on": type}

    def spanish_name(self):
        return "Servicio"

    def get_json(self):
        return {
            "name": self.name,
            "type": self.spanish_name(),
            "mensual_cost": format_price(self.mensual_cost),
        }

    def __str__(self):
        """Retorna una representación en string del objeto.

        Returns:
            str: Representación en string del objeto.
        """
        return f"{self.spanish_name()} {self.name}"

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            LogicalResourceManager: Resource manager para este modelo.
        """
        return LogicalResourceManager(db.session, db.with_polymorphic(Service, "*"))


class Discipline(Service):
    teacher = db.Column(db.String(120), nullable=False, default="")
    schedule_time = db.Column(db.String(80), nullable=False, default="")
    categories = db.relationship(
        "Category", secondary=discipline_category, back_populates="disciplines"
    )

    __mapper_args__ = {
        "polymorphic_identity": "discipline",
    }

    def spanish_name(self):
        return "Disciplina"

    def get_json(self):
        service_json = super().get_json()

        service_json["schedule_time"] = self.schedule_time
        service_json["teacher"] = self.teacher
        service_json["categories"] = ", ".join(
            [category.name for category in self.categories]
        )

        return service_json

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            LogicalResourceManager: Resource manager para este modelo.
        """
        return LogicalResourceManager(db.session, Discipline)


class Membership(Service):
    __mapper_args__ = {
        "polymorphic_identity": "membership",
    }

    def spanish_name(self):
        return "Membresía"

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            LogicalResourceManager: Resource manager para este modelo.
        """
        return LogicalResourceManager(db.session, Membership)
