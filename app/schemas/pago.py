"""
🇪🇸 Schemas de Pago
🇺🇸 Payment Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.pago import EstadoPago

class PagoBase(BaseModel):
    prestamo_id: int
    numero_cuota: int
    monto: float
    fecha_programada: datetime

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    fecha_pago: Optional[datetime] = None
    estado: Optional[EstadoPago] = None

class Pago(PagoBase):
    id: int
    fecha_pago: Optional[datetime]
    estado: EstadoPago

    class Config:
        orm_mode = True 