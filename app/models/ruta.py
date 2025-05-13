"""
🇪🇸 Modelo de Ruta
🇺🇸 Route Model
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Ruta(Base):
    """
    🇪🇸 Modelo para rutas de cobranza
    🇺🇸 Collection route model
    """
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    zona = Column(String(100), nullable=False)
    cobrador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    cobrador = relationship("Usuario", back_populates="rutas_asignadas")
    cobranzas = relationship("Cobranza", back_populates="ruta")

    class Config:
        from_attributes = True 