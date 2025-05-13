"""
🇪🇸 Router para la gestión de notificaciones
🇺🇸 Router for notification management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.notificacion import Notificacion
from ..schemas.notificacion import (
    NotificacionCreate,
    NotificacionUpdate,
    Notificacion as NotificacionSchema,
    NotificacionResumen
)
from ..utils.notificaciones import NotificationService
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=NotificacionSchema)
async def crear_notificacion(
    notificacion: NotificacionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    🇪🇸 Crea una nueva notificación
    🇺🇸 Creates a new notification
    """
    service = NotificationService(db)
    return await service.crear_notificacion(notificacion)

@router.post("/{notificacion_id}/enviar")
async def enviar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    🇪🇸 Envía una notificación específica
    🇺🇸 Sends a specific notification
    """
    service = NotificationService(db)
    success = await service.enviar_notificacion(notificacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al enviar la notificación"
        )
    return {"message": "Notificación enviada exitosamente"}

@router.post("/{notificacion_id}/leer", response_model=NotificacionSchema)
async def marcar_como_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    🇪🇸 Marca una notificación como leída
    🇺🇸 Marks a notification as read
    """
    service = NotificationService(db)
    notificacion = await service.marcar_como_leida(notificacion_id)
    if not notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificación no encontrada"
        )
    return notificacion

@router.get("/resumen", response_model=NotificacionResumen)
async def obtener_resumen(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene un resumen de las notificaciones
    🇺🇸 Gets a notification summary
    """
    service = NotificationService(db)
    return service.obtener_resumen()

@router.post("/reenviar-fallidas")
async def reenviar_fallidas(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    🇪🇸 Reintenta enviar las notificaciones fallidas
    🇺🇸 Retries sending failed notifications
    """
    service = NotificationService(db)
    exitos = await service.reenviar_fallidas()
    return {
        "message": f"Se reenviaron exitosamente {exitos} notificaciones",
        "notificaciones_reenviadas": exitos
    } 