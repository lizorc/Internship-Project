from datetime import date
from ..models import CO_STR_model
from sqlalchemy.orm import Session
from ..schemas import CO_STR_schema
from ..CRUD import PRO_crud, LIQ_crud
from ..validations import CO_STR_validation, GENERAL_validation



# OBTENER TODOS LAS CONVOCATORIAS STR
def get_convocatorias_STR(db: Session):
    return db.query(CO_STR_model.Convocatoria_STR).all()

# FILTRAR CONVOCATORIA STR POR AGENTE 
def get_convocatoria_STR_agente(db: Session, Agente: str):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.Agente == Agente).all()

# FILTRAR CONVOCATORIA STR POR ID 
def get_convocatoria_STR(db: Session, Conv_STR_id: int):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.ID == Conv_STR_id).first()

# FILTRAR CONVOCATORIA STR POR PROYECTO 
def get_convocatoria_STR_proyecto(db: Session, Proyecto: str):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.Proyecto == Proyecto).all()

# FILTRAR CONVOCATORIA STR POR PERIODO
def get_convocatoria_STR_liquidacion(db: Session, Liquidacion: date):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.Liquidacion == Liquidacion).all()

# FILTRAR CONVOCATORIA STR POR ID 
def get_version_convocatoria_STR(db: Session, Conv_STR_id: int):
    return db.query(CO_STR_model.Convocatoria_STR.Version).filter(CO_STR_model.Convocatoria_STR.ID == Conv_STR_id).first()._asdict()

# FILTRAR CONVOCATORIA STR POR ID 
def get_proyecto_convocatoria_STR(db: Session, Conv_STR_id: int):
    return db.query(CO_STR_model.Convocatoria_STR.Proyecto).filter(CO_STR_model.Convocatoria_STR.ID == Conv_STR_id).first()._asdict()

# FILTRAR CONVOCATORIA STR POR ID 
def get_liquidacion_convocatoria_STR(db: Session, Conv_STR_id: int):
    return db.query(CO_STR_model.Convocatoria_STR.Liquidacion).filter(CO_STR_model.Convocatoria_STR.ID == Conv_STR_id).first()._asdict()

# FILTRAR LIQUIDACION POR PERIODO LIMITES
def get_convocatoria_STR_liquidacion_rango(db: Session, Fecha_Desde: date, Fecha_Hasta: date):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.Liquidacion.between(Fecha_Desde, Fecha_Hasta)).all()

# FILTRAR CONVOCATORIA STR POR PROYECTO Y PERIODO
def get_convocatoria_STR_proyecto_liquidacion(db: Session, Proyecto: str, Liquidacion: date):
    return db.query(CO_STR_model.Convocatoria_STR).filter(CO_STR_model.Convocatoria_STR.Proyecto == Proyecto).filter(CO_STR_model.Convocatoria_STR.Liquidacion == Liquidacion).all()

# FILTRAR CONVOCATORIA STR POR PROYECTO Y PERIODO
def get_liq_convocatoria_STR(db: Session, Proyecto: str, Liquidacion: date, Version):
    return db.query(CO_STR_model.Convocatoria_STR.Liquidacion).filter(CO_STR_model.Convocatoria_STR.Proyecto == Proyecto).filter(CO_STR_model.Convocatoria_STR.Liquidacion == Liquidacion).filter(CO_STR_model.Convocatoria_STR.Version == Version).first()

# CREAR CONVOCATORIA STR DESDE LIQ PPA
def create_convocatoria_STR_grupo(db: Session, Agente: str, Rol: str, Proyecto: str, Liquidacion: date, Version: str):
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    Datos = CO_STR_validation.Buscar_datos_Conv(db, Proyecto, Liquidacion)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    db_ = CO_STR_model.Convocatoria_STR(Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = Agente, Rol_Agente = Rol, Anualidad = Datos.Anualidad, Porcentaje = Datos.Porcentaje, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = CO_STR_validation.calcular_Conv_STR(db, get_PB, get_DA, IPP_Actual, Liquidacion, Proyecto)
    return calculo

# CREAR CONVOCATORIA STR SOLO LIQ PPA
def create_convocatoria_STR_individual(db: Session, Proyecto: str, Liquidacion: date, Version: str):
    get_AG = LIQ_crud.get_Agente_liquidacion_PPA(db, Proyecto)
    get_R = LIQ_crud.get_Rol_liquidacion_PPA(db, Proyecto)
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    Datos = CO_STR_validation.Buscar_datos_Conv(db, Proyecto, Liquidacion)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    db_ = CO_STR_model.Convocatoria_STR(Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = get_AG, Rol_Agente = get_R, Anualidad = Datos.Anualidad, Porcentaje = Datos.Porcentaje, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = CO_STR_validation.calcular_Conv_STR(db, get_PB, get_DA, IPP_Actual, Liquidacion, Proyecto)
    liq = LIQ_crud.get_liquidacion_PPA(db, Proyecto, Liquidacion, Version)
    liq.Valor_PPA = calculo
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR CONVOCATORIA STR
def update_convocatoria_STR(db: Session, Conv_STR: CO_STR_schema.Convocatoria_STR, Conv_STR_id: int):
    db_ = get_convocatoria_STR(db, Conv_STR_id)
    data = Conv_STR.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)

    get_PO = get_proyecto_convocatoria_STR(db, Conv_STR_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_convocatoria_STR(db, Conv_STR_id)
    FO = PRO_crud.get_FO_CP(db, get_PO)
    FR = PRO_crud.get_FR_CP(db, get_PO)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, get_FA)
    Datos = CO_STR_validation.Buscar_datos_Conv(db, get_PO, get_FA)
    get_PB = PRO_crud.get_Precio_CP(db, get_PO)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, get_FA)
    db_.Dias_Atraso = get_DA
    db_.Anualidad = Datos.Anualidad
    db_.Porcentaje = Datos.Porcentaje
    db_.IPP_Actual = IPP_Actual
    db.commit
    calculo = CO_STR_validation.calcular_Conv_STR(db, get_PB, get_DA, IPP_Actual, get_FA, get_PO) 
    Version = get_version_convocatoria_STR(db, Conv_STR_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = calculo
    db.commit()
    return db_

# ELIMINAR CONVOCATORIA STR
def delete_convocatoria_STR(db: Session, Conv_STR_id: int):
    get_PO = get_proyecto_convocatoria_STR(db, Conv_STR_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_convocatoria_STR(db, Conv_STR_id)
    get_FA = get_FA.get("Liquidacion")
    Version = get_version_convocatoria_STR(db, Conv_STR_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = 0
    db.commit()
    db_ = get_convocatoria_STR(db, Conv_STR_id)
    db.delete(db_)
    db.commit()
    return {f"Convocatoria STR {Conv_STR_id} eliminada"}