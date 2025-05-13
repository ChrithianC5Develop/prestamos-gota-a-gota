"""
🇪🇸 Punto de entrada principal de la aplicación
🇺🇸 Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import usuarios, prestamos, pagos, notificaciones, cobranza, auth, clientes, rutas
from .config import settings

# 🇪🇸 Crear la aplicación FastAPI
# 🇺🇸 Create FastAPI application
app = FastAPI(
    title="Préstamos Gota a Gota API",
    description="""
    🇪🇸 API para el sistema de gestión de préstamos gota a gota.
    Incluye gestión de préstamos, pagos, cobranzas y notificaciones.
    
    🇺🇸 API for the "gota a gota" loan management system.
    Includes loan, payment, collection and notification management.
    """,
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# 🇪🇸 Configurar CORS
# 🇺🇸 Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🇪🇸 Incluir los routers
# 🇺🇸 Include routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Autenticación"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    usuarios.router,
    prefix="/api/v1/usuarios",
    tags=["Usuarios"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    clientes.router,
    prefix="/api/v1/clientes",
    tags=["Clientes"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    prestamos.router,
    prefix="/api/v1/prestamos",
    tags=["Préstamos"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    pagos.router,
    prefix="/api/v1/pagos",
    tags=["Pagos"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    notificaciones.router,
    prefix="/api/v1/notificaciones",
    tags=["Notificaciones"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    cobranza.router,
    prefix="/api/v1/cobranzas",
    tags=["Cobranzas"],
    responses={404: {"description": "No encontrado"}},
)

app.include_router(
    rutas.router,
    prefix="/api/v1/rutas",
    tags=["Rutas"],
    responses={404: {"description": "No encontrado"}},
)

@app.get("/", tags=["Root"])
async def root():
    """
    🇪🇸 Endpoint raíz que muestra información básica de la API
    🇺🇸 Root endpoint showing basic API information
    """
    return {
        "app": "Préstamos Gota a Gota API",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "redoc": "/api/v1/redoc"
    } 