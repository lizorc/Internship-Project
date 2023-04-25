from datetime import date
from sqlalchemy.orm import Session
from ..models import DA_EXP_model
from ..schemas import DA_EXP_schema
from .PRO_crud import *


 
# OBTENER TODOS LOS DATOS EXPANSIONES STR
def get_dato_expansiones_OR_STR(db: Session):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR).all()

# FILTRAR DATO EXPANSION OR STR POR ID 
def get_dato_expansion_OR_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()

# FILTRAR DATO EXPANSION OR STR POR PROYECTO
def get_dato_expansion_OR_STR_proyecto(db: Session, Proyecto: str):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR).filter(DA_EXP_model.Dato_Expansion_OR_STR.Proyecto == Proyecto).all()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_dato_expansion_OR_STR_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR).filter(DA_EXP_model.Dato_Expansion_OR_STR.Proyecto == Proyecto
    ).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_ID_dato_expansion_OR_STR_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.ID).filter(DA_EXP_model.Dato_Expansion_OR_STR.Proyecto == Proyecto
    ).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()._asdict()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_dato_expansion_OR_STR_periodo(db: Session, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()

# CONSULTAR DATO DE PROYECTO EN DATO AMPLIACION
def get_Proyecto_Dato_Exp_OR_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.Proyecto).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE BRAEN EN DATO EXPANSION OR STR
def get_BRAEN_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.BRAEN).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE TASA RETORNO EN DATO EXPANSION OR STR
def get_Tasa_Retorno_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.Tasa_Retorno).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE BRAEN EN DATO EXPANSION OR STR
def get_BRAEN_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.BRAEN).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE RC EN DATO EXPANSION OR STR
def get_RC_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.RC).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE BRT EN DATO EXPANSION OR STR
def get_BRT_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.BRT).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE NE EN DATO EXPANSION OR STR
def get_NE_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.NE).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE BRA IAOM EN DATO EXPANSION OR STR
def get_BRA_IAOM_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.BRA_IAOM).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE FECHA INICIO VIGENCIA EN DATO CONVOCATORIA
def get_Inicio_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Inicio_Vigen).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CONSULTAR DATO DE FECHA FIN VIGENCIA EN DATO CONVOCATORIA
def get_Fin_Dato_Exp_STR(db: Session, Dato_Exp_id: int):
    return db.query(DA_EXP_model.Dato_Expansion_OR_STR.Fecha_Fin_Vigen).filter(DA_EXP_model.Dato_Expansion_OR_STR.ID == Dato_Exp_id).first()._asdict()

# CREAR DATO EXPANSION OR STR ASOCIADO A UNA LIQ
def create_dato_expansion_OR_STR_en_proyecto(db: Session, Dato_Exp_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Create, Proyecto: str):
    db_ = DA_EXP_model.Dato_Expansion_OR_STR(**Dato_Exp_STR.dict(), Proyecto = Proyecto)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR DATO EXPANSION OR STR
def update_dato_expansion_OR_STR(db: Session, Dato_Exp_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Update, Dato_Exp_id: int):
    db_ = get_dato_expansion_OR_STR(db, Dato_Exp_id)
    data = Dato_Exp_STR.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR DATO EXPANSION OR STR
def delete_dato_expansion_OR_STR(db: Session, Dato_Exp_id: int):
    db_ = get_dato_expansion_OR_STR(db, Dato_Exp_id)
    db.delete(db_)
    db.commit()
    return {f"Dato Expansión OR STR {Dato_Exp_id} eliminada"}