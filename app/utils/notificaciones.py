"""
🇪🇸 Servicio de gestión de notificaciones
🇺🇸 Notification management service
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.notificacion import (
    Notificacion,
    TipoNotificacion,
    CanalNotificacion,
    EstadoNotificacion
)
from ..models.usuario import Usuario
from ..schemas.notificacion import NotificacionCreate, NotificacionResumen
from .notification_providers import get_notification_provider

class NotificationService:
    """
    🇪🇸 Servicio para gestionar notificaciones
    🇺🇸 Service for managing notifications
    """
    def __init__(self, db: Session):
        """
        🇪🇸 Inicializa el servicio con una sesión de base de datos
        🇺🇸 Initializes the service with a database session
        """
        self.db = db

    async def crear_notificacion(self, notificacion_data: NotificacionCreate) -> Notificacion:
        """
        🇪🇸 Crea una nueva notificación en la base de datos
        🇺🇸 Creates a new notification in the database
        """
        notificacion = Notificacion(
            tipo=notificacion_data.tipo,
            canal=notificacion_data.canal,
            titulo=notificacion_data.titulo,
            mensaje=notificacion_data.mensaje,
            usuario_id=notificacion_data.usuario_id,
            prestamo_id=notificacion_data.prestamo_id,
            pago_id=notificacion_data.pago_id,
            cobranza_id=notificacion_data.cobranza_id,
            datos_adicionales=notificacion_data.datos_adicionales,
            estado=EstadoNotificacion.PENDIENTE
        )
        
        self.db.add(notificacion)
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    async def enviar_notificacion(self, notificacion_id: int) -> bool:
        """
        🇪🇸 Envía una notificación específica usando el proveedor adecuado
        🇺🇸 Sends a specific notification using the appropriate provider
        """
        notificacion = self.db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
        if not notificacion:
            return False
        
        try:
            # Obtener el destinatario desde la base de datos
            destinatario = notificacion.usuario.email  # Asumiendo que se usa el correo

            # Obtener el proveedor adecuado para el canal de notificación
            provider = get_notification_provider(notificacion.canal)
            
            # Enviar la notificación
            success = await provider.send_notification(
                to=destinatario,
                title=notificacion.titulo,
                message=notificacion.mensaje,
                metadata=notificacion.datos_adicionales
            )
            
            if success:
                notificacion.estado = EstadoNotificacion.ENVIADA
                notificacion.fecha_envio = datetime.utcnow()
            else:
                notificacion.estado = EstadoNotificacion.FALLIDA
            
            self.db.commit()
            return success
        except Exception as e:
            # Loguear el error
            notificacion.estado = EstadoNotificacion.FALLIDA
            notificacion.datos_adicionales = {
                **(notificacion.datos_adicionales or {}),
                "error": str(e)
            }
            self.db.commit()
            return False

    async def marcar_como_leida(self, notificacion_id: int) -> Optional[Notificacion]:
        """
        🇪🇸 Marca una notificación como leída
        🇺🇸 Marks a notification as read
        """
        notificacion = self.db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
        if not notificacion:
            return None
        
        notificacion.estado = EstadoNotificacion.LEIDA
        notificacion.fecha_lectura = datetime.utcnow()
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def obtener_resumen(self) -> Dict[str, Any]:
        """
        🇪🇸 Obtiene un resumen de las notificaciones
        🇺🇸 Gets a notification summary
        """
        # Contar notificaciones por estado
        total_pendientes = self.db.query(func.count(Notificacion.id))\
            .filter(Notificacion.estado == EstadoNotificacion.PENDIENTE).scalar() or 0
        
        total_enviadas = self.db.query(func.count(Notificacion.id))\
            .filter(Notificacion.estado == EstadoNotificacion.ENVIADA).scalar() or 0
        
        total_fallidas = self.db.query(func.count(Notificacion.id))\
            .filter(Notificacion.estado == EstadoNotificacion.FALLIDA).scalar() or 0
        
        total_leidas = self.db.query(func.count(Notificacion.id))\
            .filter(Notificacion.estado == EstadoNotificacion.LEIDA).scalar() or 0
        
        # Contar por tipo de notificación
        por_tipo = {}
        for tipo in TipoNotificacion:
            por_tipo[tipo.value] = self.db.query(func.count(Notificacion.id))\
                .filter(Notificacion.tipo == tipo).scalar() or 0
        
        # Contar por canal
        por_canal = {}
        for canal in CanalNotificacion:
            por_canal[canal.value] = self.db.query(func.count(Notificacion.id))\
                .filter(Notificacion.canal == canal).scalar() or 0
        
        return {
            "total_pendientes": total_pendientes,
            "total_enviadas": total_enviadas,
            "total_fallidas": total_fallidas,
            "total_leidas": total_leidas,
            "por_tipo": por_tipo,
            "por_canal": por_canal
        }

    async def reenviar_fallidas(self) -> int:
        """
        🇪🇸 Reintenta enviar las notificaciones fallidas
        🇺🇸 Retries sending failed notifications
        """
        notificaciones_fallidas = self.db.query(Notificacion)\
            .filter(Notificacion.estado == EstadoNotificacion.FALLIDA)\
            .all()
        
        exitos = 0
        for notificacion in notificaciones_fallidas:
            if await self.enviar_notificacion(notificacion.id):
                exitos += 1
        
        return exitos 