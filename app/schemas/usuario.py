"""
🇪🇸 Esquemas de Usuario
🇺🇸 User Schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    """
    🇪🇸 Esquema base de usuario
    🇺🇸 Base user schema
    """
    email: EmailStr
    nombre: str
    is_active: bool = True

class UsuarioCreate(UsuarioBase):
    """
    🇪🇸 Esquema para crear usuario
    🇺🇸 User creation schema
    """
    password: str
    rol_id: int

class UsuarioUpdate(BaseModel):
    """
    🇪🇸 Esquema para actualizar usuario
    🇺🇸 User update schema
    """
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None
    is_active: Optional[bool] = None

class Usuario(UsuarioBase):
    """
    🇪🇸 Esquema completo de usuario
    🇺🇸 Complete user schema
    """
    id: int
    rol_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """
        🇪🇸 Configuración del modelo
        🇺🇸 Model configuration
        """
        from_attributes = True

class UsuarioInDB(Usuario):
    """
    🇪🇸 Esquema de usuario en base de datos
    🇺🇸 User in database schema
    """
    hashed_password: str 