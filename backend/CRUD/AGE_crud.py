from sqlalchemy.orm import Session
from ..models import AGE_model
from ..schemas import AGE_schema

 

# OBTENER TODOS LOS AGENTES 
def get_agentes(db: Session):
    return db.query(AGE_model.Agente).all()

# FILTRAR AGENTE POR NIT 
def get_agente_NIT(db: Session, NIT: str):
    return db.query(AGE_model.Agente).filter(AGE_model.Agente.NIT == NIT).first()

# FILTRAR AGENTE POR ASIC 
def get_agente(db: Session, ASIC: str):
    return db.query(AGE_model.Agente).filter(AGE_model.Agente.ASIC == ASIC).first()

# FILTRAR AGENTE POR Razon_Social 
def get_agente_Razon_Social(db: Session, Razon_Social: str):
    return db.query(AGE_model.Agente).filter(AGE_model.Agente.Razon_Social == Razon_Social).first()

# CREAR AGENTE 
def create_agente(db: Session, agente: AGE_schema.Agente_Create):
    db_ = AGE_model.Agente(**agente.dict())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR AGENTE 
def update_agente(db: Session, agente: AGE_schema.Agente_Update, ASIC: str):
    db_ = get_agente(db, ASIC)
    data = agente.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR AGENTE 
def delete_agente(db: Session, ASIC: str):
    db_A = get_agente(db, ASIC)
    db.delete(db_A)
    db.commit()
    return {f"Agente {ASIC} eliminado"}