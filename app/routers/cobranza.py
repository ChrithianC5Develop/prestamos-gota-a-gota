"""
🇪🇸 Router para la gestión de cobranzas
🇺🇸 Router for collection management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date, timedelta
from sqlalchemy.sql import func
from ..database import get_db
from ..models.cobranza import Cobranza, EstadoCobranza
from ..models.usuario import Usuario
from ..schemas.cobranza import (
    CobranzaCreate,
    CobranzaUpdate,
    Cobranza as CobranzaSchema,
    CobranzaResumen,
    RutaCobranza,
    AsignacionCobranza
)
from ..utils.auth import get_current_active_user, verificar_rol_cobrador

router = APIRouter()

@router.post("/", response_model=CobranzaSchema)
async def crear_cobranza(
    cobranza: CobranzaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Crea una nueva cobranza
    🇺🇸 Creates a new collection
    """
    # Verificar que el cobrador existe
    cobrador = db.query(Usuario).filter(Usuario.id == cobranza.cobrador_id).first()
    if not cobrador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cobrador no encontrado"
        )
    
    db_cobranza = Cobranza(**cobranza.dict())
    db.add(db_cobranza)
    db.commit()
    db.refresh(db_cobranza)
    return db_cobranza

@router.put("/{cobranza_id}", response_model=CobranzaSchema)
async def actualizar_cobranza(
    cobranza_id: int,
    cobranza: CobranzaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualiza una cobranza existente
    🇺🇸 Updates an existing collection
    """
    db_cobranza = db.query(Cobranza).filter(Cobranza.id == cobranza_id).first()
    if not db_cobranza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cobranza no encontrada"
        )
    
    for key, value in cobranza.dict(exclude_unset=True).items():
        setattr(db_cobranza, key, value)
    
    if cobranza.estado == EstadoCobranza.COMPLETADA:
        db_cobranza.fecha_realizada = datetime.utcnow()
    
    db.commit()
    db.refresh(db_cobranza)
    return db_cobranza

@router.get("/cobrador/{cobrador_id}", response_model=List[CobranzaSchema])
async def obtener_cobranzas_por_cobrador(
    cobrador_id: int,
    fecha: date,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene las cobranzas asignadas a un cobrador en una fecha
    🇺🇸 Gets collections assigned to a collector on a date
    """
    cobranzas = db.query(Cobranza).filter(
        Cobranza.cobrador_id == cobrador_id,
        Cobranza.fecha_programada >= fecha,
        Cobranza.fecha_programada < fecha + timedelta(days=1)
    ).all()
    return cobranzas

@router.get("/resumen", response_model=CobranzaResumen)
async def obtener_resumen(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene un resumen de las cobranzas en un período
    🇺🇸 Gets a collection summary for a period
    """
    # Conteos por estado
    estados = db.query(
        Cobranza.estado,
        func.count(Cobranza.id)
    ).filter(
        Cobranza.fecha_programada >= fecha_inicio,
        Cobranza.fecha_programada <= fecha_fin
    ).group_by(Cobranza.estado).all()
    
    estados_dict = dict(estados)
    
    # Montos totales
    montos = db.query(
        func.sum(Cobranza.monto_esperado).label("esperado"),
        func.sum(Cobranza.monto_recibido).label("recibido")
    ).filter(
        Cobranza.fecha_programada >= fecha_inicio,
        Cobranza.fecha_programada <= fecha_fin
    ).first()
    
    # Conteos por zona
    zonas = db.query(
        Cobranza.zona,
        func.count(Cobranza.id)
    ).filter(
        Cobranza.fecha_programada >= fecha_inicio,
        Cobranza.fecha_programada <= fecha_fin
    ).group_by(Cobranza.zona).all()
    
    # Conteos por cobrador
    cobradores = db.query(
        Usuario.nombre,
        func.count(Cobranza.id)
    ).join(Cobranza).filter(
        Cobranza.fecha_programada >= fecha_inicio,
        Cobranza.fecha_programada <= fecha_fin
    ).group_by(Usuario.nombre).all()
    
    return CobranzaResumen(
        total_pendientes=estados_dict.get(EstadoCobranza.PENDIENTE, 0),
        total_completadas=estados_dict.get(EstadoCobranza.COMPLETADA, 0),
        total_fallidas=estados_dict.get(EstadoCobranza.FALLIDA, 0),
        monto_total_esperado=montos.esperado or 0,
        monto_total_recibido=montos.recibido or 0,
        por_zona={zona: count for zona, count in zonas},
        por_cobrador={nombre: count for nombre, count in cobradores},
        por_estado={estado.value: estados_dict.get(estado, 0) for estado in EstadoCobranza}
    )

@router.post("/asignar", response_model=List[CobranzaSchema])
async def asignar_cobranzas(
    asignacion: AsignacionCobranza,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Asigna múltiples cobranzas a un cobrador
    🇺🇸 Assigns multiple collections to a collector
    """
    # Verificar que el cobrador existe
    cobrador = db.query(Usuario).filter(Usuario.id == asignacion.cobrador_id).first()
    if not cobrador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cobrador no encontrado"
        )
    
    # Actualizar las cobranzas
    cobranzas = db.query(Cobranza).filter(
        Cobranza.id.in_(asignacion.cobranza_ids)
    ).all()
    
    for cobranza in cobranzas:
        cobranza.cobrador_id = asignacion.cobrador_id
        if asignacion.fecha_programada:
            cobranza.fecha_programada = asignacion.fecha_programada
    
    db.commit()
    return cobranzas

@router.get("/ruta/{fecha}", response_model=List[RutaCobranza])
async def obtener_rutas_cobranza(
    fecha: date,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtiene las rutas de cobranza para una fecha
    🇺🇸 Gets collection routes for a date
    """
    rutas = db.query(Cobranza).filter(
        Cobranza.fecha_programada >= fecha,
        Cobranza.fecha_programada < fecha + timedelta(days=1)
    ).order_by(
        Cobranza.zona,
        Cobranza.cobrador_id,
        Cobranza.orden_ruta
    ).all()
    
    # Agrupar por zona y cobrador
    rutas_agrupadas = {}
    for cobranza in rutas:
        key = (cobranza.zona, cobranza.cobrador_id)
        if key not in rutas_agrupadas:
            rutas_agrupadas[key] = []
        rutas_agrupadas[key].append(cobranza)
    
    # Convertir a lista de RutaCobranza
    return [
        RutaCobranza(
            id=i,
            fecha=fecha,
            cobrador_id=cobrador_id,
            zona=zona,
            cobranzas=cobranzas
        )
        for i, ((zona, cobrador_id), cobranzas) in enumerate(rutas_agrupadas.items(), 1)
    ] 