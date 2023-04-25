from datetime import date
from sqlalchemy.orm import Session
from ..models import LIQ_model
from ..schemas import LIQ_schema
from ..CRUD import CO_STN_crud, CO_STR_crud, AMP_STN_crud, EXP_STR_crud
#from ..validations import LIQ_validation, GENERAL_validation
from .PRO_crud import *
from .SE_FPO_crud import *



# OBTENER TODOS LAS LIQUIDACION PPA
def get_liquidaciones_PPA(db: Session):
    return db.query(LIQ_model.Liquidacion_PPA).all()

# FILTRAR LIQUIDACION PPA POR PROYECTO, PERIODO Y VERSION
def get_liquidacion_PPA(db: Session, Proyecto: str, Periodo: date, Version: str):
    return db.query(LIQ_model.Liquidacion_PPA
    ).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto
    ).filter(LIQ_model.Liquidacion_PPA.Periodo == Periodo
    ).filter(LIQ_model.Liquidacion_PPA.Version == Version).first()

# FILTRAR LIQUIDACION PPA POR PROYECTO, PERIODO Y VERSION
def get_liquidacion_PPA_periodo_version_proceso(db: Session, Periodo: date, Version: str, Proceso: str):
    return db.query(LIQ_model.Liquidacion_PPA
    ).filter(LIQ_model.Liquidacion_PPA.Periodo == Periodo
    ).filter(LIQ_model.Liquidacion_PPA.Version == Version
    ).filter(LIQ_model.Liquidacion_PPA.Categoria == Proceso).first()

# FILTRAR LIQUIDACION PPA POR AGENTE
def get_liquidacion_PPA_agente(db: Session, Agente: str):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Agente == Agente).all()

# FILTRAR LIQUIDACION PPA POR PROYECTO
def get_liquidacion_PPA_proyecto(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto).all()

# FILTRAR LIQUIDACION PPA POR PERIODO
def get_liquidacion_PPA_periodo(db: Session, Periodo: date):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Periodo == Periodo).all()

# FILTRAR LIQUIDACION PPA POR PERIODO RANGO
def get_liquidacion_PPA_periodo_rango(db: Session, Fecha_Desde: date, Fecha_Hasta: date):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Periodo.between(Fecha_Desde, Fecha_Hasta)).all()

# FILTRAR LIQUIDACION PPA POR PROYECTO
def get_liquidacion_PPA_proyecto_periodo(db: Session, Proyecto: str, Periodo: date):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto).filter(LIQ_model.Liquidacion_PPA.Periodo == Periodo).all()

# FILTRAR LIQUIDACION PPA POR CATEGORIA
def get_liquidacion_PPA_categoria(db: Session, Categoria: str):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Categoria == Categoria).all()

# FILTRAR LIQUIDACION PPA POR SUBCATEGORIA
def get_liquidacion_PPA_subcategoria(db: Session, Subcategoria: str):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Subcategoria == Subcategoria).all()

# FILTRAR LIQUIDACION PPA POR CATEGORIA Y SUBCATEGORIA
def get_liquidacion_PPA_categoria_subcategoria(db: Session, Categoria: str, Subcategoria: str):
    return db.query(LIQ_model.Liquidacion_PPA).filter(LIQ_model.Liquidacion_PPA.Categoria == Categoria).filter(LIQ_model.Liquidacion_PPA.Subcategoria == Subcategoria).all()

# CONSULTA DE AGENTE EN LIQUIDACION PPA
def get_Agente_liquidacion_PPA(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA.Agente).select_from(LIQ_model.Liquidacion_PPA).where(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto)

# CONSULTA DE ROL AGENTE EN LIQUIDACION PPA
def get_Rol_liquidacion_PPA(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA.Rol_Agente).select_from(LIQ_model.Liquidacion_PPA).where(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto)

# CONSULTAR DATO DE ROL AGENTE POR LIQUIDACION PPA
def get_Rol_LiqPro(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA.Rol_Agente).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto).first()._asdict()

# CONSULTAR DATO DE CATEGORIA POR LIQUIDACION PPA
def get_Categ_LiqPro(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA.Categoria).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto).first()._asdict()

# CONSULTAR DATO DE SUBCATEGORIA POR LIQUIDACION PPA
def get_Subcateg_LiqPro(db: Session, Proyecto: str):
    return db.query(LIQ_model.Liquidacion_PPA.Subcategoria).filter(LIQ_model.Liquidacion_PPA.Proyecto == Proyecto).first()._asdict()

# CREAR LIQUIDACION PPA
def create_liquidacion_PPA(db: Session, liquidacion: LIQ_schema.Liquidacion_PPA_Create, Proceso: str):
    db_ = get_proyectos(db)
    if db_:
        
        # VERIFICAR QUE EL PERIODO, LA VERSION Y EL PROCESO NO SE REPITA 
        if get_liquidacion_PPA_periodo_version_proceso(db, liquidacion.Periodo, liquidacion.Version, Proceso):
            raise HTTPException(status_code = 400, detail = f"Ya existe un registro de Periodo {liquidacion.Periodo} y Version {liquidacion.Version} para el Proceso {Proceso}")
        i = 1
        while get_proyecto_id(db, i):
            CP = get_proyecto_id_CP(db, i)
            CP = CP.get("Codigo_Proyecto")
            FO = get_FO_CP(db, CP)
            FR = get_FR_CP(db, CP)
            CT = get_Categoria_CP(db, CP)
            SC = get_Subcategoria_CP(db, CP)
            CT = CT.get("Categoria")
            SC = SC.get("Subcategoria")
            FO = FO.get("FPO_Oficial")
            FR = FR.get("FPO_Real")
            FA = liquidacion.Periodo

            if FO != None and FR != None:
                if Proceso == CT:
                    if CT == "STN" and SC == "Convocatoria":
                        if not (FR <= FO or FR < FA) or (FO.year != FR.year and FO.month != FR.month and FO < FR):
                            TD = get_seguimiento_FPO_tipo_doc_proyecto(db, CP).pop()._asdict()
                            TD = TD.get("Tipo_Doc")
                            if TD == "CC":
                                crear(db, liquidacion, CP, CT, SC)

                    else:
                        if not (FR <= FO or FA < FO or FR < FA) or (FO.year != FR.year and FO.month != FR.month and FO < FR):
                            crear(db, liquidacion, CP, CT, SC)
                            
            i = i + 1
    else:
        raise HTTPException(status_code = 400, detail = f"No hay proyectos para liquidar")

    if get_liquidacion_PPA_periodo_version_proceso(db, liquidacion.Periodo, liquidacion.Version, Proceso):
        raise HTTPException(status_code = 200, detail = f"Liquidaciones creadas exitosamente")
    else: 
        raise HTTPException(status_code = 200, detail = f"No hay liquidaciones")

# INTRODUCIR LOS DATOS A LA BASE DE DATOS
def crear(db: Session, liquidacion: LIQ_schema.Liquidacion_PPA_Create, CP: str, CT: str, SC: str):
    get_A = get_Agente_CP(db, CP)
    get_A = get_A.get("Agente")
    get_R = get_Rol_CP(db, CP)
    get_R = get_R.get("Rol_Agente")
    valor = 0
    if CT == "STN" and SC == "Convocatoria" and not get_R == "Generador":
        valor = CO_STN_crud.create_convocatoria_STN_grupo(db, get_A, get_R, CP, liquidacion.Periodo, liquidacion.Version)
    if CT == "STN" and SC == "Ampliación":
        valor = AMP_STN_crud.create_ampliacion_STN_grupo(db, get_A, CP, liquidacion.Periodo, liquidacion.Version)
    if CT == "STR" and SC == "Convocatoria":
        valor = CO_STR_crud.create_convocatoria_STR_grupo(db, get_A, get_R, CP, liquidacion.Periodo, liquidacion.Version)
    if CT == "STR" and SC == "Expansión OR":
        valor = EXP_STR_crud.create_expansion_OR_STR_grupo(db, get_A, CP, liquidacion.Periodo, liquidacion.Version)
    
    db_ = LIQ_model.Liquidacion_PPA(**liquidacion.dict(), Agente = get_A, Rol_Agente = get_R, Proyecto = CP, Categoria = CT, Subcategoria = SC, Valor_PPA = valor)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR LIQUIDACION PPA
def update_liquidacion_PPA(db: Session, liquidacion: LIQ_schema.Liquidacion_PPA_Update, Proyecto: str, Periodo: date, Version: str):
    db_ = get_liquidacion_PPA(db, Proyecto, Periodo, Version)
    data = liquidacion.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR LIQUIDACION PPA
def delete_liquidacion_PPA(db: Session, Proyecto: str, Periodo: date, Version: str):
    db_ = get_liquidacion_PPA(db, Proyecto, Periodo, Version)
    db.delete(db_)
    db.commit()
    return {f"Liquidación PPA para el Proyecto {Proyecto}, el Periodo {Periodo} y la Version {Version} eliminada"}