import re

def validate_password(password: str) -> bool:
    """
    Valida que la contraseña cumpla con:
      - Al menos 8 caracteres
      - 1 letra mayúscula
      - 1 letra minúscula
      - 1 número
      - 1 carácter especial
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True
