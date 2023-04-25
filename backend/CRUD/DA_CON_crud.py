from datetime import date
from sqlalchemy.orm import Session
from ..models import DA_CON_model
from ..schemas import DA_CON_schema
from ..validations import DA_CON_validation
from .PRO_crud import *


 
# OBTENER TODOS LOS DATOS CONVOCATORIAS
def get_datos_convocatorias(db: Session):
    return db.query(DA_CON_model.Dato_Convocatoria).all()

# FILTRAR DATO CONVOCATORIA POR ID 
def get_dato_convocatoria(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()

# FILTRAR DATO CONVOCATORIA POR PROYECTO
def get_dato_convocatoria_proyecto(db: Session, Proyecto: str):
    return db.query(DA_CON_model.Dato_Convocatoria).filter(DA_CON_model.Dato_Convocatoria.Proyecto == Proyecto).all()

# FILTRAR DATO CONVOCATORIA POR PROYECTO Y FECHAS
def get_dato_convocatoria_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_CON_model.Dato_Convocatoria).filter(DA_CON_model.Dato_Convocatoria.Proyecto == Proyecto
    ).filter(DA_CON_model.Dato_Convocatoria.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_CON_model.Dato_Convocatoria.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()

# FILTRAR ID DATO CONVOCATORIA POR PROYECTO Y FECHAS
def get_ID_dato_convocatoria_proyecto_periodo(db: Session, Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_CON_model.Dato_Convocatoria.ID).filter(DA_CON_model.Dato_Convocatoria.Proyecto == Proyecto
    ).filter(DA_CON_model.Dato_Convocatoria.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen
    ).filter(DA_CON_model.Dato_Convocatoria.Fecha_Fin_Vigen == Fecha_Fin_Vigen).first()._asdict()

# FILTRAR DATO CONVOCATORIA POR FECHAS
def get_dato_convocatoria_periodo(db: Session, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date):
    return db.query(DA_CON_model.Dato_Convocatoria).filter(DA_CON_model.Dato_Convocatoria.Fecha_Inicio_Vigen == Fecha_Inicio_Vigen).filter(DA_CON_model.Dato_Convocatoria.Fecha_Fin_Vigen == Fecha_Fin_Vigen).all()

# CONSULTAR DATO DE PROYECTO EN DATO CONVOCATORIA
def get_Proyecto_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.Proyecto).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()

# CONSULTAR DATO DE ANUALIDAD EN DATO CONVOCATORIA
def get_Anualidad_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.Anualidad).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()

# CONSULTAR DATO DE PORCENTAJE EN DATO CONVOCATORIA
def get_Porcentaje_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.Porcentaje).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()

# CONSULTAR DATO DE PORCENTAJE EN DATO CONVOCATORIA
def get_PPI_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.PPI).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()

# CONSULTAR DATO DE FECHA INICIO VIGENCIA EN DATO CONVOCATORIA
def get_Inicio_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.Fecha_Inicio_Vigen).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()

# CONSULTAR DATO DE FECHA FIN VIGENCIA EN DATO CONVOCATORIA
def get_Fin_Dato_Conv(db: Session, Dato_Conv_id: int):
    return db.query(DA_CON_model.Dato_Convocatoria.Fecha_Fin_Vigen).filter(DA_CON_model.Dato_Convocatoria.ID == Dato_Conv_id).first()._asdict()


# CREAR DATO CONVOCATORIA ASOCIADO A UNA LIQ
def create_dato_conv_en_proyecto(db: Session, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Create, Proyecto: str):
    get_C = get_Categoria_proyecto(db, Proyecto)
    db_ = DA_CON_model.Dato_Convocatoria(**Dato_Conv.dict(), Proyecto = Proyecto, Categoria = get_C)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR DATO CONVOCATORIA
def update_dato_conv(db: Session, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Update, Dato_Conv_id: int):
    db_ = get_dato_convocatoria(db, Dato_Conv_id)
    data = Dato_Conv.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR DATO CONVOCATORIA
def delete_dato_conv(db: Session, Dato_Conv_id: int):
    db_ = get_dato_convocatoria(db, Dato_Conv_id)
    db.delete(db_)
    db.commit()
    return {f"Dato Convocatoria {Dato_Conv_id} eliminada"}