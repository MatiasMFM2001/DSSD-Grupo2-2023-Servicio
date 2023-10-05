from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)
from src.core.database.enterprises.enterprise import Enterprise

class Producer(Enterprise):
    __tablename__ = "producers"
    materials = db.relationship("Material", back_populates="producer")
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Producer)
    
    