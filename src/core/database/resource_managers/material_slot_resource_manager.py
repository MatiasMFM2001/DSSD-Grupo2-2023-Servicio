from src.core.database.resource_managers.logical_resource_manager import (
    PhysicalResourceManager,
)
from werkzeug.exceptions import NotFound

class MaterialSlotResourceManager(PhysicalResourceManager):
    def reserve_all(self, object_ids, tuple_name, model_class):
        exists_by_id = self.exists_all(object_ids, model_class=model_class)
        
        for id, result in exists_by_id.items():
            if not result:
                raise NotFound(f"{tuple_name} de ID {id} no existe")
        
        for selec in self.get_all(object_ids, model_class=model_class):
            if selec.reserved:
                raise ValueError(f"{tuple_name} de ID {selec.id} ya estaba reservada")

            selec.reserved = True
            self.dbs.add(selec)
    
    def atomic_reserve_all(self, material_ids, slot_ids):
        from src.core.database.board import MaterialSupplier, FabricationSlot
        
        with self.dbs.begin_nested():
            self.reserve_all(material_ids, "El MaterialSupplier", MaterialSupplier)
            self.reserve_all(slot_ids, "El Slot de fabricación", FabricationSlot)

        self.commit()