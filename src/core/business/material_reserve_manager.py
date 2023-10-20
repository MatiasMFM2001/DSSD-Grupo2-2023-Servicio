from src.core.database.board import MaterialReserve
from src.core.business.crud_manager import CRUDManager


class MaterialReserveManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase MaterialReserveManager."""
        super().__init__(MaterialReserve)