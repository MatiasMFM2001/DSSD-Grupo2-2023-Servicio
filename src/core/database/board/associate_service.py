from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db

associate_service = db.Table(
    "associate_service",
    db.Column("associate_id", db.Integer, db.ForeignKey("associates.id")),
    db.Column("service_id", db.Integer, db.ForeignKey("services.id")),
)
