from datetime import date
from ..models import AMP_STN_model
from sqlalchemy.orm import Session
from ..schemas import AMP_STN_schema
from ..CRUD import PRO_crud, LIQ_crud
from ..validations import AMP_STN_validation, GENERAL_validation



# OBTENER TODOS LAS AMPLIACIONES STN
def get_ampliaciones_STN(db: Session):
    return db.query(AMP_STN_model.Ampliacion_STN).all()

# FILTRAR AMPLIACION STN POR AGENTE 
def get_ampliacion_STN_agente(db: Session, Agente: str):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.Agente == Agente).all()

# FILTRAR AMPLIACION STN POR ID 
def get_ampliacion_STN(db: Session, Amp_id: int):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.ID == Amp_id).first()

# FILTRAR AMPLIACION STN POR PROYECTO 
def get_ampliacion_STN_proyecto(db: Session, Proyecto: str):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.Proyecto == Proyecto).all()

# FILTRAR AMPLIACION STN POR PERIODO
def get_ampliacion_STN_liquidacion_PPA(db: Session, Liquidacion: date):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.Liquidacion == Liquidacion).all()

# FILTRAR AMPLIACION STN POR ID 
def get_version_ampliacion_STN(db: Session, Amp_id: int):
    return db.query(AMP_STN_model.Ampliacion_STN.Version).filter(AMP_STN_model.Ampliacion_STN.ID == Amp_id).first()._asdict()

# FILTRAR CONVOCATORIA STN POR ID 
def get_proyecto_ampliacion_STN(db: Session, Amp_id: int):
    return db.query(AMP_STN_model.Ampliacion_STN.Proyecto).filter(AMP_STN_model.Ampliacion_STN.ID == Amp_id).first()._asdict()

# FILTRAR CONVOCATORIA STN POR ID 
def get_liquidacion_ampliacion_STN(db: Session, Amp_id: int):
    return db.query(AMP_STN_model.Ampliacion_STN.Liquidacion).filter(AMP_STN_model.Ampliacion_STN.ID == Amp_id).first()._asdict()

# FILTRAR LIQUIDACION POR PERIODO LIMITES
def get_ampliacion_STN_liquidacion_rango(db: Session, Fecha_Desde: date, Fecha_Hasta: date):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.Liquidacion.between(Fecha_Desde, Fecha_Hasta)).all()

# FILTRAR AMPLIACION STN POR PROYECTO Y PERIODO
def get_ampliacion_STN_proyecto_liquidacion_PPA(db: Session, Proyecto: str, Liquidacion: date):
    return db.query(AMP_STN_model.Ampliacion_STN).filter(AMP_STN_model.Ampliacion_STN.Proyecto == Proyecto).filter(AMP_STN_model.Ampliacion_STN.Liquidacion == Liquidacion).all()

# FILTRAR CONVOCATORIA STN POR ID 
def get_Liq_ampliacion_STN(db: Session,  Proyecto: str, Liquidacion: date, Version):
    return db.query(AMP_STN_model.Ampliacion_STN.Liquidacion).filter(AMP_STN_model.Ampliacion_STN.Proyecto == Proyecto).filter(AMP_STN_model.Ampliacion_STN.Liquidacion == Liquidacion).filter(AMP_STN_model.Ampliacion_STN.Version == Version).first()
from fastapi import HTTPException
# CREAR PPA AMPLIACION STN DESDE LIQ PPA
def create_ampliacion_STN_grupo(db: Session, Agente: str, Proyecto: str, Liquidacion: date, Version: str):
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    Datos = AMP_STN_validation.Buscar_datos_Amp_STN(db, Proyecto, Liquidacion)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    db_ = AMP_STN_model.Ampliacion_STN(Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = Agente, IAT = Datos.IAT, CRE = Datos.CRE, PAOMR_Actual = Datos.PAOMR_Actual, PAOMR_Aprobado = Datos.PAOMR_Aprobado, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = AMP_STN_validation.calcular_Amp_STN(db, get_PB, IPP_Actual, get_DA, Liquidacion, Proyecto)
    return calculo

# CREAR PPA AMPLIACION STN SOLO LIQ PPA
def create_ampliacion_STN_individual(db: Session, Proyecto: str, Liquidacion: date, Version: str):
    get_AG = LIQ_crud.get_Agente_liquidacion_PPA(db, Proyecto)
    get_R = LIQ_crud.get_Rol_liquidacion_PPA(db, Proyecto)
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    Datos = AMP_STN_validation.Buscar_datos_Amp_STN(db, Proyecto, Liquidacion)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, Liquidacion)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, Liquidacion)
    db_ = AMP_STN_model.Ampliacion_STN(Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = get_AG, IAT = Datos.IAT, CRE = Datos.CRE, PAOMR_Actual = Datos.PAOMR_Actual, PAOMR_Aprobado = Datos.PAOMR_Aprobado, IPP_Actual = IPP_Actual, Dias_Atraso = get_DA)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = AMP_STN_validation.calcular_Amp_STN(db, get_PB, IPP_Actual, get_DA, Liquidacion, Proyecto)
    liq = LIQ_crud.get_liquidacion_PPA(db, Proyecto, Liquidacion, Version)
    liq.Valor_PPA = calculo
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR AMPLIACION STN
def update_ampliacion_STN(db: Session, Amp_id: int):
    db_ = get_ampliacion_STN(db, Amp_id)
    #data = Amp_STN.dict(exclude_unset = True)
    #for key, value in data.items():
    #    setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)

    get_PO = get_proyecto_ampliacion_STN(db, Amp_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_ampliacion_STN(db, Amp_id)
    FO = PRO_crud.get_FO_CP(db, get_PO)
    FR = PRO_crud.get_FR_CP(db, get_PO)
    get_DA = GENERAL_validation.calcular_atraso(FO, FR, get_FA)
    Datos = AMP_STN_validation.Buscar_datos_Amp_STN(db, get_PO, get_FA)
    IPP_Actual = GENERAL_validation.Buscar_IPP(db, get_FA)
    db_.Dias_A = get_DA
    db_.IAT = Datos.IAT
    db_.CRE = Datos.CRE
    db_.PAOMR_Actual = Datos.PAOMR_Actual
    db_.PAOMR_Aprobado = Datos.PAOMR_Aprobado
    db.commit
    get_PB = PRO_crud.get_Precio_CP(db, get_PO)
    calculo = AMP_STN_validation.actualizar_Amp_STN(db, get_PB, IPP_Actual, get_DA, get_FA, get_PO)
    Version = get_version_ampliacion_STN(db, Amp_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = calculo
    db.commit()
    return db_

# ELIMINAR AMPLIACION STN
def delete_ampliacion_STN(db: Session, Amp_id: int):
    get_PO = get_proyecto_ampliacion_STN(db, Amp_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_ampliacion_STN(db, Amp_id)
    get_FA = get_FA.get("Liquidacion")
    Version = get_version_ampliacion_STN(db, Amp_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = 0
    db.commit()
    db_ = get_ampliacion_STN(db, Amp_id)
    db.delete(db_)
    db.commit()
    return {f"Ampliación STN {Amp_id} eliminada"}
