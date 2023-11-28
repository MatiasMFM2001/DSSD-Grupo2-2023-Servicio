from flask import Flask, render_template
from src.service.config import config
from src.service.helpers import handlers
from src.core.database.db_instance import db
from src.core.database import database
from src.api.blueprints.root_api_bp import root_api_bp
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from src.api.helpers.api_responses import SimpleErrorResponse
#Facu estuvo aqui
#swagger
from flask_swagger_ui import get_swaggerui_blueprint
from pathlib import Path
import traceback


def create_app(static_folder: str = "static", env: str = "development") -> Flask:
    """Crea la aplicacion web.

    Args:
        env (str): configura el entorno. Por defecto "development".
        static_folder (str): ruta de archivos estaticos. Por defecto "static".

    Returns:
        Flask: instancia de la clase Flask.
    """

    # locale.setlocale(locale.LC_TIME, '')

    app = Flask(__name__, static_folder=static_folder, template_folder=Path(__file__).parent.parent.parent.resolve())
    app.config.from_object(config[env])
    db.init_app(app)

    if env == "development":
        cors = CORS(app, supports_credentials=True)

    @app.cli.command(name="reset_db")
    @app.route("/db/reset")
    def reset_db():
        """Resetea la base de datos."""
        database.reset_db()
        return "Reiniciado!"

    @app.cli.command(name="populate_db")
    def populate_db():
        """Llena la base de datos con datos de prueba."""
        database.populate_db()

    @app.cli.command(name="db_test_everything")
    def db_test_everything():
        """Ejecuta las funciones reset_db(), populate_db(), list_db(), delete_db(). de database.py"""
        database.db_test_everything()

    @app.route("/db/initialize")
    def initializate_prod_db():
        """Inicializa la base de datos en producción."""
        database.initializate_prod_db()
        return "Inicializado!"

    @app.cli.command(name="reset_and_initialize_db")
    @app.route("/db/reset_and_initialize")
    def reset_and_initialize_db():
        """Resetea e inicializa la base de datos."""
        database.reset_db()
        database.initializate_prod_db()
        return "Hecho!"
    
    @app.errorhandler(HTTPException)
    def handle_exception(exception):
        """Return JSON instead of HTML for HTTP errors."""
        return SimpleErrorResponse(exception.code, exception.description)
    
    @app.errorhandler(ValueError)
    def handle_error(exception):
        return SimpleErrorResponse(400, str(exception))
    
    @app.errorhandler(Exception)
    def handle_error(exception):
        print(traceback.format_exc())
        return SimpleErrorResponse(500, str(exception))

    #Facu estuvo aqui
    #Swagger
    
    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config["SWAGGER_URL"],  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        app.config["API_URL"],
        
        config={  # Swagger UI config overrides
            "app_name": "Global Furniture",
            "onComplete": """
                function(ui) {
                    ui.preauthorizeApiKey("bearerAuth", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTc4MTgyMjMsImlkIjoxfQ.NXRJSFAcWKFxezbZfo2eknurORhHXz5IzoXTH6h4cdo")
                }
            """
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )
    
    @swaggerui_blueprint.route(app.config["API_URL"])
    def read_swagger_file():
        return render_template("static/swagger.yaml", url=app.config["RUN_URL"], port=app.config["RUN_PORT"])

    app.register_blueprint(root_api_bp)
    app.register_blueprint(swaggerui_blueprint)

    return app