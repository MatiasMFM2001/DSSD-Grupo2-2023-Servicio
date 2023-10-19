from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class FabricationSlot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    
    producer_id = db.Column(db.Integer, db.ForeignKey("producer.id"))
    producer = db.relationship("Producer", back_populates="slots")
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, FabricationSlot)
    
    