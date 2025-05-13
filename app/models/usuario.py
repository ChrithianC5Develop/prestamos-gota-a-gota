"""
🇪🇸 Modelo de Usuario
🇺🇸 User Model
"""
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Usuario(Base):
    """
    🇪🇸 Modelo de usuario para la base de datos
    🇺🇸 User database model
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 🇪🇸 Relaciones
    # 🇺🇸 Relationships
    rol = relationship("Rol", back_populates="usuarios")
    prestamos_creados = relationship("Prestamo", back_populates="creado_por")
    pagos_registrados = relationship("Pago", back_populates="registrado_por")
    notificaciones = relationship("Notificacion", back_populates="usuario")
    cobranzas_asignadas = relationship("Cobranza", back_populates="cobrador")
    rutas_asignadas = relationship("Ruta", back_populates="cobrador") 