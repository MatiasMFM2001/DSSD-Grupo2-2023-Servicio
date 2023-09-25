from src.core.database.db_instance import db

furniture_category = db.Table(
    "furniture_category",
    db.Column("furniture_id", db.Integer, db.ForeignKey("furniture.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)
