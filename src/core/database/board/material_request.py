from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class MaterialRequest(db.Model):
    __tablename__ = "material_requests"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"))
    material = db.relationship("Material", back_populates="requests")
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, MaterialRequest)
    
    def get_json(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "delivery_date": self.delivery_date,
            "material_id": self.material_id,
        }
    