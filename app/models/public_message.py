from app.extensions import db
from datetime import datetime, timezone

class PublicMessage(db.Model):
    __tablename__ = "public_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    tematica = db.Column(db.String(100), nullable=False)
    idioma = db.Column(db.String(50), nullable=False)
    contestado = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)
    reply = db.Column(db.Text, nullable=True)
    responder_id = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

