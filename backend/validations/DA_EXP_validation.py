from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import DA_EXP_schema
from ..CRUD import DA_EXP_crud


 
# CREAR
def validar_datos_Exp_STR_crear(db: Session, Dato_Exp_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Create, Proyecto: str):

    get_C = DA_EXP_crud.get_Categoria_CP(db, Proyecto)
    get_C = get_C.get("Categoria")

    get_S = DA_EXP_crud.get_Subcategoria_CP(db, Proyecto)
    get_S = get_S.get("Subcategoria")

    # VERIFICAR SI SE PUEDE HACER ESTE CALCULO PARA LA LIQUIDACIÓN
    if not (get_C == "STR" and get_S == "Expansión OR"):
        raise HTTPException(status_code = 400, detail = f"El proyecto es {get_C} {get_S} no se puede guardar estos datos")
    
        # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(Dato_Exp_STR.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(Dato_Exp_STR.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA TASA DE RETORNO TENGA INFORMACIÓN
    if Dato_Exp_STR.Tasa_Retorno == 0:
        raise HTTPException(status_code = 400, detail = "Tasa de Retorno sin información")
    
    # VERIFICAR QUE LA BRAEN TENGA INFORMACIÓN
    if Dato_Exp_STR.BRAEN == 0:
        raise HTTPException(status_code = 400, detail = "BRAEN sin información")

    # VERIFICAR QUE LA RC TENGA INFORMACIÓN
    if Dato_Exp_STR.RC == 0:
        raise HTTPException(status_code = 400, detail = "RC sin información")
    
    # VERIFICAR QUE LA BRT TENGA INFORMACIÓN
    if Dato_Exp_STR.BRT == 0:
        raise HTTPException(status_code = 400, detail = "BRT sin información")
    
    # VERIFICAR QUE LA NE TENGA INFORMACIÓN
    if Dato_Exp_STR.NE == 0:
        raise HTTPException(status_code = 400, detail = "NE sin información")
    
    # VERIFICAR QUE LA BRA_IAOM TENGA INFORMACIÓN
    if Dato_Exp_STR.BRA_IAOM == 0:
        raise HTTPException(status_code = 400, detail = "%BRA IAOM sin información")
    
    # VERIFICAR QUE EL PERIODO NO SE REPITAN 
    if DA_EXP_crud.get_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Dato_Exp_STR.Fecha_Inicio_Vigen, Dato_Exp_STR.Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"Ya existe un registro con las Fechas {Dato_Exp_STR.Fecha_Inicio_Vigen} y {Dato_Exp_STR.Fecha_Fin_Vigen} para el Proyecto {Proyecto}")


# ACTUALIZAR
def validar_datos_Exp_STR_actualizar(db: Session, Dato_Exp_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Update, Dato_Exp_id: int):
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Exp_STR.Fecha_Inicio_Vigen != None:
        try:
            datetime.strftime(Dato_Exp_STR.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Exp_STR.Fecha_Fin_Vigen != None:
        try:
            datetime.strftime(Dato_Exp_STR.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    Proyecto = DA_EXP_crud.get_Proyecto_Dato_Exp_OR_STR(db, Dato_Exp_id)
    Proyecto = Proyecto.get("Proyecto")


# CONFIRMAR EXISTENCIA 
def verificar_dato_Exp_STR(db: Session, Dato_Exp_id: int):

    # VERIFICAR QUE EL CP DEL PROYECTO ESTE EN EL SISTEMA
    db_ = DA_EXP_crud.get_dato_expansion_OR_STR(db, Dato_Exp_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Dato Expansión OR STR {Dato_Exp_id} no existe en Base de Datos")