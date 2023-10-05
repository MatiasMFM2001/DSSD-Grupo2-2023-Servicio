from src.core.database.board import Category
from src.core.business.crud_manager import CRUDManager


class CategoryManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CategoryManager."""
        super().__init__(Category)
    
    def validate(self, **kwargs):
        name = kwargs.get("name")
        
        if name is not None:
            search = self.database.filter_by(name=name).first()
            if (search is not None) and (search.name == name):
                raise ValueError(f"El nombre de categoría '{name}' ya está en uso.")