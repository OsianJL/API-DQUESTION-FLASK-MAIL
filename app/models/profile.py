from app.extensions import db

class Profile(db.Model):
    __tablename__ = "profiles"

    # Usamos user_id como clave primaria para una relación uno a uno
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    image_url = db.Column(db.String(255))
    moto = db.Column(db.String(255))

    def __init__(self, user_id, username, image_url=None, moto=None):
        self.user_id = user_id
        self.username = username
        self.image_url = image_url
        self.moto = moto
