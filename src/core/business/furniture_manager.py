from src.core.database.board import Furniture
from src.core.business.crud_manager import CRUDManager


class FurnitureManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase FurnitureManager."""
        super().__init__(Furniture)

    def get_furnitures_paginator(self, page):
        return self.get_paginator(
            self.database.query(), page
        )