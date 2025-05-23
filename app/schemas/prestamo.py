"""
🇪🇸 Schemas de Préstamo
🇺🇸 Loan Schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from ..models.prestamo import FrecuenciaPago, EstadoPrestamo
from .cliente import Cliente
from .pago import Pago

class PrestamoBase(BaseModel):
    cliente_id: int
    monto: float
    interes: float
    plazo: int
    frecuencia_pago: FrecuenciaPago

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoUpdate(BaseModel):
    estado: Optional[EstadoPrestamo] = None
    monto: Optional[float] = None
    interes: Optional[float] = None
    plazo: Optional[int] = None
    frecuencia_pago: Optional[FrecuenciaPago] = None

class Prestamo(PrestamoBase):
    id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: EstadoPrestamo
    monto_total: float
    valor_cuota: float

    class Config:
        from_attributes = True

class PrestamoDetalle(Prestamo):
    cliente: Cliente
    pagos: List[Pago]

    class Config:
        from_attributes = True 