from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# Funciones para confirmación de email (ya existentes)
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["TOKEN_SECRET_KEY"])
    return serializer.dumps(email, salt="email-confirmation-salt")

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["TOKEN_SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt="email-confirmation-salt",
            max_age=expiration
        )
    except Exception:
        return False
    return email

# Nuevas funciones para resetear la contraseña
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["TOKEN_SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset-salt")

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["TOKEN_SECRET_KEY"])
    try:
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=expiration
        )
    except Exception:
        return False
    return email
