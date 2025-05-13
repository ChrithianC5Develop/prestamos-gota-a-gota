"""
🇪🇸 Esquemas de notificación
🇺🇸 Notification schemas
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from ..models.notificacion import TipoNotificacion, CanalNotificacion, EstadoNotificacion

class NotificacionBase(BaseModel):
    """
    🇪🇸 Esquema base para notificaciones
    🇺🇸 Base schema for notifications
    """
    tipo: TipoNotificacion
    canal: CanalNotificacion
    titulo: str
    mensaje: str
    datos_adicionales: Optional[Dict[str, Any]] = None

class NotificacionCreate(NotificacionBase):
    """
    🇪🇸 Esquema para crear notificaciones
    🇺🇸 Schema for creating notifications
    """
    usuario_id: int
    prestamo_id: Optional[int] = None
    pago_id: Optional[int] = None
    cobranza_id: Optional[int] = None

class NotificacionUpdate(BaseModel):
    """
    🇪🇸 Esquema para actualizar notificaciones
    🇺🇸 Schema for updating notifications
    """
    titulo: Optional[str] = None
    mensaje: Optional[str] = None
    estado: Optional[EstadoNotificacion] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class Notificacion(NotificacionBase):
    """
    🇪🇸 Esquema completo de notificación
    🇺🇸 Full notification schema
    """
    id: int
    usuario_id: int
    prestamo_id: Optional[int] = None
    pago_id: Optional[int] = None
    cobranza_id: Optional[int] = None
    estado: EstadoNotificacion
    fecha_creacion: datetime
    fecha_envio: Optional[datetime] = None
    fecha_lectura: Optional[datetime] = None

    class Config:
        from_attributes = True

class NotificacionResumen(BaseModel):
    """
    🇪🇸 Esquema para el resumen de notificaciones
    🇺🇸 Schema for notification summary
    """
    total_pendientes: int
    total_enviadas: int
    total_fallidas: int
    total_leidas: int
    por_tipo: Dict[str, int]
    por_canal: Dict[str, int] 