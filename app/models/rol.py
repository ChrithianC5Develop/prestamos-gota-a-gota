"""
🇪🇸 Modelo de Rol
🇺🇸 Role Model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class Rol(Base):
    """
    🇪🇸 Modelo de rol para la base de datos
    🇺🇸 Role database model
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))

    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol") 