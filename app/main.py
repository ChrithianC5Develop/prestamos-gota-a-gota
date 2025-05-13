"""
🇪🇸 Punto de entrada principal de la aplicación
🇺🇸 Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# 🇪🇸 Crear la aplicación FastAPI
# 🇺🇸 Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
)

# 🇪🇸 Configurar CORS
# 🇺🇸 Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🇪🇸 Incluir los routers
# 🇺🇸 Include routers
from .routers import auth_router, usuarios_router, clientes_router, prestamos_router, pagos_router

app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Autenticación"]
)

app.include_router(
    usuarios_router,
    prefix=f"{settings.API_V1_PREFIX}/usuarios",
    tags=["Usuarios"]
)

app.include_router(
    clientes_router,
    prefix=f"{settings.API_V1_PREFIX}/clientes",
    tags=["Clientes"]
)

app.include_router(
    prestamos_router,
    prefix=f"{settings.API_V1_PREFIX}/prestamos",
    tags=["Préstamos"]
)

app.include_router(
    pagos_router,
    prefix=f"{settings.API_V1_PREFIX}/pagos",
    tags=["Pagos"]
)

@app.get("/")
async def root():
    """
    🇪🇸 Ruta raíz que redirige a la documentación
    🇺🇸 Root route that redirects to documentation
    """
    return {"message": "Bienvenido a la API de Prestamos Gota a Gota. Visite /api/v1/docs para la documentación."} 