from src.core.database.board import Slot
from src.core.business.crud_manager import CRUDManager


class SlotManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(Slot)
    
    def validate(self, **kwargs):
            
        price = kwargs.get("price")
        
        if price is not None and price < 0.0:
            raise ValueError(f"El precio {price} es negativo.")
        
        beginning = kwargs.get("beginning")
        end = kwargs.get("end")

        if beginning is not None and end is not None and beginning >= end:
            raise ValueError(f"La fecha de inicio no puede ser mayor que la fecha final.")