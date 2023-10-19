from src.core.database.board import Material
from src.core.business.crud_manager import CRUDManager


class MaterialManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase MaterialManager."""
        super().__init__(Material)
    
    def validate(self, **kwargs):
        name = kwargs.get("name")
        
        if name is not None:
            search = self.database.filter_by(name=name).first()
            if (search is not None) and (search.name == name):
                raise ValueError(f"El nombre de material '{name}' ya está en uso.")
        
        price = kwargs.get("price")
        
        if price is not None and price < 0.0:
            raise ValueError(f"El precio {price} es negativo.")