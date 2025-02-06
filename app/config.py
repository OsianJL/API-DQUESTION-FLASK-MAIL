import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Obtener la URL de la base de datos desde la variable de entorno
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
    # Si la URL empieza con 'postgres://', cámbiala a 'postgresql://'
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
