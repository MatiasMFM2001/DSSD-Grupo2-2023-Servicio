"""
from flask import Blueprint # para que funcione la url
from src.api.helpers.api_responses import SimpleOKResponse, SimpleErrorResponse #para las respuestas de error
from src.core.business.user_manager import auth_m #porque requiere login
from src.core.business.collection_manager import CollectionManager
from src.api.helpers.api_requests import get_json #para verificar que LOS CAMPOS NOM,BRADOS ESTEN!!


collection_api_bp = Blueprint("collection_api_bp", __name__, url_prefix="/collection") #para qeu se pueda usar la url

collection_m= CollectionManager()# para tener a mano el manager


@collection_api_bp.route("/cargar", methods=["POST"])
@auth_m.login_required(False) #yoo quiero el usuario en la query
def guardarCollection():
    values, error = get_json({"nombre"})

    if error:
        return error

    collection_m.create(**values)
    return SimpleOKResponse("Funca maestro")

"""