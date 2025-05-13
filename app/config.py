"""
🇪🇸 Configuración de la aplicación
🇺🇸 Application configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    🇪🇸 Configuración de la aplicación usando variables de entorno
    🇺🇸 Application settings using environment variables
    """
    # App Config
    PROJECT_NAME: str = "Prestamos Gota a Gota API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "your-password"
    DB_NAME: str = "prestamos_gota_a_gota"
    DATABASE_URL: str = "sqlite:///./prestamos.db"  # Default for testing
    
    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    
    # WhatsApp Business API
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_ID: str = ""
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    
    # Twilio (SMS)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    🇪🇸 Obtiene la configuración cacheada
    🇺🇸 Gets cached settings
    """
    return Settings()

settings = get_settings()

# 🇪🇸 Cadena de conexión para SQLAlchemy
# 🇺🇸 SQLAlchemy connection string
DATABASE_URL = settings.DATABASE_URL 