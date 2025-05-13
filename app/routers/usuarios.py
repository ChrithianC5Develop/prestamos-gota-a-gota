"""
🇪🇸 Router para la gestión de usuarios
🇺🇸 Router for user management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.usuario import Usuario
from ..schemas.usuario import UsuarioCreate, UsuarioUpdate, Usuario as UsuarioSchema
from ..utils.auth import get_current_active_user, get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UsuarioSchema])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener lista de usuarios
    🇺🇸 Get list of users
    """
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.post("/", response_model=UsuarioSchema)
async def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Crear un nuevo usuario
    🇺🇸 Create a new user
    """
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    hashed_password = get_password_hash(usuario.password)
    db_usuario = Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        hashed_password=hashed_password,
        rol_id=usuario.rol_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/{usuario_id}", response_model=UsuarioSchema)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener un usuario por ID
    🇺🇸 Get a user by ID
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioSchema)
async def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualizar un usuario
    🇺🇸 Update a user
    """
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    update_data = usuario.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_usuario, field, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Eliminar un usuario
    🇺🇸 Delete a user
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    db.delete(usuario)
    db.commit()
    return None 