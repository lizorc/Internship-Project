from datetime import date
from sqlalchemy.orm import Session
from ..models import VAL_model
from ..schemas import VAL_schema


 
# OBTENER TODOS LOS VALORES
def get_valores(db: Session):
    return db.query(VAL_model.Valor).all()

# FILTRAR VALOR POR TIPO
def get_Tipo_valor(db: Session, Tipo: str):
    return db.query(VAL_model.Valor).filter(VAL_model.Valor.Tipo == Tipo).all()

# FILTRAR VALOR POR PERIODO
def get_Periodo_valor(db: Session, Periodo: date):
    return db.query(VAL_model.Valor).filter(VAL_model.Valor.Periodo == Periodo).all()

# FILTRAR VALOR POR PERIODO Y TIPO
def get_valor(db: Session, Periodo: date, Tipo: str):
    return db.query(VAL_model.Valor).filter(VAL_model.Valor.Periodo == Periodo).filter(VAL_model.Valor.Tipo == Tipo).first()

# FILTRAR VALOR POR ID
def get_valor_ID(db: Session, ID: int):
    return db.query(VAL_model.Valor).filter(VAL_model.Valor.ID == ID).first()

# FILTRAR VALOR POR ID
def get_valor_ID_periodo(db: Session, ID: int):
    return db.query(VAL_model.Valor.Periodo).filter(VAL_model.Valor.ID == ID).first()._asdict()

# FILTRAR VALOR POR ID
def get_valor_ID_tipo(db: Session, ID: int):
    return db.query(VAL_model.Valor.Tipo).filter(VAL_model.Valor.ID == ID).first()._asdict()

# CONSULTAR DATO DE VALOR EN VALOR
def get_valor_Valor(db: Session, Periodo: date, Tipo: str):
    return db.query(VAL_model.Valor.Valor).filter(VAL_model.Valor.Periodo == Periodo).filter(VAL_model.Valor.Tipo == Tipo).first()._asdict()

# CREAR VALOR
def create_valor(db: Session, Val: VAL_schema.Valor_Create):
    db_ = VAL_model.Valor(**Val.dict())
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR VALOR
def update_valor(db: Session, Val: VAL_schema.Valor_Update, Periodo: date, Tipo: str):
    db_ = get_valor(db, Periodo, Tipo)
    data = Val.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR VALOR
def delete_valor(db: Session, Periodo: date, Tipo: str):
    db_ = get_valor(db, Periodo, Tipo)
    db.delete(db_)
    db.commit()
    return {f"Valor del Periodo {Periodo} y Tipo {Tipo} eliminado"}