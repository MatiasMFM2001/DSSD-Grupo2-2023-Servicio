from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class MaterialSupplier(db.Model):
    __tablename__ = "material_supplier"
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    arrival_date = db.Column(db.Date, nullable=False)
    reserved = db.Column(db.Boolean, nullable=False, default=False)
    
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"))
    material = db.relationship("Material", back_populates="suppliers")
    
    supplier_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    supplier = db.relationship("Supplier", back_populates="materials")

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, MaterialSupplier)

    def get_json(self):
        return {
            "id": self.id,
            "material_id": self.material_id,
            "supplier_id": self.supplier_id,
            "stock": self.stock,
            "arrival_date": self.arrival_date,
        }