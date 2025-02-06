import pytest
from app import create_app
from app.extensions import db

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
