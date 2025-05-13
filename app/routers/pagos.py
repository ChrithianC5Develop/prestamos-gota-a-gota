"""
🇪🇸 Router para la gestión de pagos
🇺🇸 Router for payment management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.pago import Pago, EstadoPago
from ..models.prestamo import Prestamo, EstadoPrestamo
from ..schemas.pago import PagoCreate, PagoUpdate, Pago as PagoSchema
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=PagoSchema)
async def create_pago(
    pago: PagoCreate,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Registrar un nuevo pago
    🇺🇸 Register a new payment
    """
    # Verificar que el préstamo existe
    prestamo = db.query(Prestamo).filter(Prestamo.id == pago.prestamo_id).first()
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado"
        )
    
    # Crear el pago
    db_pago = Pago(**pago.dict())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    
    # Actualizar estado del préstamo si es necesario
    pagos_pendientes = db.query(Pago).filter(
        Pago.prestamo_id == prestamo.id,
        Pago.estado == EstadoPago.PENDIENTE
    ).count()
    
    if pagos_pendientes == 0:
        prestamo.estado = EstadoPrestamo.COMPLETADO
        db.commit()
    
    return db_pago

@router.get("/prestamo/{prestamo_id}", response_model=List[PagoSchema])
async def get_pagos_by_prestamo(
    prestamo_id: int,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener pagos de un préstamo
    🇺🇸 Get payments of a loan
    """
    pagos = db.query(Pago).filter(Pago.prestamo_id == prestamo_id).all()
    return pagos

@router.put("/{pago_id}", response_model=PagoSchema)
async def update_pago(
    pago_id: int,
    pago: PagoUpdate,
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualizar un pago
    🇺🇸 Update a payment
    """
    db_pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if db_pago is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )
    
    # Si se está marcando como pagado
    if pago.estado == EstadoPago.PAGADO and db_pago.estado != EstadoPago.PAGADO:
        db_pago.fecha_pago = datetime.utcnow()
    
    for field, value in pago.dict(exclude_unset=True).items():
        setattr(db_pago, field, value)
    
    db.commit()
    db.refresh(db_pago)
    
    # Actualizar estado del préstamo si es necesario
    prestamo = db.query(Prestamo).filter(Prestamo.id == db_pago.prestamo_id).first()
    pagos_pendientes = db.query(Pago).filter(
        Pago.prestamo_id == prestamo.id,
        Pago.estado == EstadoPago.PENDIENTE
    ).count()
    
    if pagos_pendientes == 0:
        prestamo.estado = EstadoPrestamo.COMPLETADO
        db.commit()
    
    return db_pago

@router.get("/atrasados", response_model=List[PagoSchema])
async def get_pagos_atrasados(
    db: Session = Depends(get_db),
    current_user: Prestamo = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener lista de pagos atrasados
    🇺🇸 Get list of overdue payments
    """
    pagos_atrasados = db.query(Pago).filter(
        Pago.fecha_programada < datetime.utcnow(),
        Pago.estado == EstadoPago.PENDIENTE
    ).all()
    return pagos_atrasados 