"""
🇪🇸 Modelo de Notificación
🇺🇸 Notification Model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class TipoNotificacion(str, enum.Enum):
    """
    🇪🇸 Tipos de notificación
    🇺🇸 Notification types
    """
    SISTEMA = "sistema"
    PAGO = "pago"
    PRESTAMO = "prestamo"
    COBRANZA = "cobranza"
    ALERTA = "alerta"

class CanalNotificacion(str, enum.Enum):
    """
    🇪🇸 Canales de notificación
    🇺🇸 Notification channels
    """
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    PUSH = "push"

class EstadoNotificacion(str, enum.Enum):
    """
    🇪🇸 Estados de notificación
    🇺🇸 Notification states
    """
    PENDIENTE = "pendiente"
    ENVIADA = "enviada"
    FALLIDA = "fallida"
    LEIDA = "leida"

class Notificacion(Base):
    """
    🇪🇸 Modelo de notificación
    🇺🇸 Notification model
    """
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    
    # Tipo y canal
    tipo = Column(Enum(TipoNotificacion), nullable=False)
    canal = Column(Enum(CanalNotificacion), nullable=False)
    
    # Contenido
    titulo = Column(String(255), nullable=False)
    mensaje = Column(String(1000), nullable=False)
    datos_adicionales = Column(JSON, nullable=True)
    
    # Referencias
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    prestamo_id = Column(Integer, ForeignKey("prestamos.id"), nullable=True)
    pago_id = Column(Integer, ForeignKey("pagos.id"), nullable=True)
    cobranza_id = Column(Integer, ForeignKey("cobranzas.id"), nullable=True)
    
    # Estado y fechas
    estado = Column(Enum(EstadoNotificacion), default=EstadoNotificacion.PENDIENTE)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_envio = Column(DateTime(timezone=True), nullable=True)
    fecha_lectura = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notificaciones")
    prestamo = relationship("Prestamo", back_populates="notificaciones")
    pago = relationship("Pago", back_populates="notificaciones")
    cobranza = relationship("Cobranza", back_populates="notificaciones")

    class Config:
        from_attributes = True 