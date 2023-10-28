from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class MaterialSupplier(db.Model):
    __tablename__ = "material_supplier"
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"), primary_key=True)
    
    material = db.relationship("Material", back_populates="suppliers")
    supplier = db.relationship("Supplier", back_populates="materials")

    stock = db.Column(db.Integer, nullable=False, default=0)
    arrival_date = db.Column(db.Date, nullable=False)
    
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, MaterialSupplier)
