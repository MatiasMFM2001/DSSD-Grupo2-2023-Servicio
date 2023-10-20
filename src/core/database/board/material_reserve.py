from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class MaterialReserve(db.Model):
    __tablename__ = "material_reserve"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"), nullable=False)
    material = db.relationship("Material")

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, MaterialReserve)
    
    def get_json(self):
        return {
            "amount": self.amount,
            "id": self.id,
            "total_price": self.total_price,
        }