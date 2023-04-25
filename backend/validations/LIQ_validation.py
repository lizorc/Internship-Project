from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import LIQ_schema
from ..CRUD import LIQ_crud, CO_STN_crud, CO_STR_crud



# CREAR
def validar_liquidaciones_crear(liquidacion: LIQ_schema.Liquidacion_PPA_Create, Proceso: str):
    
    # VERIFICAR QUE LA PROCESO SEA LO CORRECTO
    if not (Proceso == "STN" or Proceso == "STR"):
        raise HTTPException(status_code = 400, detail = "Proceso Invalido. Opciones permitidas: STN o STR")
    
    # VERIFICAR QUE EL PERIODO DE LIQUIDACION TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(liquidacion.Periodo, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Periodo Liquidación Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA VERSION TENGA INFORMACION
    if liquidacion.Version == None:
        raise HTTPException(status_code = 400, detail = "Versión sin Información")

    # VERIFICAR QUE LA VERSION SEA LO CORRECTO
    if not (liquidacion.Version == "Est" or liquidacion.Version == "Liq" or liquidacion.Version == "Aju1" or liquidacion.Version == "Aju2"):
        raise HTTPException(status_code = 400, detail = "Versión Invalida. Opciones permitidas: Est, Liq, Aju1 o Aju2")


# ACTUALIZAR
def validar_liquidaciones_actualizar(liquidacion: LIQ_schema.Liquidacion_PPA_Update):
    
    # VERIFICAR QUE EL PERIODO DE LIQUIDACION TENGA LA SINTAXIS CORRECTA
    if liquidacion.Periodo != None:
        try:
            datetime.strftime(liquidacion.Periodo, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Periodo Liquidación Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA VERSION SEA LO CORRECTO
    if not (liquidacion.Version == "Est" or liquidacion.Version == "Liq" or liquidacion.Version == "Aju1" or liquidacion.Version == "Aju2"):
        raise HTTPException(status_code = 400, detail = "Versión Invalida. Opciones permitidas: Est, Liq, Aju1 o Aju2")


# CONFIRMAR EXISTENCIA 
def verificar_liquidacion_PPA(db: Session, Proyecto: str, Periodo: date, Version: str):

    # VERIFICAR QUE EL ID DE LIQUIDACION PPA ESTE EN EL SISTEMA
    db_ = LIQ_crud.get_liquidacion_PPA(db, Proyecto, Periodo, Version)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Liquidacion para el Proyecto {Proyecto}, el Periodo {Periodo} y la Version {Version} no existe en Base de Datos")


# CONFIRMAR QUE UNA LIQUIDACION SOLO TENGA CALCULO PPA
def verificar_calculo_unico(db: Session, Proyecto: str, Periodo: date, Version: str):

    # VERIFICAR QUE EL ID DE LA LIQUIDACION ESTE EN EL SISTEMA
    db_Con_STN = CO_STN_crud.get_liq_convocatoria_STN(db, Proyecto, Periodo, Version)
    db_Con_STR = CO_STR_crud.get_liq_convocatoria_STR(db, Proyecto, Periodo, Version)

    if db_Con_STN or db_Con_STR:
        raise HTTPException(status_code = 404, detail = f"Ya hay un Calculo para esta liquidacion")
