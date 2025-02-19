import json

def test_create_profile(client, access_token):
    # Suponiendo que tienes un fixture "client" y "access_token" configurados en conftest.py
    data = {
        "username": "mi_usuario",
        "image_url": "http://url-de-mi-imagen.com/imagen.jpg",
        "moto": "Mi moto favorita"
    }
    response = client.post(
        "/profile",
        headers={"Authorization": f"Bearer {access_token}"},
        json=data
    )
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Perfil creado exitosamente."

def test_get_profile(client, access_token, test_user, test_profile):
    response = client.get(
        f"/profile/{test_user.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert "username" in json_data

def test_patch_profile(client, access_token, test_user, test_profile):
    data = {"moto": "Actualización parcial de moto"}
    response = client.patch(
        f"/profile/{test_user.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=data
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Perfil actualizado exitosamente."

def test_delete_profile(client, access_token, test_user, test_profile):
    response = client.delete(
        f"/profile/{test_user.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Perfil eliminado exitosamente."
