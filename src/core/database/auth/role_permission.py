from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db

role_permission = db.Table(
    "rol_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id")),
)
