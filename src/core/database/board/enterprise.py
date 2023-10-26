from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Enterprise(db.Model):
    __tablename__ = "enterprises"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    
    type = db.Column(db.String(16))

    __mapper_args__ = {
        "polymorphic_identity": "enterprise",
        "polymorphic_on": type
    }
    
    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Enterprise)
    
    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
        }