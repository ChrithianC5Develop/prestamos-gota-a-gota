"""
🇪🇸 Modelo de Pago
🇺🇸 Payment Model
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class EstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    ATRASADO = "atrasado"

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"))
    numero_cuota = Column(Integer)
    monto = Column(Float)
    fecha_programada = Column(DateTime)
    fecha_pago = Column(DateTime, nullable=True)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    
    # Relaciones
    prestamo = relationship("Prestamo", back_populates="pagos")

    class Config:
        orm_mode = True 