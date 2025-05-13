"""
🇪🇸 Router para la gestión de clientes
🇺🇸 Router for client management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.cliente import Cliente
from ..schemas.cliente import ClienteCreate, ClienteUpdate, Cliente as ClienteSchema
from ..utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ClienteSchema)
async def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_active_user)
):
    """
    🇪🇸 Crear un nuevo cliente
    🇺🇸 Create a new client
    """
    db_cliente = db.query(Cliente).filter(Cliente.cedula == cliente.cedula).first()
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cédula ya está registrada"
        )
    
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=List[ClienteSchema])
async def get_clientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener lista de clientes
    🇺🇸 Get list of clients
    """
    clientes = db.query(Cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/{cliente_id}", response_model=ClienteSchema)
async def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_active_user)
):
    """
    🇪🇸 Obtener un cliente por ID
    🇺🇸 Get a client by ID
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return cliente

@router.put("/{cliente_id}", response_model=ClienteSchema)
async def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_active_user)
):
    """
    🇪🇸 Actualizar un cliente
    🇺🇸 Update a client
    """
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    for field, value in cliente.dict(exclude_unset=True).items():
        setattr(db_cliente, field, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Cliente = Depends(get_current_active_user)
):
    """
    🇪🇸 Eliminar un cliente
    🇺🇸 Delete a client
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    db.delete(cliente)
    db.commit()
    return None 