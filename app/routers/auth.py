"""
🇪🇸 Router de autenticación
🇺🇸 Authentication router
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.usuario import Usuario
from ..utils.auth import verify_password, create_access_token
from ..config import settings

router = APIRouter()

@router.post("/login")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    🇪🇸 Endpoint de login que devuelve un token JWT
    🇺🇸 Login endpoint that returns a JWT token
    """
    # 🇪🇸 Buscar usuario por email
    # 🇺🇸 Find user by email
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 🇪🇸 Verificar contraseña
    # 🇺🇸 Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 🇪🇸 Verificar si el usuario está activo
    # 🇺🇸 Verify if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # 🇪🇸 Crear token de acceso
    # 🇺🇸 Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "nombre": user.nombre,
            "rol_id": user.rol_id
        }
    } 