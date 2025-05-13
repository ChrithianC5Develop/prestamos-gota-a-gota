"""
🇪🇸 Modelo de Préstamo
🇺🇸 Loan Model
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class FrecuenciaPago(str, enum.Enum):
    DIARIO = "diario"
    SEMANAL = "semanal"
    QUINCENAL = "quincenal"
    MENSUAL = "mensual"

class EstadoPrestamo(str, enum.Enum):
    PENDIENTE = "pendiente"
    ACTIVO = "activo"
    COMPLETADO = "completado"
    ATRASADO = "atrasado"
    CANCELADO = "cancelado"

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    monto = Column(Float)
    interes = Column(Float)  # Tasa de interés en porcentaje
    plazo = Column(Integer)  # Número de cuotas
    frecuencia_pago = Column(Enum(FrecuenciaPago))
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime)
    estado = Column(Enum(EstadoPrestamo), default=EstadoPrestamo.PENDIENTE)
    
    # Campos calculados almacenados
    monto_total = Column(Float)  # Monto + interés
    valor_cuota = Column(Float)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="prestamos")
    pagos = relationship("Pago", back_populates="prestamo")

    class Config:
        orm_mode = True 