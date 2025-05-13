"""
🇪🇸 Modelo de Cobranza
🇺🇸 Collection Model
"""
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class EstadoCobranza(str, enum.Enum):
    """
    🇪🇸 Estados posibles de una cobranza
    🇺🇸 Possible collection states
    """
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    FALLIDA = "fallida"
    REPROGRAMADA = "reprogramada"

class MetodoPago(str, enum.Enum):
    """
    🇪🇸 Métodos de pago aceptados
    🇺🇸 Accepted payment methods
    """
    EFECTIVO = "efectivo"
    TRANSFERENCIA = "transferencia"
    DEPOSITO = "deposito"
    MOVIL = "pago_movil"

class Cobranza(Base):
    """
    🇪🇸 Modelo principal de cobranza
    🇺🇸 Main collection model
    """
    __tablename__ = "cobranzas"

    id = Column(Integer, primary_key=True, index=True)
    
    # Referencias
    pago_id = Column(Integer, ForeignKey("pagos.id"), nullable=False)
    cobrador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Información de la cobranza
    monto_esperado = Column(Float, nullable=False)
    monto_recibido = Column(Float, nullable=True)
    metodo_pago = Column(Enum(MetodoPago), nullable=True)
    estado = Column(Enum(EstadoCobranza), default=EstadoCobranza.PENDIENTE)
    
    # Ubicación y ruta
    zona = Column(String(100), nullable=False)
    direccion_cobro = Column(String(500), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=True)
    orden_ruta = Column(Integer, nullable=True)
    
    # Timestamps
    fecha_programada = Column(DateTime(timezone=True), nullable=False)
    fecha_realizada = Column(DateTime(timezone=True), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Seguimiento
    intentos = Column(Integer, default=0)
    notas = Column(String(1000), nullable=True)
    requiere_supervisor = Column(Boolean, default=False)
    
    # Relaciones
    pago = relationship("Pago", back_populates="cobranzas")
    cobrador = relationship("Usuario", back_populates="cobranzas_asignadas")
    ruta = relationship("Ruta", back_populates="cobranzas")
    notificaciones = relationship("Notificacion", back_populates="cobranza")

    class Config:
        from_attributes = True 