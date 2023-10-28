from src.core.database.board import FabricationSlot
from src.core.business.crud_manager import CRUDManager
from datetime import date


class MaterialRequestManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(FabricationSlot)
    
    def validate(self, **kwargs):
            
        price = kwargs.get("price")
        
        if amount is not None and amount < 0:
            raise ValueError(f"La cantidad {amount} es negativa.")
        
        if arrival_date is not None and arrival_date < date.today():
            raise ValueError(f"La fecha de llegada {arrival_date} está en el pasado.")
        
        beginning = kwargs.get("beginning")
        end = kwargs.get("end")

        if beginning is not None and end is not None and beginning >= end:
            raise ValueError(f"La fecha de inicio no puede ser mayor que la fecha final.")