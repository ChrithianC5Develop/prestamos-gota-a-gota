"""
🇪🇸 Tests para el sistema de notificaciones
🇺🇸 Tests for the notification system
"""
import pytest
from datetime import datetime
from app.models.notificacion import TipoNotificacion, CanalNotificacion, EstadoNotificacion
from app.schemas.notificacion import NotificacionCreate

def test_crear_notificacion(authorized_client, test_user):
    """
    🇪🇸 Test de creación de notificación
    🇺🇸 Test notification creation
    """
    notificacion_data = {
        "tipo": TipoNotificacion.PAGO.value,
        "canal": CanalNotificacion.EMAIL.value,
        "titulo": "Test Notification",
        "mensaje": "This is a test notification",
        "usuario_id": test_user.id,
        "datos_adicionales": {"test_key": "test_value"}
    }
    
    response = authorized_client.post("/api/v1/notificaciones/", json=notificacion_data)
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == notificacion_data["titulo"]
    assert data["estado"] == EstadoNotificacion.PENDIENTE.value

def test_marcar_notificacion_como_leida(authorized_client, test_user, db):
    """
    🇪🇸 Test para marcar una notificación como leída
    🇺🇸 Test marking a notification as read
    """
    from app.models.notificacion import Notificacion
    
    # Crear notificación de prueba
    notif = Notificacion(
        tipo=TipoNotificacion.PAGO,
        canal=CanalNotificacion.EMAIL,
        titulo="Test",
        mensaje="Test message",
        usuario_id=test_user.id,
        estado=EstadoNotificacion.ENVIADA
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    
    response = authorized_client.post(f"/api/v1/notificaciones/{notif.id}/leer")
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == EstadoNotificacion.LEIDA.value
    assert "fecha_lectura" in data

def test_obtener_resumen_notificaciones(authorized_client, test_user, db):
    """
    🇪🇸 Test para obtener el resumen de notificaciones
    🇺🇸 Test getting notification summary
    """
    from app.models.notificacion import Notificacion
    
    # Crear varias notificaciones de prueba
    notificaciones = [
        Notificacion(
            tipo=TipoNotificacion.PAGO,
            canal=CanalNotificacion.EMAIL,
            titulo=f"Test {i}",
            mensaje=f"Test message {i}",
            usuario_id=test_user.id,
            estado=EstadoNotificacion.PENDIENTE
        ) for i in range(3)
    ]
    db.add_all(notificaciones)
    db.commit()
    
    response = authorized_client.get("/api/v1/notificaciones/resumen")
    assert response.status_code == 200
    data = response.json()
    assert data["total_pendientes"] >= 3
    assert "por_tipo" in data
    assert "por_canal" in data 