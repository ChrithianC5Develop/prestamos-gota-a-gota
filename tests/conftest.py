"""
🇪🇸 Configuración y fixtures para tests
🇺🇸 Configuration and fixtures for tests
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configurar variables de entorno para tests
os.environ["PROJECT_NAME"] = "Prestamos Gota a Gota API"
os.environ["API_V1_PREFIX"] = "/api/v1"
os.environ["DEBUG"] = "true"
os.environ["ENVIRONMENT"] = "test"
os.environ["BACKEND_CORS_ORIGINS"] = '["*"]'
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["SMTP_HOST"] = "smtp.gmail.com"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_USERNAME"] = "test@example.com"
os.environ["SMTP_PASSWORD"] = "test-password"
os.environ["SMTP_FROM_EMAIL"] = "test@example.com"
os.environ["WHATSAPP_TOKEN"] = "test-whatsapp-token"
os.environ["WHATSAPP_PHONE_ID"] = "test-phone-id"
os.environ["TELEGRAM_BOT_TOKEN"] = "test-telegram-token"
os.environ["TWILIO_ACCOUNT_SID"] = "test-account-sid"
os.environ["TWILIO_AUTH_TOKEN"] = "test-auth-token"
os.environ["TWILIO_PHONE_NUMBER"] = "+1234567890"

from app.database import Base, get_db
from app.main import app
from app.models import Rol, Usuario
from app.utils.auth import get_password_hash, create_access_token, oauth2_scheme

# Crear base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """
    🇪🇸 Fixture que proporciona una sesión de base de datos para tests
    🇺🇸 Fixture that provides a database session for tests
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """
    🇪🇸 Fixture que proporciona un cliente de test para la API
    🇺🇸 Fixture that provides a test client for the API
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user(db):
    """
    🇪🇸 Fixture que crea un usuario de prueba
    🇺🇸 Fixture that creates a test user
    """
    # Crear rol de administrador
    rol = Rol(
        id=1,
        nombre="Administrador",
        descripcion="Rol con acceso total al sistema"
    )
    db.add(rol)
    db.commit()
    
    # Crear rol de cobrador
    rol_cobrador = Rol(
        id=2,
        nombre="Cobrador",
        descripcion="Rol con permisos de cobranza"
    )
    db.add(rol_cobrador)
    db.commit()
    
    # Crear usuario de prueba
    user = Usuario(
        email="test@example.com",
        nombre="Test User",
        hashed_password=get_password_hash("testpassword"),
        rol_id=rol.id,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def token(test_user):
    """
    🇪🇸 Fixture que genera un token JWT para autenticación
    🇺🇸 Fixture that generates a JWT token for authentication
    """
    return create_access_token(
        data={"sub": test_user.email},
        expires_delta=None
    )

@pytest.fixture
def authorized_client(client, token):
    """
    🇪🇸 Fixture que proporciona un cliente autorizado con token JWT
    🇺🇸 Fixture that provides an authorized client with JWT token
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def authenticated_user(test_user, db):
    """
    🇪🇸 Fixture que proporciona un usuario autenticado
    🇺🇸 Fixture that provides an authenticated user
    """
    def override_dependency():
        return test_user
    
    app.dependency_overrides[oauth2_scheme] = lambda: "test-token"
    app.dependency_overrides[get_db] = lambda: db
    yield test_user
    del app.dependency_overrides[oauth2_scheme]
    del app.dependency_overrides[get_db] 