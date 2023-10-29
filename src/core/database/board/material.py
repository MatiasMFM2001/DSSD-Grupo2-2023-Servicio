from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    short_unit = db.Column(db.String(8), nullable=False, default="unit")
    
    suppliers = db.relationship("MaterialSupplier", back_populates="material")
    requests = db.relationship("MaterialRequest", back_populates="material")
    
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
            "short_unit": self.short_unit,
        }
    