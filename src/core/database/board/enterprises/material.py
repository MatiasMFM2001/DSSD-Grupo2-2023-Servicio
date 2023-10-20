from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"))
    supplier = db.relationship("Supplier", back_populates="materials")
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Material)
    
    