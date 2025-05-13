"""
🇪🇸 Configuración de la aplicación
🇺🇸 Application configuration
"""
from typing import List
from pydantic import BaseModel, AnyHttpUrl
from decouple import config

class Settings(BaseModel):
    # 🇪🇸 Configuración de la API
    # 🇺🇸 API Configuration
    PROJECT_NAME: str = "Prestamos Gota a Gota API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True
    
    # 🇪🇸 Configuración de la base de datos
    # 🇺🇸 Database Configuration
    DB_HOST: str = config('DB_HOST', default='localhost')
    DB_PORT: int = config('DB_PORT', default=3306, cast=int)
    DB_USER: str = config('DB_USER', default='root')
    DB_PASSWORD: str = config('DB_PASSWORD', default='cmvn5000')
    DB_NAME: str = config('DB_NAME', default='prestamos_gota_a_gota')
    
    # 🇪🇸 Configuración de JWT
    # 🇺🇸 JWT Configuration
    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', default='your-secret-key-here')
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 🇪🇸 Configuración de CORS
    # 🇺🇸 CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        case_sensitive = True

settings = Settings()

# 🇪🇸 Cadena de conexión para SQLAlchemy
# 🇺🇸 SQLAlchemy connection string
DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}" 