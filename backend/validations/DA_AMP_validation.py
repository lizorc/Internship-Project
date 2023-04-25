from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from ..schemas import DA_AMP_schema
from ..CRUD import PRO_crud, DA_AMP_crud


 
# CREAR
def validar_datos_Amp_STN_crear(db: Session, Dato_Amp_STN: DA_AMP_schema.Dato_Ampliacion_STN_Create, Proyecto: str):

    get_C = PRO_crud.get_Categoria_CP(db, Proyecto)
    get_C = get_C.get("Categoria")

    get_S = PRO_crud.get_Subcategoria_CP(db, Proyecto)
    get_S = get_S.get("Subcategoria")

    # VERIFICAR SI SE PUEDE HACER ESTE CALCULO PARA LA LIQUIDACIÓN
    if not (get_C == "STN" and get_S == "Ampliación"):
        raise HTTPException(status_code = 400, detail = f"El proyecto es {get_C} {get_S} no se puede guardar estos datos")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(Dato_Amp_STN.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(Dato_Amp_STN.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE EL IAT TENGA INFORMACIÓN
    if Dato_Amp_STN.IAT == 0:
        raise HTTPException(status_code = 400, detail = "IAT sin información")
    
    # VERIFICAR QUE EL CRE TENGA INFORMACIÓN
    if Dato_Amp_STN.CRE == 0:
        raise HTTPException(status_code = 400, detail = "CREG sin información")

    # VERIFICAR QUE EL PAOMR_ACTUAL TENGA INFORMACIÓN
    if Dato_Amp_STN.PAOMR_Actual == 0:
        raise HTTPException(status_code = 400, detail = "PAOMR_Actual sin información")
    
    # VERIFICAR QUE EL PAOMR_APROBADO TENGA INFORMACIÓN
    if Dato_Amp_STN.PAOMR_Aprobado == 0:
        raise HTTPException(status_code = 400, detail = "PAOMR_Aprobado sin información")
    
    # VERIFICAR QUE EL PERIODO NO SE REPITAN 
    if DA_AMP_crud.get_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Dato_Amp_STN.Fecha_Inicio_Vigen, Dato_Amp_STN.Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"Ya existe un registro con las Fechas {Dato_Amp_STN.Fecha_Inicio_Vigen} y {Dato_Amp_STN.Fecha_Fin_Vigen} para el Proyecto {Proyecto}")


# ACTUALIZAR
def validar_datos_Amp_STN_actualizar(db: Session, Dato_Amp_STN: DA_AMP_schema.Dato_Ampliacion_STN_Update, Dato_Amp_id: int):
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Amp_STN.Fecha_Inicio_Vigen != None:
        try:
            datetime.strftime(Dato_Amp_STN.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Amp_STN.Fecha_Fin_Vigen != None:
        try:
            datetime.strftime(Dato_Amp_STN.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE EL IAT TENGA INFORMACIÓN
    if Dato_Amp_STN.IAT == 0:
        raise HTTPException(status_code = 400, detail = "IAT sin información")
    
    # VERIFICAR QUE EL CRE TENGA INFORMACIÓN
    if Dato_Amp_STN.CRE == 0:
        raise HTTPException(status_code = 400, detail = "CREG sin información")

    # VERIFICAR QUE EL PAOMR_ACTUAL TENGA INFORMACIÓN
    if Dato_Amp_STN.PAOMR_Actual == 0:
        raise HTTPException(status_code = 400, detail = "PAOMR_Actual sin información")
    
    # VERIFICAR QUE EL PAOMR_APROBADO TENGA INFORMACIÓN
    if Dato_Amp_STN.PAOMR_Aprobado == 0:
        raise HTTPException(status_code = 400, detail = "PAOMR_Aprobado sin información")
    
    Proyecto = DA_AMP_crud.get_Proyecto_Dato_Amp_STN(db, Dato_Amp_id)
    Proyecto = Proyecto.get("Proyecto")


# CONFIRMAR EXISTENCIA 
def verificar_dato_Amp_STN(db: Session, Dato_Amp_id: int):

    # VERIFICAR QUE EL CP DEL PROYECTO ESTE EN EL SISTEMA
    db_ = DA_AMP_crud.get_dato_ampliacion_STN(db, Dato_Amp_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Dato Ampliación STN {Dato_Amp_id} no existe en Base de Datos")