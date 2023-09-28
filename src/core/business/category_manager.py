from src.core.database.board import Category
from src.core.business.crud_manager import CRUDManager


class CategoryManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CategoryManager."""
        super().__init__(Category)
        
    def get_categories_paginator(self, page):
        return self.get_paginator(
            self.database.query(), page
        )