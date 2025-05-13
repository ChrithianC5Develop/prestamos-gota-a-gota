"""
🇪🇸 Proveedores de notificaciones
🇺🇸 Notification providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from ..models.notificacion import CanalNotificacion
from ..config import settings

class NotificationProvider(ABC):
    """
    🇪🇸 Clase base abstracta para proveedores de notificaciones
    🇺🇸 Abstract base class for notification providers
    """
    @abstractmethod
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Envía una notificación
        🇺🇸 Sends a notification
        """
        pass

class EmailNotificationProvider(NotificationProvider):
    """
    🇪🇸 Proveedor de notificaciones por correo electrónico
    🇺🇸 Email notification provider
    """
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Envía un correo electrónico
        🇺🇸 Sends an email
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_FROM_EMAIL
            msg['To'] = to
            msg['Subject'] = title
            
            # Contenido del mensaje
            msg.attach(MIMEText(message, 'plain'))
            
            # Conexión con el servidor SMTP
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            
            # Envío del correo
            text = msg.as_string()
            server.sendmail(settings.SMTP_FROM_EMAIL, to, text)
            server.quit()
            
            return True
        except Exception as e:
            # En un entorno real, aquí deberías loguear el error
            print(f"Error al enviar correo: {str(e)}")
            return False

class SMSNotificationProvider(NotificationProvider):
    """
    🇪🇸 Proveedor de notificaciones por SMS usando Twilio
    🇺🇸 SMS notification provider using Twilio
    """
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Envía un SMS
        🇺🇸 Sends an SMS
        """
        try:
            from twilio.rest import Client
            
            # Inicializar cliente de Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Enviar SMS
            message = client.messages.create(
                body=f"{title}\n{message}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to
            )
            
            return True
        except Exception as e:
            # En un entorno real, aquí deberías loguear el error
            print(f"Error al enviar SMS: {str(e)}")
            return False

class WhatsAppNotificationProvider(NotificationProvider):
    """
    🇪🇸 Proveedor de notificaciones por WhatsApp
    🇺🇸 WhatsApp notification provider
    """
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Envía un mensaje de WhatsApp
        🇺🇸 Sends a WhatsApp message
        """
        try:
            # URL de la API de WhatsApp Business
            url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_ID}/messages"
            
            # Cabeceras con el token de autenticación
            headers = {
                "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            
            # Payload con el mensaje
            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {
                    "body": f"{title}\n{message}"
                }
            }
            
            # Enviar la solicitud a la API
            response = requests.post(url, headers=headers, json=payload)
            
            return response.status_code == 200
        except Exception as e:
            # En un entorno real, aquí deberías loguear el error
            print(f"Error al enviar mensaje de WhatsApp: {str(e)}")
            return False

class TelegramNotificationProvider(NotificationProvider):
    """
    🇪🇸 Proveedor de notificaciones por Telegram
    🇺🇸 Telegram notification provider
    """
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Envía un mensaje de Telegram
        🇺🇸 Sends a Telegram message
        """
        try:
            # URL de la API de Telegram
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            
            # Payload con el mensaje
            payload = {
                "chat_id": to,
                "text": f"*{title}*\n{message}",
                "parse_mode": "Markdown"
            }
            
            # Enviar la solicitud a la API
            response = requests.post(url, json=payload)
            
            return response.status_code == 200
        except Exception as e:
            # En un entorno real, aquí deberías loguear el error
            print(f"Error al enviar mensaje de Telegram: {str(e)}")
            return False

class MockNotificationProvider(NotificationProvider):
    """
    🇪🇸 Proveedor de notificaciones ficticio para testing
    🇺🇸 Mock notification provider for testing
    """
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        🇪🇸 Simula el envío de una notificación
        🇺🇸 Simulates sending a notification
        """
        # Para testing, siempre devuelve True
        print(f"MOCK: Enviando notificación a {to} - Título: {title} - Mensaje: {message}")
        return True

def get_notification_provider(canal: CanalNotificacion) -> NotificationProvider:
    """
    🇪🇸 Factory para obtener el proveedor adecuado según el canal
    🇺🇸 Factory to get the appropriate provider based on the channel
    """
    # En ambiente de test, usamos el proveedor mock
    if settings.ENVIRONMENT == "test":
        return MockNotificationProvider()
        
    # En producción/desarrollo, usamos los proveedores reales
    providers = {
        CanalNotificacion.EMAIL: EmailNotificationProvider(),
        CanalNotificacion.SMS: SMSNotificationProvider(),
        CanalNotificacion.WHATSAPP: WhatsAppNotificationProvider(),
        CanalNotificacion.TELEGRAM: TelegramNotificationProvider(),
        CanalNotificacion.PUSH: MockNotificationProvider(),  # No implementado aún
    }
    
    return providers.get(canal, MockNotificationProvider()) 