"""
🇪🇸 Router para la gestión de rutas
🇺🇸 Router for route management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.ruta import Ruta
from ..models.usuario import Usuario
from ..schemas.ruta import (
    RutaCreate,
    RutaUpdate,
    Ruta as RutaSchema
)
from ..utils.auth import get_current_active_user, verificar_rol_cobrador

router = APIRouter()

@router.post("/", response_model=RutaSchema)
async def crear_ruta(
    ruta: RutaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Crea una nueva ruta
    🇺🇸 Creates a new route
    """
    # Verificar que el cobrador existe
    cobrador = db.query(Usuario).filter(Usuario.id == ruta.cobrador_id).first()
    if not cobrador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cobrador no encontrado"
        )
    
    db_ruta = Ruta(**ruta.dict())
    db.add(db_ruta)
    db.commit()
    db.refresh(db_ruta)
    return db_ruta

@router.put("/{ruta_id}", response_model=RutaSchema)
async def actualizar_ruta(
    ruta_id: int,
    ruta: RutaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualiza una ruta existente
    🇺🇸 Updates an existing route
    """
    db_ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if not db_ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    
    for key, value in ruta.dict(exclude_unset=True).items():
        setattr(db_ruta, key, value)
    
    db.commit()
    db.refresh(db_ruta)
    return db_ruta

@router.get("/{ruta_id}", response_model=RutaSchema)
async def obtener_ruta(
    ruta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene una ruta por su ID
    🇺🇸 Gets a route by its ID
    """
    ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if not ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    return ruta

@router.get("/cobrador/{cobrador_id}", response_model=List[RutaSchema])
async def obtener_rutas_por_cobrador(
    cobrador_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene todas las rutas asignadas a un cobrador
    🇺🇸 Gets all routes assigned to a collector
    """
    rutas = db.query(Ruta).filter(Ruta.cobrador_id == cobrador_id).all()
    return rutas

@router.delete("/{ruta_id}")
async def eliminar_ruta(
    ruta_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Elimina una ruta
    🇺🇸 Deletes a route
    """
    ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if not ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    
    db.delete(ruta)
    db.commit()
    return {"message": "Ruta eliminada exitosamente"} 