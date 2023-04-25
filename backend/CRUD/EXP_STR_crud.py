from datetime import date
from sqlalchemy.orm import Session
from ..models import EXP_STR_model
from ..schemas import EXP_STR_schema
from ..CRUD import PRO_crud, LIQ_crud
from ..validations import EXP_STR_validation, GENERAL_validation



# OBTENER TODOS LAS AMPLIACIONES STR
def get_expansiones_OR_STR(db: Session):
    return db.query(EXP_STR_model.Expansion_OR_STR).all()

# FILTRAR EXPANSION OR STR POR AGENTE 
def get_expansion_OR_STR_agente(db: Session, Agente: str):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.Agente == Agente).all()

# FILTRAR EXPANSION OR STR POR ID 
def get_expansion_OR_STR(db: Session, Exp_STR_id: int):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.ID == Exp_STR_id).first()

# FILTRAR EXPANSION OR STR POR PROYECTO 
def get_expansion_OR_STR_proyecto(db: Session, Proyecto: str):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.Proyecto == Proyecto).all()

# FILTRAR EXPANSION OR STR POR PERIODO
def get_expansion_OR_STR_liquidacion(db: Session, Liquidacion: date):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.Liquidacion == Liquidacion).all()

# FILTRAR EXPANSION OR STR POR ID 
def get_version_expansion_OR_STR(db: Session, Exp_STR_id: int):
    return db.query(EXP_STR_model.Expansion_OR_STR.Version).filter(EXP_STR_model.Expansion_OR_STR.ID == Exp_STR_id).first()._asdict()

# FILTRAR EXPANSION OR STR POR ID 
def get_proyecto_expansion_OR_STR(db: Session, Exp_STR_id: int):
    return db.query(EXP_STR_model.Expansion_OR_STR.Proyecto).filter(EXP_STR_model.Expansion_OR_STR.ID == Exp_STR_id).first()._asdict()

# FILTRAR EXPANSION OR STR POR ID 
def get_liquidacion_expansion_OR_STR(db: Session, Exp_STR_id: int):
    return db.query(EXP_STR_model.Expansion_OR_STR.Liquidacion).filter(EXP_STR_model.Expansion_OR_STR.ID == Exp_STR_id).first()._asdict()

# FILTRAR LIQUIDACION POR PERIODO LIMITES
def get_expansion_OR_STR_liquidacion_rango(db: Session, Fecha_Desde: date, Fecha_Hasta: date):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.Liquidacion.between(Fecha_Desde, Fecha_Hasta)).all()

# FILTRAR EXPANSION OR STR POR PROYECTO Y PERIODO
def get_expansion_OR_STR_proyecto_liquidacion(db: Session, Proyecto: str, Liquidacion: date):
    return db.query(EXP_STR_model.Expansion_OR_STR).filter(EXP_STR_model.Expansion_OR_STR.Proyecto == Proyecto).filter(EXP_STR_model.Expansion_OR_STR.Liquidacion == Liquidacion).all()

# CONSULTAR LIQUIDACION EN EXPANSION OR STR
def get_Liq_expansion_OR_STR(db: Session, Proyecto: str, Liquidacion: date, Version):
    return db.query(EXP_STR_model.Expansion_OR_STR.Liquidacion).filter(EXP_STR_model.Expansion_OR_STR.Proyecto == Proyecto).filter(EXP_STR_model.Expansion_OR_STR.Liquidacion == Liquidacion).filter(EXP_STR_model.Expansion_OR_STR.Version == Version).first()

# CREAR EXPANSION OR STR DESDE LIQ PPA
def create_expansion_OR_STR_grupo(db: Session, Agente: str, Proyecto: str, Liquidacion: date, Version: str):
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    get_IAA = EXP_STR_validation.calcular_IAA(db, Liquidacion, Proyecto)
    get_IAOM = EXP_STR_validation.calcular_IAOM(db, Liquidacion, Proyecto)
    get_FM = EXP_STR_validation.calcular_FM(db, Liquidacion, Proyecto)
    db_ = EXP_STR_model.Expansion_OR_STR(Liquidacion = Liquidacion, Proyecto = Proyecto, Agente = Agente, Version = Version, IAA = get_IAA, IAOM = get_IAOM, FM = get_FM, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = EXP_STR_validation.calcular_Exp_STR(get_PB, IPP_Actual, get_DA, Liquidacion, get_IAA, get_IAOM, get_FM)
    return calculo

# CREAR EXPANSION OR STR SOLO LIQ PPA
def create_expansion_OR_STR_individual(db: Session, Proyecto: str, Liquidacion: date, Version: str):
    get_AG = LIQ_crud.get_Agente_liquidacion_PPA(db, Proyecto)
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    get_IAA = EXP_STR_validation.calcular_IAA(db, Liquidacion, Proyecto)
    get_IAOM = EXP_STR_validation.calcular_IAOM(db, Liquidacion, Proyecto)
    get_FM = EXP_STR_validation.calcular_FM(db, Liquidacion, Proyecto)
    db_ = EXP_STR_model.Expansion_OR_STR(Liquidacion = Liquidacion, Proyecto = Proyecto, Agente = get_AG, Version = Version, IAA = get_IAA, IAOM = get_IAOM, FM = get_FM, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = EXP_STR_validation.calcular_Exp_STR(get_PB, IPP_Actual, get_DA, Liquidacion, get_IAA, get_IAOM, get_FM)
    liq = LIQ_crud.get_liquidacion_PPA(db, Proyecto, Liquidacion, Version)
    liq.Valor_PPA = calculo
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_


# ACTUALIZAR EXPANSION OR STR
def update_expansion_OR_STR(db: Session, Exp_STR_id: int):
    db_ = get_expansion_OR_STR(db, Exp_STR_id)

    get_PO = get_proyecto_expansion_OR_STR(db, Exp_STR_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_expansion_OR_STR(db, Exp_STR_id)
    FO = PRO_crud.get_FO_CP(db, get_PO)
    FR = PRO_crud.get_FR_CP(db, get_PO)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, get_FA)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, get_FA)
    get_IAA = EXP_STR_validation.calcular_IAA(db, get_FA, get_PO)
    get_IAOM = EXP_STR_validation.calcular_IAOM(db, get_FA, get_PO)
    get_FM = EXP_STR_validation.calcular_FM(db, get_FA, get_PO)
    db_.Dias_A = get_DA
    db_.IAA = get_IAA
    db_.IAOM = get_IAOM
    db_.FM = get_FM
    db.commit
    get_PB = PRO_crud.get_Precio_CP(db, get_PO)
    calculo = EXP_STR_validation.calcular_Exp_STR(get_PB, IPP_Actual, get_DA, get_FA, get_IAA, get_IAOM, get_FM)
    Version = get_version_expansion_OR_STR(db, Exp_STR_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = calculo
    db.commit()
    return db_

# ELIMINAR EXPANSION OR STR
def delete_expansion_OR_STR(db: Session, Exp_STR_id: int):
    get_PO = get_proyecto_expansion_OR_STR(db, Exp_STR_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_expansion_OR_STR(db, Exp_STR_id)
    get_FA = get_FA.get("Liquidacion")
    Version = get_version_expansion_OR_STR(db, Exp_STR_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = 0
    db.commit()
    db_ = get_expansion_OR_STR(db, Exp_STR_id)
    db.delete(db_)
    db.commit()
    return {f"Expansión OR STR {Exp_STR_id} eliminada"}