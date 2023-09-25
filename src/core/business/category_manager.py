from src.core.database.board import Category
from src.core.business.crud_manager import CRUDManager


class CategoryManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CategoryManager."""
        super().__init__(Category)