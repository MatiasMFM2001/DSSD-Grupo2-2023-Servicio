from src.core.database import db
from src.core.auth import user_role

role_permission = db.Table(
    "rol_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id")),
)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", secondary=user_role, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_permission)
