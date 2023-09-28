from src.core.database.board import Collection
from src.core.business.crud_manager import CRUDManager


#colection manager hereda de crud manager para que asi pueda guardad cosas en la BD
class CollectionManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CollectionManager."""
        super().__init__(Collection)
    
    def get_collections_paginator(self, page):
        return self.get_paginator(
            self.database.query(), page
        )