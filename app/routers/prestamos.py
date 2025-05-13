"""
🇪🇸 Router para la gestión de préstamos
🇺🇸 Router for loan management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models.prestamo import Prestamo, EstadoPrestamo
from ..models.pago import Pago, EstadoPago
from ..schemas.prestamo import PrestamoCreate, PrestamoUpdate, Prestamo as PrestamoSchema, PrestamoDetalle
from ..utils.auth import get_current_active_user

router = APIRouter()

def calcular_fechas_pagos(
    fecha_inicio: datetime,
    plazo: int,
    frecuencia_pago: str
) -> List[datetime]:
    """Calcula las fechas de pago basadas en la frecuencia"""
    fechas = []
    fecha_actual = fecha_inicio
    
    for _ in range(plazo):
        if frecuencia_pago == "diario":
            fecha_actual += timedelta(days=1)
        elif frecuencia_pago == "semanal":
            fecha_actual += timedelta(weeks=1)
        elif frecuencia_pago == "quincenal":
            fecha_actual += timedelta(days=15)
        elif frecuencia_pago == "mensual":
            # Aproximación simple del mes
            fecha_actual += timedelta(days=30)
        
        fechas.append(fecha_actual)
    
    return fechas

@router.post("/", response_model=PrestamoDetalle)
async def create_prestamo(
    prestamo: PrestamoCreate,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Crear un nuevo préstamo
    🇺🇸 Create a new loan
    """
    # Calcular montos
    monto_total = prestamo.monto * (1 + prestamo.interes/100)
    valor_cuota = monto_total / prestamo.plazo
    
    # Crear el préstamo
    db_prestamo = Prestamo(
        **prestamo.dict(),
        monto_total=monto_total,
        valor_cuota=valor_cuota,
        estado=EstadoPrestamo.ACTIVO,
        fecha_inicio=datetime.utcnow()
    )
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    
    # Generar los pagos
    fechas_pago = calcular_fechas_pagos(
        db_prestamo.fecha_inicio,
        prestamo.plazo,
        prestamo.frecuencia_pago
    )
    
    for i, fecha in enumerate(fechas_pago, 1):
        pago = Pago(
            prestamo_id=db_prestamo.id,
            numero_cuota=i,
            monto=valor_cuota,
            fecha_programada=fecha,
            estado=EstadoPago.PENDIENTE
        )
        db.add(pago)
    
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo

@router.get("/", response_model=List[PrestamoSchema])
async def get_prestamos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener lista de préstamos
    🇺🇸 Get list of loans
    """
    prestamos = db.query(Prestamo).offset(skip).limit(limit).all()
    return prestamos

@router.get("/{prestamo_id}", response_model=PrestamoDetalle)
async def get_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener un préstamo por ID
    🇺🇸 Get a loan by ID
    """
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if prestamo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    return prestamo

@router.put("/{prestamo_id}", response_model=PrestamoSchema)
async def update_prestamo(
    prestamo_id: int,
    prestamo: PrestamoUpdate,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualizar un préstamo
    🇺🇸 Update a loan
    """
    db_prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if db_prestamo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    
    # Actualizar solo los campos proporcionados
    for field, value in prestamo.dict(exclude_unset=True).items():
        setattr(db_prestamo, field, value)
    
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo

@router.delete("/{prestamo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Eliminar un préstamo
    🇺🇸 Delete a loan
    """
    prestamo = db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()
    if prestamo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    db.delete(prestamo)
    db.commit()
    return None 