"""
🇪🇸 Modelo de Cliente
🇺🇸 Client Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(20), unique=True, index=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    telefono = Column(String(20))
    direccion = Column(String(200))
    email = Column(String(100), unique=True, index=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    prestamos = relationship("Prestamo", back_populates="cliente")

    class Config:
        orm_mode = True 