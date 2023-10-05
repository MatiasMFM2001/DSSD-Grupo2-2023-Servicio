from src.core.database.board import Collection
from src.core.business.crud_manager import CRUDManager


#colection manager hereda de crud manager para que asi pueda guardad cosas en la BD
class CollectionManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase CollectionManager."""
        super().__init__(Collection)
    
    def validate(self, **kwargs):
        name = kwargs.get("name")
        
        if name is not None:
            search = self.database.filter_by(name=name).first()
            if (search is not None) and (search.name == name):
                raise ValueError(f"El nombre de colección '{name}' ya está en uso.")
        
        