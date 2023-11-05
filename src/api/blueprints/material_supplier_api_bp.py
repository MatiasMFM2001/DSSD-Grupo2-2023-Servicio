from flask import Blueprint, request

from src.core.business.material_supplier_manager import MaterialSupplierManager
from src.core.business.material_manager import MaterialManager
from src.core.database.board import MaterialSupplier

from src.api.helpers import paginator_to_json, to_json
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse
from src.service.helpers.controller_helpers import get_int, api_validate_id
from src.core.business.user_manager import auth_m
from src.api.helpers.api_requests import get_json, force_fields
from werkzeug.exceptions import HTTPException

material_supplier_api_bp = Blueprint("material_supplier_api_bp", __name__, url_prefix="/material_supplier")
material_suppliers_m = MaterialSupplierManager()
material_m = MaterialManager()


@material_supplier_api_bp.route("/create", methods=["POST"])
@auth_m.permission_required("material_supplier_create")
def create_material_supplier():
    values, error = get_json({"material_id", "supplier_id", "stock", "arrival_date"})

    if error:
        return error

    material_suppliers_m.create(**values)
    return SimpleOKResponse("Material_supplier creado correctamente")

@material_supplier_api_bp.route("/all", methods=["GET"])
@auth_m.permission_required("material_supplier_list")
def all_material_suppliers_by_material_stock_arrival():
    """Obtiene todos los material_suppliers."""
    material, error = api_validate_id(material_m, request.args, tuple_name="El material", key="material")
    
    if error:
        return error
    
    values, error = force_fields(request.args, {"stock", "arrival_date", "material"})

    if error:
        return error
    
    material_suppliers = to_json(material_suppliers_m.filter_get_list(
        MaterialSupplier.material_id == material.id,
        MaterialSupplier.reserved == False,
        MaterialSupplier.stock >= values["stock"],
        MaterialSupplier.arrival_date <= values["arrival_date"],
    ))
    return SimpleOKResponse(material_suppliers=material_suppliers)

@material_supplier_api_bp.route("/reserve", methods=["POST"])
@auth_m.permission_required("material_supplier_reserve")
def reserve_material_supplier():
    """Reserva un material_supplier de fabricación"""
    material_supplier, error = api_validate_id(material_suppliers_m, request.args, tuple_name="El material_supplier")

    if error:
        return error

    if material_supplier.reserved:
        return SimpleErrorResponse(400, f"El material_supplier de ID {material_supplier.id} ya estaba reservado")
      
    material_suppliers_m.update(material_supplier.id, reserved=True)
    return SimpleOKResponse("Material_supplier reservado correctamente")

@material_supplier_api_bp.route("/reserve_all", methods=["POST"])
@auth_m.permission_required("material_supplier_reserve")
def atomic_reserve_all():
    values, error = get_json({"material_ids", "slot_ids"})

    if error:
        return error
    
    material_ids = values["material_ids"]
    slot_ids = values["slot_ids"]
    
    if not isinstance(material_ids, list):
        return SimpleErrorResponse(400, "material_ids no es una lista")
    
    if not isinstance(slot_ids, list):
        return SimpleErrorResponse(400, "slot_ids no es una lista")
    
    material_suppliers_m.atomic_reserve_all(material_ids, slot_ids)
    return SimpleOKResponse("Todo reservado correctamente")