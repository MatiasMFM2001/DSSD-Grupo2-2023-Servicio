from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Collection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True) #colección
    bonita_process_id = db.Column(db.Integer) #id de la instancia del proceso de bonita de cada colección
    name = db.Column(db.String(255), nullable=False)
    initial_fabrication_term = db.Column(db.DateTime(), nullable=False)
    final_fabrication_term = db.Column(db.DateTime(), nullable=False)
    estimated_launch_date = db.Column(db.DateTime(), nullable=False)
    bd_or_drive = db.Column(db.String(2), nullable=False, default='bd')
    editable = db.Column(db.Boolean, default=True)
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
            "bonita_process_id": self.bonita_process_id,
            "initial_fabrication_term": self.initial_fabrication_term.strftime("%d/%m/%Y"),
            "final_fabrication_term": self.final_fabrication_term.strftime("%d/%m/%Y"),
            "estimated_launch_date": self.estimated_launch_date.strftime("%d/%m/%Y"),
            "bd_or_drive": self.bd_or_drive,
            "editable": self.editable
        }