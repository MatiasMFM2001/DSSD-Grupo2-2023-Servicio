from src.core.database.board import MaterialSupplier
from src.core.business.crud_manager import CRUDManager
from datetime import datetime
from src.core.business.supplier_manager import SupplierManager
from src.core.business.material_manager import MaterialManager

supplier_m = SupplierManager()
material_m = MaterialManager()


class MaterialSupplierManager(CRUDManager):
    def __init__(self):
        """Constructor de la clase SlotManager."""
        super().__init__(MaterialSupplier)
    
    def validate(self, **kwargs):         
        amount = kwargs.get("amount")
        
        if amount is not None and amount < 0:
            raise ValueError(f"La cantidad {amount} es negativa.")
        
        arrival_date = kwargs.get("arrival_date")
        
        if arrival_date is not None and datetime.strptime(arrival_date, "%Y-%m-%d") < datetime.today():
            raise ValueError(f"La fecha de llegada {arrival_date} está en el pasado.")
        
        supplier_id = kwargs.get("supplier_id")
        
        if supplier_id is not None and not supplier_m.exists(supplier_id):
            raise ValueError(f"El proveedor de ID {supplier_id} no existe.")
        
        material_id = kwargs.get("material_id")
        
        if material_id is not None and not material_m.exists(material_id):
            raise ValueError(f"El material de ID {material_id} no existe.")
    
    def atomic_reserve_all(self, material_ids, slot_ids):
        return self.database.atomic_reserve_all(material_ids, slot_ids, True)
    
    def atomic_unreserve_all(self, material_ids, slot_ids):
        return self.database.atomic_reserve_all(material_ids, slot_ids, False)

    def filter_available_get_list(self, material_id, min_stock, max_date):
        return self.filter_get_list(
            MaterialSupplier.material_id == material_id,
            MaterialSupplier.reserved == False,
            MaterialSupplier.stock >= min_stock,
            MaterialSupplier.arrival_date <= max_date,
        )