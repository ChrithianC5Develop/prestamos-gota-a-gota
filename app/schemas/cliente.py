"""
🇪🇸 Schemas de Cliente
🇺🇸 Client Schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class ClienteBase(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    telefono: str
    direccion: str
    email: EmailStr

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None

class Cliente(ClienteBase):
    id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        orm_mode = True 