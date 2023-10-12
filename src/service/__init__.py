from flask import Flask
from src.service.config import config
from src.service.helpers import handlers
from src.core.database.db_instance import db
from src.core.database import database
from src.api.blueprints.root_api_bp import root_api_bp
from src.service.helpers import controller_helpers
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from src.api.helpers.api_responses import SimpleErrorResponse


def create_app(static_folder: str = "static", env: str = "development") -> Flask:
    """Crea la aplicacion web.

    Args:
        env (str): configura el entorno. Por defecto "development".
        static_folder (str): ruta de archivos estaticos. Por defecto "static".

    Returns:
        Flask: instancia de la clase Flask.
    """

    # locale.setlocale(locale.LC_TIME, '')

    app = Flask(__name__, static_folder=static_folder, template_folder="templates/")
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
        return SimpleErrorResponse(500, str(exception))
    
    app.jinja_env.globals.update(generate_url=controller_helpers.generate_url)

    app.register_blueprint(root_api_bp)

    return app