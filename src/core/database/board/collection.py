from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Collection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True) #colección
    name = db.Column(db.String(255), nullable=False)
    initial_fabrication_term = db.Column(db.DateTime(), nullable=False)
    final_fabrication_term = db.Column(db.DateTime(), nullable=False)
    estimated_launch_date = db.Column(db.DateTime(), nullable=False)
    furnitures = db.relationship("Furniture", back_populates="collection") # ?

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Collection)
    
    def get_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "initial_fabrication_term": self.initial_fabrication_term,
            "final_fabrication_term": self.final_fabrication_term,
            "estimated_launch_date": self.estimated_launch_date
        }