from src.core.database.db_instance import db
from src.core.database.resource_managers.material_slot_resource_manager import (
    MaterialSlotResourceManager,
)

class FabricationSlot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    beginning = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)
    reserved = db.Column(db.Boolean, nullable=False, default=False)
    fabrication_progress = db.Column(db.Float, nullable=False, default=0.0)
    
    producer_id = db.Column(db.Integer, db.ForeignKey("enterprises.id"))
    producer = db.relationship("Producer", back_populates="slots")
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return MaterialSlotResourceManager(db.session, FabricationSlot)
    
    def get_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "beginning": self.beginning,
            "end": self.end,
            "fabrication_progress": self.fabrication_progress,
            "producer": self.producer.get_json(),
        }
