"""
🇪🇸 Schemas de Cobranza
🇺🇸 Collection Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from ..models.cobranza import EstadoCobranza, MetodoPago

class CobranzaBase(BaseModel):
    """
    🇪🇸 Schema base para cobranzas
    🇺🇸 Base collection schema
    """
    pago_id: int
    cobrador_id: int
    monto_esperado: float
    zona: str = Field(..., max_length=100)
    direccion_cobro: str = Field(..., max_length=500)
    fecha_programada: datetime
    ruta_id: Optional[int] = None
    orden_ruta: Optional[int] = None

class CobranzaCreate(CobranzaBase):
    """
    🇪🇸 Schema para crear cobranzas
    🇺🇸 Collection creation schema
    """
    pass

class CobranzaUpdate(BaseModel):
    """
    🇪🇸 Schema para actualizar cobranzas
    🇺🇸 Collection update schema
    """
    monto_recibido: Optional[float] = None
    metodo_pago: Optional[MetodoPago] = None
    estado: Optional[EstadoCobranza] = None
    fecha_realizada: Optional[datetime] = None
    notas: Optional[str] = Field(None, max_length=1000)
    requiere_supervisor: Optional[bool] = None
    ruta_id: Optional[int] = None
    orden_ruta: Optional[int] = None

class Cobranza(CobranzaBase):
    """
    🇪🇸 Schema completo de cobranza
    🇺🇸 Complete collection schema
    """
    id: int
    monto_recibido: Optional[float] = None
    metodo_pago: Optional[MetodoPago] = None
    estado: EstadoCobranza
    fecha_realizada: Optional[datetime] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    intentos: int
    notas: Optional[str] = None
    requiere_supervisor: bool

    class Config:
        from_attributes = True

class CobranzaResumen(BaseModel):
    """
    🇪🇸 Schema resumido para el dashboard
    🇺🇸 Summary schema for dashboard
    """
    total_pendientes: int
    total_completadas: int
    total_fallidas: int
    monto_total_esperado: float
    monto_total_recibido: float
    por_zona: dict[str, int]
    por_cobrador: dict[str, int]
    por_estado: dict[str, int]

class RutaCobranza(BaseModel):
    """
    🇪🇸 Schema para rutas de cobranza
    🇺🇸 Collection route schema
    """
    id: int
    fecha: datetime
    cobrador_id: int
    zona: str
    cobranzas: List[Cobranza]
    
    class Config:
        from_attributes = True

class AsignacionCobranza(BaseModel):
    """
    🇪🇸 Schema para asignar cobranzas a cobradores
    🇺🇸 Schema for assigning collections to collectors
    """
    cobrador_id: int
    cobranza_ids: List[int]
    fecha_programada: Optional[datetime] = None 