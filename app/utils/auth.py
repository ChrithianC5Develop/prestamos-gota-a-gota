"""
🇪🇸 Utilidades de autenticación y autorización
🇺🇸 Authentication and authorization utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models.usuario import Usuario

# 🇪🇸 Configuración de bcrypt
# 🇺🇸 Bcrypt configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🇪🇸 Configuración de OAuth2
# 🇺🇸 OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    🇪🇸 Verifica si la contraseña coincide con el hash
    🇺🇸 Verifies if the password matches the hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    🇪🇸 Genera un hash de la contraseña
    🇺🇸 Generates a password hash
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    🇪🇸 Crea un token JWT
    🇺🇸 Creates a JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """
    🇪🇸 Obtiene el usuario actual basado en el token JWT
    🇺🇸 Gets the current user based on JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    🇪🇸 Verifica que el usuario actual esté activo
    🇺🇸 Verifies that the current user is active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user

async def verificar_rol_cobrador(current_user: Usuario = Depends(get_current_active_user)) -> Usuario:
    """
    🇪🇸 Verifica que el usuario tenga el rol de cobrador
    🇺🇸 Verifies that the user has the collector role
    """
    if current_user.rol_id != 2:  # Asumiendo que 2 es el ID del rol de cobrador
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de cobrador"
        )
    return current_user 