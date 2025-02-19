import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

# Configuración específica para pruebas
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Base de datos en memoria
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test_jwt_secret'
    SECRET_KEY = 'test_secret_key'

@pytest.fixture
def app():
    # Creamos la app usando la función create_app()
    app = create_app()
    # Sobrescribimos la configuración con la de pruebas
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

# Fixture para crear un usuario de prueba
@pytest.fixture
def test_user(app):
    # Crea un usuario de prueba
    user = User(email="test@example.com", password="Test@1234")
    db.session.add(user)
    db.session.commit()
    return user

# Fixture para generar un token JWT para el usuario de prueba
@pytest.fixture
def access_token(test_user, app):
    with app.app_context():
        # Usamos el id del usuario como identidad; conviértelo a string si es necesario
        token = create_access_token(identity=str(test_user.id))
        return token

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)
    print("Usando base de datos de pruebas:", app.config["SQLALCHEMY_DATABASE_URI"])
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_profile(client, access_token):
    # Crea un perfil para el usuario de prueba usando el endpoint POST /profile
    data = {
        "username": "mi_usuario",
        "image_url": "http://example.com/imagen.jpg",
        "moto": "Mi moto favorita"
    }
    response = client.post(
        "/profile",
        headers={"Authorization": f"Bearer {access_token}"},
        json=data
    )
    # Aseguramos que se creó correctamente
    assert response.status_code == 201, "El perfil debería crearse exitosamente"
    return data  # O podrías devolver algo más, si lo necesitas
