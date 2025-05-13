"""
🇪🇸 Modelos de la aplicación
🇺🇸 Application models
"""
from .rol import Rol
from .usuario import Usuario
from .cliente import Cliente
from .prestamo import Prestamo
from .pago import Pago
from .notificacion import Notificacion
from .cobranza import Cobranza
from .ruta import Ruta

# Asegurar que todos los modelos estén disponibles
__all__ = [
    "Rol",
    "Usuario",
    "Cliente",
    "Prestamo",
    "Pago",
    "Notificacion",
    "Cobranza",
    "Ruta"
] 