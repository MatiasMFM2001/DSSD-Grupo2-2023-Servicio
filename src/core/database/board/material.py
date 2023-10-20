from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    arrivalDate = db.Column(db.Date, nullable=False)
    businessName = db.Column(db.String(255), nullable=False)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Material)
    
    def get_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "price": self.price,
            "arrivalDate": self.arrivalDate,
            "businessName": self.businessName,
        }