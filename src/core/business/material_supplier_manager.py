from src.core.database.board import MaterialRequest
from src.core.business.material_request_manager import MaterialRequestManager


class MaterialSupplierManager(MaterialRequestManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(FabricationSlot)
    