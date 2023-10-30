from src.core.database.board import Supplier
from src.core.business.crud_manager import CRUDManager


class SupplierManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase MaterialManager."""
        super().__init__(Supplier)
