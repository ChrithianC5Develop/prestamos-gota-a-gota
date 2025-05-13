"""
🇪🇸 Configuración de la base de datos
🇺🇸 Database configuration
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

# 🇪🇸 Configurar logging
# 🇺🇸 Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🇪🇸 Crear el motor de SQLAlchemy
# 🇺🇸 Create SQLAlchemy engine
try:
    logger.info(f"Intentando conectar a la base de datos con URL: {DATABASE_URL}")
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True  # Esto mostrará todas las consultas SQL
    )
    # Probar la conexión
    with engine.connect() as conn:
        logger.info("¡Conexión exitosa a la base de datos!")
except Exception as e:
    logger.error(f"Error al conectar a la base de datos: {str(e)}")
    raise

# 🇪🇸 Crear la sesión local
# 🇺🇸 Create local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🇪🇸 Crear la base declarativa
# 🇺🇸 Create declarative base
Base = declarative_base()

# 🇪🇸 Función para obtener la base de datos
# 🇺🇸 Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 