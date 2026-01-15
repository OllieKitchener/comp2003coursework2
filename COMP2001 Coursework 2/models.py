from datetime import datetime, timezone
from config import db, ma

class Profile(db.Model):
    __tablename__ = "Profiles"
    __table_args__ = {"schema": "CW2"}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(100))
    bio = db.Column(db.String(500))

    weight = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    preferred_units = db.Column(db.String(20), default="Metric")

    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        sqla_session = db.session
        include_fk = True