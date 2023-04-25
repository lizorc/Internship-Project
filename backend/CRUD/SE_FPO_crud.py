from .PRO_crud import *
from ..models import SE_FPO_model
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import SE_FPO_schema
from datetime import date, datetime
from ..request import API_extraction
from ..validations import SE_FPO_validation



# OBTENER TODOS LAS SEGUIMIENTOES FPO
def get_seguimientos_FPO(db: Session):
    return db.query(SE_FPO_model.Seguimiento_FPO).all()

# FILTRAR SEGUIMIENTO FPO POR ID 
def get_seguimiento_FPO(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()

# FILTRAR SEGUIMIENTO FPO POR PROYECTO
def get_seguimiento_FPO_proyecto(db: Session, Proyecto: str):
    return db.query(SE_FPO_model.Seguimiento_FPO).filter(SE_FPO_model.Seguimiento_FPO.Proyecto == Proyecto).all()

# FILTRAR SEGUIMIENTO FPO POR PROYECTO
def get_Seg_FPO_proyecto(db: Session, Proyecto: str):
    return db.query(SE_FPO_model.Seguimiento_FPO.ID).filter(SE_FPO_model.Seguimiento_FPO.Proyecto == Proyecto).all()

# FILTRAR SEGUIMIENTO FPO POR FECHA REAL
def get_seguimiento_FPO_real(db: Session, Fecha_Real: date):
    return db.query(SE_FPO_model.Seguimiento_FPO).filter(SE_FPO_model.Seguimiento_FPO.Fecha_Real == Fecha_Real).all()

# FILTRAR TIPO DOC POR PROYECTO
def get_seguimiento_FPO_tipo_doc_proyecto(db: Session, Proyecto: str):
    return db.query(SE_FPO_model.Seguimiento_FPO.Tipo_Doc).filter(SE_FPO_model.Seguimiento_FPO.Proyecto == Proyecto).all()

# FILTRAR SEGUIMIENTO FPO POR FECHA OFICIAL
def get_seguimiento_FPO_oficial(db: Session, Fecha_Oficial: date):
    return db.query(SE_FPO_model.Seguimiento_FPO).filter(SE_FPO_model.Seguimiento_FPO.Fecha_Oficial == Fecha_Oficial).all()

# CONSULTAR Proyecto EN SEGUIMIENTO FPO
def get_Proyecto_Seg_FPO_id(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO.Proyecto).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()._asdict()

# CONSULTAR FECHA EN SEGUIMIENTO FPO
def get_Real_Seg_FPO_id(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO.Fecha_Real).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()._asdict()

# CONSULTAR FECHA EN SEGUIMIENTO FPO
def get_Oficial_Seg_FPO_id(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO.Fecha_Oficial).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()._asdict()

# CONSULTAR FECHA_FIN_VIGEN EN SEGUIMIENTO FPO
def get_Fecha_Fin_Seg_FPO_id(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO.Fecha_Fin_Vigen).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()._asdict()

# CONSULTAR FECHA_INICIO_VIGEN EN SEGUIMIENTO FPO
def get_Fecha_Inicio_Seg_FPO_id(db: Session, Seg_FPO_id: int):
    return db.query(SE_FPO_model.Seguimiento_FPO.Fecha_Inicio_Vigen).filter(SE_FPO_model.Seguimiento_FPO.ID == Seg_FPO_id).first()._asdict()

# FILTRAR SEGUIMIENTO FPO POR FECHA OFICIAL
def get_seguimiento_FPO_oficial_real(db: Session, Fecha_Oficial: date, Fecha_Real: date):
    return db.query(SE_FPO_model.Seguimiento_FPO).filter(SE_FPO_model.Seguimiento_FPO.Fecha_Oficial == Fecha_Oficial).filter(SE_FPO_model.Seguimiento_FPO.Fecha_Real == Fecha_Real).all()

# CREAR SEGUIMIENTO FPO ASOCIADO A UN PROYECTO
def create_seguimiento_FPO_en_proyecto(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, Proyecto: str):
    SE_FPO_validation.poner_fecha_fin_crear(db, seguimiento_FPO, Proyecto)
    db_ = SE_FPO_model.Seguimiento_FPO(**seguimiento_FPO.dict(), Proyecto = Proyecto, Fecha_Fin_Vigen = None)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    get_P = get_proyecto(db, Proyecto)
    get_P.FPO_Oficial = seguimiento_FPO.Fecha_Oficial
    get_P.FPO_Real = seguimiento_FPO.Fecha_Real
    db.commit()
    return db_


# CREAR SEGUIMIENTOS FPO DESDE LA API
def create_seguimiento_FPO_por_API(db: Session):
    db_ = get_proyectos(db)
    if db_:
        j = 1
        API = API_extraction.return_FPO_data()
        while get_proyecto_id(db, j):
            Proyecto = get_proyecto_id_CP(db, j)
            Proyecto = Proyecto.get("Codigo_Proyecto")

            
            data = next((x for x in API if x["Codigo_Proyecto"] == Proyecto), None)

            if data != None:
    
                FO_API = data['FPO_Oficial']
                FR_API = data['FPO_Real'][0:-9]
                FO_DB = get_FO_CP(db, Proyecto)
                FO_DB = FO_DB.get("FPO_Oficial")
                FR_DB = get_FR_CP(db, Proyecto)
                FR_DB = FR_DB.get("FPO_Real")

                if FO_API != None:
                    FO_API = FO_API[0:-9]
                    FO_API = datetime.strptime(FO_API, '%Y-%m-%d').date()
                    FR_API = datetime.strptime(FR_API, '%Y-%m-%d').date()
                        
                    if (FO_API != FO_DB or FR_API != FR_DB) or (FO_DB == None and FR_DB == None):
                        SE_FPO_validation.poner_fechas(db, Proyecto, FO_API, FR_API)

                if FO_API == None:
                    FR_API = datetime.strptime(FR_API, '%Y-%m-%d').date()

                    if FR_DB == None or FR_API != FR_DB:
                        if FO_DB == None: 
                            SE_FPO_validation.poner_fechas(db, Proyecto, FR_API, FR_API)

                        if FO_DB != None:
                            FO = SE_FPO_validation.poner_fecha_oficial(db, Proyecto)
                            SE_FPO_validation.poner_fechas(db, Proyecto, FO, FR_API)
            j = j + 1
        raise HTTPException(status_code = 200, detail = f"Seguimientos de FPO extraidos de la API MDC")
    else:
        raise HTTPException(status_code = 400, detail = f"No hay registros de Proyectos en la Base de Datos")


# ACTUALIZAR SEGUIMIENTO FPO
def update_seguimiento_FPO(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Update, Seg_FPO_id: int):
    db_ = get_seguimiento_FPO(db, Seg_FPO_id)
    get_F_an = get_Fecha_Inicio_Seg_FPO_id(db, Seg_FPO_id)
    get_F_an = get_F_an.get("Fecha_Inicio_Vigen")
    data = seguimiento_FPO.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    SE_FPO_validation.actualizar_fecha_fin(db, seguimiento_FPO, Seg_FPO_id)
    return db_


# ELIMINAR SEGUIMIENTO FPO
def delete_seguimiento_FPO(db: Session, Seg_FPO_id: int):
    get_CP = get_Proyecto_Seg_FPO_id(db, Seg_FPO_id)
    get_CP = get_CP.get("Proyecto")
    db_ = get_seguimiento_FPO(db, Seg_FPO_id)
    db.delete(db_)
    db.commit()
    SE_FPO_validation.cambiar_fechas_eliminar(db, get_CP) 
    return {f"Seguimiento FPO {Seg_FPO_id} eliminada"}