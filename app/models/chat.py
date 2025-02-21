from app.extensions import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    user2_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(), nullable=False)

    # Opcional: definir una restricción de unicidad para que no se repitan conversaciones
    __table_args__ = (
        db.UniqueConstraint('user1_id', 'user2_id', name='uq_chat_users'),
    )
