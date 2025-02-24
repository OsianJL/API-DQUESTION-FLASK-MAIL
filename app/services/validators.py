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

def validate_email(email: str) -> bool:
    """
    Valida que el email tenga un formato estándar:
    Debe contener al menos un carácter antes y después de '@' y un dominio con un punto.
    """
    # Esta expresión regular es simple y cubre la mayoría de los casos estándar.
    regex = r"(^[\w\.-]+@[\w\.-]+\.\w+$)"
    return re.match(regex, email) is not None