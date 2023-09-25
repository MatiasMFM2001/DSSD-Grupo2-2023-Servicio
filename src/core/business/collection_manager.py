from src.core.database.board import Collection
from src.core.business.crud_manager import CRUDManager


#colection manager hereda de crud manager para que asi pueda guardad cosas en la BD
class CollectionManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase UserManager."""
        super().__init__(Collection)