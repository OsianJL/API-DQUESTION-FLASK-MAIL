import json

def test_register_and_login(client):
    # Registrar un nuevo usuario
    register_data = {
        "email": "test@example.com",
        "password": "Test@1234"
    }
    response = client.post("/register", json=register_data)
    assert response.status_code == 201, "El registro debería retornar status 201"
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Usuario registrado exitosamente."

    # Iniciar sesión con las credenciales registradas
    login_data = {
        "email": "test@example.com",
        "password": "Test@1234"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200, "El login debería retornar status 200"
    data = response.get_json()
    assert "access_token" in data, "La respuesta debe incluir el access_token"

def test_protected_endpoint(client):
    # Registrar y loguear un usuario para obtener el token
    register_data = {
        "email": "protected@example.com",
        "password": "Protected@123"
    }
    client.post("/register", json=register_data)

    login_data = {
        "email": "protected@example.com",
        "password": "Protected@123"
    }
    response = client.post("/login", json=login_data)
    data = response.get_json()
    token = data.get("access_token")
    assert token is not None, "El token JWT no debe ser None"

    # Acceder a la ruta protegida usando el token obtenido
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200, "La ruta protegida debería retornar status 200"
    data = response.get_json()
    assert "message" in data, "La respuesta debe incluir un mensaje"
    assert "ruta protegida" in data["message"], "El mensaje debe indicar que es una ruta protegida"
