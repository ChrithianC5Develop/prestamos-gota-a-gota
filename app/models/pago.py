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
    registrado_por_id = Column(Integer, ForeignKey("usuarios.id"))
    numero_cuota = Column(Integer)
    monto = Column(Float)
    fecha_programada = Column(DateTime)
    fecha_pago = Column(DateTime, nullable=True)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    
    # Relaciones
    prestamo = relationship("Prestamo", back_populates="pagos")
    registrado_por = relationship("Usuario", back_populates="pagos_registrados")
    notificaciones = relationship("Notificacion", back_populates="pago")
    cobranzas = relationship("Cobranza", back_populates="pago")

    class Config:
        from_attributes = True 