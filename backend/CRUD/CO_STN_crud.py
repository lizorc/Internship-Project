from datetime import date
from ..models import CO_STN_model
from sqlalchemy.orm import Session
from ..schemas import CO_STN_schema
from ..CRUD import PRO_crud, LIQ_crud
from ..validations import CO_STN_validation, GENERAL_validation



# OBTENER TODOS LAS CONVOCATORIAS STN
def get_convocatorias_STN(db: Session):
    return db.query(CO_STN_model.Convocatoria_STN).all()

# FILTRAR CONVOCATORIA STN POR AGENTE 
def get_convocatoria_STN_agente(db: Session, Agente: str):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.Agente == Agente).all()

# FILTRAR CONVOCATORIA STN POR ID 
def get_convocatoria_STN(db: Session, Conv_STN_id: int):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.ID == Conv_STN_id).first()

# FILTRAR CONVOCATORIA STN POR PROYECTO 
def get_convocatoria_STN_proyecto(db: Session, Proyecto: str):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.Proyecto == Proyecto).all()

# FILTRAR CONVOCATORIA STN POR PERIODO
def get_convocatoria_STN_liquidacion_PPA(db: Session, Liquidacion: date):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.Liquidacion == Liquidacion).all()

# FILTRAR CONVOCATORIA STN POR ID 
def get_version_convocatoria_STN(db: Session, Conv_STN_id: int):
    return db.query(CO_STN_model.Convocatoria_STN.Version).filter(CO_STN_model.Convocatoria_STN.ID == Conv_STN_id).first()._asdict()

# FILTRAR CONVOCATORIA STN POR ID 
def get_proyecto_convocatoria_STN(db: Session, Conv_STN_id: int):
    return db.query(CO_STN_model.Convocatoria_STN.Proyecto).filter(CO_STN_model.Convocatoria_STN.ID == Conv_STN_id).first()._asdict()

# FILTRAR CONVOCATORIA STN POR ID 
def get_liquidacion_convocatoria_STN(db: Session, Conv_STN_id: int):
    return db.query(CO_STN_model.Convocatoria_STN.Liquidacion).filter(CO_STN_model.Convocatoria_STN.ID == Conv_STN_id).first()._asdict()

# FILTRAR LIQUIDACION POR PERIODO LIMITES
def get_convocatoria_STN_liquidacion_PPA_rango(db: Session, Fecha_Desde: date, Fecha_Hasta: date):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.Liquidacion.between(Fecha_Desde, Fecha_Hasta)).all()

# FILTRAR CONVOCATORIA STN POR PROYECTO Y PERIODO
def get_convocatoria_STN_proyecto_liquidacion_PPA(db: Session, Proyecto: str, Liquidacion: date):
    return db.query(CO_STN_model.Convocatoria_STN).filter(CO_STN_model.Convocatoria_STN.Proyecto == Proyecto).filter(CO_STN_model.Convocatoria_STN.Liquidacion == Liquidacion).all()

# FILTRAR CONVOCATORIA STN POR ID 
def get_liq_convocatoria_STN(db: Session, Proyecto: str, Liquidacion: date, Version):
    return db.query(CO_STN_model.Convocatoria_STN.Liquidacion).filter(CO_STN_model.Convocatoria_STN.Proyecto == Proyecto).filter(CO_STN_model.Convocatoria_STN.Liquidacion == Liquidacion).filter(CO_STN_model.Convocatoria_STN.Version == Version).first()

# CREAR CONVOCATORIA STN DESDE LIQ PPA
def create_convocatoria_STN_grupo(db: Session, Agente: str, Rol: str, Proyecto: str, Liquidacion: date, Version: str):
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    get_TP = CO_STN_validation.calcular_tipo_proyecto(Rol)
    Datos = CO_STN_validation.Buscar_datos_Conv_STN(db, Proyecto, Liquidacion)
    TRM = GENERAL_validation.Buscar_TRM(db, Liquidacion)
    get_DA = CO_STN_validation.calcular_atraso_Conv_STN(FO, FR, Liquidacion)
    db_ = CO_STN_model.Convocatoria_STN(Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = Agente, Rol_Agente = Rol, Anualidad = Datos.Anualidad, Porcentaje = Datos.Porcentaje, PPI_Actual = Datos.PPI_Actual, TRM = TRM, Factor_Generador = 1, Dias_Atraso = get_DA, Capacidad_O = 0, Capacidad_T = 0)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    calculo = CO_STN_validation.calcular_Conv_STN(db, get_TP, 1, get_PB, get_DA, TRM, Liquidacion, Proyecto)
    return calculo

# CREAR CONVOCATORIA STN SOLO LIQ PPA
def create_convocatoria_STN_individual(db: Session, Conv_STN: CO_STN_schema.Convocatoria_STN_Create, Proyecto: str, Liquidacion: date, Version: str):
    get_AG = LIQ_crud.get_Agente_liquidacion_PPA(db, Proyecto)
    get_R = LIQ_crud.get_Rol_liquidacion_PPA(db, Proyecto)
    FO = PRO_crud.get_FO_CP(db, Proyecto)
    FR = PRO_crud.get_FR_CP(db, Proyecto)
    Rol = LIQ_crud.get_Rol_LiqPro(db, Proyecto)
    Datos = CO_STN_validation.Buscar_datos_Conv_STN(db, Proyecto, Liquidacion)
    TRM = GENERAL_validation.Buscar_TRM(db, Liquidacion)
    get_FG = CO_STN_validation.llenar_factor_generador(Conv_STN, Rol) 
    get_DA = CO_STN_validation.calcular_atraso_Conv_STN(FO, FR, Liquidacion)
    db_ = CO_STN_model.Convocatoria_STN(**Conv_STN.dict(), Liquidacion = Liquidacion, Proyecto = Proyecto, Version = Version, Agente = get_AG, Rol_Agente = get_R, Anualidad = Datos.Anualidad, Porcentaje = Datos.Porcentaje, PPI_Actual = Datos.PPI_Actual, TRM = TRM, Factor_Generador = get_FG, Dias_Atraso = get_DA)
    get_PB = PRO_crud.get_Precio_CP(db, Proyecto)
    get_TP = CO_STN_validation.calcular_tipo_proyecto(Rol)
    calculo = CO_STN_validation.calcular_Conv_STN(db, get_TP, get_FG, get_PB, get_DA, TRM, Liquidacion, Proyecto)
    liq = LIQ_crud.get_liquidacion_PPA(db, Proyecto, Liquidacion, Version)
    liq.Valor_PPA = calculo
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR CONVOCATORIA STN
def update_convocatoria_STN(db: Session, Conv_STN: CO_STN_schema.Convocatoria_STN_Update, Conv_STN_id: int):
    db_ = get_convocatoria_STN(db, Conv_STN_id)
    data = Conv_STN.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)

    get_PO = get_proyecto_convocatoria_STN(db, Conv_STN_id)
    get_PO = get_PO.get("Proyecto")
    get_FO = PRO_crud.get_FO_CP(db, get_PO)
    get_FR = PRO_crud.get_FR_CP(db, get_PO)
    get_FA = get_liquidacion_convocatoria_STN(db, Conv_STN_id)
    get_Rol = LIQ_crud.get_Rol_LiqPro(db, get_PO)
    get_DA = CO_STN_validation.calcular_atraso_Conv_STN(get_FO, get_FR, get_FA)
    get_FG = CO_STN_validation.actu_factor_generador(Conv_STN, get_Rol)
    Datos = CO_STN_validation.Buscar_datos_Conv_STN(db, get_FA, get_PO)
    get_PB = PRO_crud.get_Precio_CP(db, get_PO)
    db_.Dias_Atraso = get_DA
    db_.Factor_Generador = get_FG
    db_.Anualidad = Datos.Anualidad
    db_.Porcentaje = Datos.Porcentaje
    db_.PPI_Actual = Datos.PPI_Actual
    db.commit
    get_TP = CO_STN_validation.calcular_tipo_proyecto(get_Rol)
    TRM = GENERAL_validation.Buscar_TRM(db, get_FA)
    calculo = CO_STN_validation.actualizar_Conv_STN(db, Conv_STN, get_TP, get_FG, get_PB, get_DA, TRM, get_FA, get_PO) 
    Version = get_version_convocatoria_STN(db, Conv_STN_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = calculo
    db.commit()
    return db_


# ELIMINAR CONVOCATORIA STN
def delete_convocatoria_STN(db: Session, Conv_STN_id: int):
    get_PO = get_proyecto_convocatoria_STN(db, Conv_STN_id)
    get_PO = get_PO.get("Proyecto")
    get_FA = get_liquidacion_convocatoria_STN(db, Conv_STN_id)
    get_FA = get_FA.get("Liquidacion")
    Version = get_version_convocatoria_STN(db, Conv_STN_id)
    Version = Version.get("Version")
    liq = LIQ_crud.get_liquidacion_PPA(db, get_PO, get_FA, Version)
    liq.Valor_PPA = 0
    db.commit()
    db_ = get_convocatoria_STN(db, Conv_STN_id)
    db.delete(db_)
    db.commit()
    return {f"Convocatoria STN {Conv_STN_id} eliminada"}