from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)
from src.core.database.board import Enterprise

class Supplier(Enterprise):
    __tablename__ = "suppliers"
    materials = db.relationship("Material", back_populates="supplier")
    
    __mapper_args__ = {
        "polymorphic_identity": "supplier",
    }

    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Supplier)
    
    