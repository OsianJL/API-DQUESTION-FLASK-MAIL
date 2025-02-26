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
    ADMIN_SECRET = os.getenv("ADMIN_SECRET", "clave_por_defecto")
    TOKEN_SECRET_KEY = os.environ.get('TOKEN_SECRET_KEY', 'default_token_key')


    # Configuración para Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ['true', '1']
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Tu email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # La contraseña o un app password
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)