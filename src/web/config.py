from os import environ


class Config:
    SECRET_KEY = ""
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SECRET_KEY = "vgfvcbvcc"
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "America/Argentina/Buenos_Aires"
    UPLOAD_FOLDER = "public/images/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    BACKEND_URI = "https://admin-grupo20.proyecto2022.linti.unlp.edu.ar"


class DevelopmentConfig(Config):
    SECRET_KEY = "fdkljdklghjdshlk"
    DEBUG = True
    DB_USER = environ.get("DB_USER", "postgres")
    DB_PASS = environ.get("DB_PASS", "postgres")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_NAME = environ.get("DB_NAME", "club")
    DB_PORT = environ.get("DB_PORT", "5432")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SCHEDULER_TIMEZONE = "America/Argentina/Buenos_Aires"
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER = "public/images/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    BACKEND_URI = "http://localhost:5000"


class TestingConfig(Config):
    SECRET_KEY = True
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.db"


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": DevelopmentConfig,
}
