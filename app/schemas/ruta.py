"""
🇪🇸 Schemas de Ruta
🇺🇸 Route Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class RutaBase(BaseModel):
    """
    🇪🇸 Schema base para rutas
    🇺🇸 Base route schema
    """
    nombre: str = Field(..., max_length=100)
    zona: str = Field(..., max_length=100)
    cobrador_id: int

class RutaCreate(RutaBase):
    """
    🇪🇸 Schema para crear rutas
    🇺🇸 Route creation schema
    """
    pass

class RutaUpdate(BaseModel):
    """
    🇪🇸 Schema para actualizar rutas
    🇺🇸 Route update schema
    """
    nombre: Optional[str] = Field(None, max_length=100)
    zona: Optional[str] = Field(None, max_length=100)
    cobrador_id: Optional[int] = None

class Ruta(RutaBase):
    """
    🇪🇸 Schema completo de ruta
    🇺🇸 Complete route schema
    """
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True 