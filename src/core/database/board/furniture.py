import os
from flask import current_app
from src.core.database.board.furniture_category import furniture_category
from src.core.database.db_instance import db
from src.core.database.resource_managers.physical_resource_manager import (
    PhysicalResourceManager,
)

class Furniture(db.Model):
    __tablename__ = "furniture"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(4), nullable=True, default=None)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"))
    collection = db.relationship("Collection", back_populates="furnitures")
    categories = db.relationship("Category", secondary=furniture_category)

    @staticmethod
    def resource_manager():
        """Retorna el resource manager para este modelo.

        Returns:
            PhysicalResourceManager: Resource manager para este modelo.
        """
        return PhysicalResourceManager(db.session, Furniture)
    
    def relative_path(self, file_extension=None):
        extension = file_extension or self.file_extension
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], "furniture")

        if self.file_extension is None:
            return os.path.join(path, "pfp0.jpg")

        return os.path.join(path, f"{self.id}.{extension}")

    def absolute_path(self, file_extension=None):
        root_path = os.path.dirname(current_app.instance_path)
        return os.path.join(root_path, self.relative_path(file_extension))
    
    def get_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "categories": [category.get_json() for category in self.categories]
        }
