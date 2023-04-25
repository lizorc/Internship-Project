from datetime import date
from sqlalchemy.orm import Session
from ..models import DA_AMP_model
from ..schemas import DA_AMP_schema
from .PRO_crud import *


 
# OBTENER TODOS LOS DATOS AMPLIACIONES STN
def get_dato_ampliaciones_STN(db: Session):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN).all()

# FILTRAR DATO AMPLIACION STN PROYECTO y PERIODO
def get_dato_ampliacion_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()

# FILTRAR DATO AMPLIACION STN PROYECTO
def get_dato_ampliacion_STN_proyecto(db: Session, Proyecto: str):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN).filter(DA_AMP_model.Dato_Ampliacion_STN.Proyecto == Proyecto).all()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_dato_ampliacion_STN_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN).filter(DA_AMP_model.Dato_Ampliacion_STN.Proyecto == Proyecto
    ).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_ID_dato_ampliacion_STN_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.ID).filter(DA_AMP_model.Dato_Ampliacion_STN.Proyecto == Proyecto
    ).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()._asdict()

# FILTRAR DATO AMPLIACION POR PROYECTO
def get_dato_ampliacion_STN_periodo(db: Session, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Fin_Vigen == Fecha_Fin_Vigen).all()

# CONSULTAR DATO DE PROYECTO EN DATO AMPLIACION
def get_Proyecto_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.Proyecto).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE IAT EN DATO AMPLIACION STN
def get_IAT_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.IAT).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE CRE EN DATO AMPLIACION STN
def get_CRE_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.CRE).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE PAOMR ACTUAL EN DATO AMPLIACION STN
def get_PAOMR_Actual_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.PAOMR_Actual).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE PAOMR APROBADO EN DATO AMPLIACION STN
def get_PAOMR_Aprobado_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.PAOMR_Aprobado).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE FECHA INICIO VIGENCIA EN DATO CONVOCATORIA
def get_Inicio_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Inicio_Vigen).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CONSULTAR DATO DE FECHA FIN VIGENCIA EN DATO CONVOCATORIA
def get_Fin_Dato_Amp_STN(db: Session, Dato_Amp_id: int):
    return db.query(DA_AMP_model.Dato_Ampliacion_STN.Fecha_Fin_Vigen).filter(DA_AMP_model.Dato_Ampliacion_STN.ID == Dato_Amp_id).first()._asdict()

# CREAR DATO AMPLIACION STN ASOCIADO A UNA LIQ
def create_dato_ampliacion_STN_en_proyecto(db: Session, Dato_Amp_STN: DA_AMP_schema.Dato_Ampliacion_STN_Create, Proyecto: str):
    db_ = DA_AMP_model.Dato_Ampliacion_STN(**Dato_Amp_STN.dict(), Proyecto = Proyecto)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR DATO AMPLIACION STN
def update_dato_ampliacion_STN(db: Session, Dato_Amp_STN: DA_AMP_schema.Dato_Ampliacion_STN_Update, Dato_Amp_id: int):
    db_ = get_dato_ampliacion_STN(db, Dato_Amp_id)
    data = Dato_Amp_STN.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR DATO AMPLIACION STN
def delete_dato_ampliacion_STN(db: Session, Dato_Amp_id: int):
    db_ = get_dato_ampliacion_STN(db, Dato_Amp_id)
    db.delete(db_)
    db.commit()
    return {f"Dato Ampliación STN {Dato_Amp_id} eliminada"}