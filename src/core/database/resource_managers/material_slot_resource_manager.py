from src.core.database.resource_managers.logical_resource_manager import (
    PhysicalResourceManager,
)

class MaterialSlotResourceManager(PhysicalResourceManager):
    def reserve_all(self, objects, tuple_name):
        for selec in objects:
            if selec.reserved:
                raise ValueError(f"{tuple_name} de ID {selec.id} ya estaba reservada")

            selec.reserved = True
            self.dbs.add(selec)
    
    def atomic_reserve_all(self, material_ids, slot_ids):
        from src.core.database.board import MaterialSupplier, FabricationSlot
        
        with self.dbs.begin():
            materials = self.get_all(material_ids, MaterialSupplier)
            slots = self.get_all(slot_ids, FabricationSlot)
            
            self.reserve_all(materials, "El MaterialSupplier")
            self.reserve_all(slots, "El Slot de fabricación")