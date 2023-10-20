from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)


class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    beginning = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)
    businessName = db.Column(db.String(255), nullable=False)
    reserved = db.Column(db.Boolean, default=False)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Slot)
    
    def get_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "beginning": self.beginning,
            "end":self.end,
            "businessName": self.businessName,
        }