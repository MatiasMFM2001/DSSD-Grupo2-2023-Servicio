from src.core.database.board import FabricationSlot
from src.core.business.crud_manager import CRUDManager
from src.core.business.producer_manager import ProducerManager

producer_m = ProducerManager()


class FabricationSlotManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(FabricationSlot)
    
    def validate(self, **kwargs):
            
        price = kwargs.get("price")
        
        if price is not None and price < 0.0:
            raise ValueError(f"El precio {price} es negativo.")
        
        beginning = kwargs.get("beginning")
        end = kwargs.get("end")

        if beginning is not None and end is not None and beginning >= end:
            raise ValueError(f"La fecha de inicio no puede ser mayor que la fecha final.")
        
        producer_id = kwargs.get("producer_id")
        
        if producer_id is not None and not producer_m.exists(producer_id):
            raise ValueError(f"El productor de ID {producer_id} no existe.")

    def atomic_reserve_all(self, material_ids, slot_ids):
        return self.database.atomic_reserve_all(material_ids, slot_ids)