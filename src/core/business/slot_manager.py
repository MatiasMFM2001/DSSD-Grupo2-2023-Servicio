from src.core.database.board import Slot
from src.core.business.crud_manager import CRUDManager


class SlotManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(Slot)
    
    def validate(self, **kwargs):
        name = kwargs.get("name")
        
        if name is not None:
            search = self.database.filter_by(name=name).first()
            if (search is not None) and (search.name == name):
                raise ValueError(f"El nombre de slot '{name}' ya está en uso.")
        
        beginning = kwargs.get("beginning")
        end = kwargs.get("end")

        if beginning is not None and end is not None and beginning <= end:
            raise ValueError(f"La fecha de inicio no puede ser menor que la fecha final.")