from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.core.database.db_instance import db

discipline_category = db.Table(
    "discipline_category",
    db.Column("disicipline_id", db.Integer, db.ForeignKey("services.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id")),
)
