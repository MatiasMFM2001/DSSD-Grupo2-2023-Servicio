from flask import Flask, render_template
from src.web.config import config
from src.web.helpers import handlers
from src.core.database.db_instance import db
from src.core.database import database
from src.web.blueprints.root_bp import root_bp
from src.web.helpers import view_helpers, controller_helpers
from src.core.business.cuote_manager import CuoteManager
from src.web.templates.super_templates.navbar import render_navbar
import locale
from flask_cors import CORS

cuotes_m = CuoteManager()


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

    app.jinja_env.globals.update(disable_if=view_helpers.disable_if)
    app.jinja_env.globals.update(num_to_words=view_helpers.num_to_spanish_words)
    app.jinja_env.globals.update(generate_url=controller_helpers.generate_url)
    app.jinja_env.globals.update(format_price=view_helpers.format_price)
    app.jinja_env.globals.update(format_date=view_helpers.format_date)
    app.jinja_env.globals.update(render_navbar=render_navbar)

    app.register_error_handler(400, handlers.bad_request_error)
    app.register_error_handler(401, handlers.unauthorized_error)
    app.register_error_handler(403, handlers.forbidden_error)
    app.register_error_handler(404, handlers.not_found_error)
    app.register_error_handler(422, handlers.unprocessable_entity_error)
    app.register_error_handler(500, handlers.internal_server_error)

    app.register_blueprint(root_bp)

    return app