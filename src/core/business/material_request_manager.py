from src.core.database.board import FabricationSlot
from src.core.business.crud_manager import CRUDManager
from datetime import date


class MaterialRequestManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(FabricationSlot)
    
    def validate(self, **kwargs):         
        amount = kwargs.get("amount")
        
        if amount is not None and amount < 0:
            raise ValueError(f"La cantidad {amount} es negativa.")
        
        arrival_date = kwargs.get("arrival_date")
        
        if arrival_date is not None and arrival_date < date.today():
            raise ValueError(f"La fecha de llegada {arrival_date} está en el pasado.")
