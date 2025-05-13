"""
🇪🇸 Script para ejecutar la aplicación FastAPI
🇺🇸 Script to run FastAPI application
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    ) 