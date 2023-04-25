from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import DA_CON_schema
from ..CRUD import PRO_crud, DA_CON_crud


 
# VALIDACIONES PARA CREAR DATOS CONVOCATORIAS
def validar_datos_conv_crear(db: Session, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Create, Proyecto: str):

    get_S = PRO_crud.get_Subcategoria_CP(db, Proyecto)
    get_S = get_S.get("Subcategoria")

    # VERIFICAR SI SE PUEDE HACER ESTE CALCULO PARA LA LIQUIDACIÓN
    if not (get_S == "Convocatoria"):
        raise HTTPException(status_code = 400, detail = f"El proyecto es {get_S} no se puede guardar estos datos")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Conv.Fecha_Inicio_Vigen != None:
        try:
            datetime.strftime(Dato_Conv.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Conv.Fecha_Fin_Vigen != None:
        try:
            datetime.strftime(Dato_Conv.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA ANUALIDAD TENGA INFORMACIÓN
    if Dato_Conv.Anualidad == 0:
        raise HTTPException(status_code = 400, detail = "Anualidad sin información")
    
    # VERIFICAR QUE EL PORCENTAJE TENGA INFORMACIÓN
    if Dato_Conv.Porcentaje == 0:
        raise HTTPException(status_code = 400, detail = "Porcentaje sin información")

    get_C = PRO_crud.get_Categoria_CP(db, Proyecto)
    get_C = get_C.get("Categoria")

    # VERIFICAR QUE EL PPI TENGA INFORMACIÓN
    if get_C == "STN" and Dato_Conv.PPI == 0:
        raise HTTPException(status_code = 400, detail = "Es una Convocatoria STN. El PPI es Obligatorio")
    
    # VERIFICAR QUE EL PPI TENGA INFORMACIÓN
    if get_C == "STR" and Dato_Conv.PPI != 0:
        raise HTTPException(status_code = 400, detail = "Es una Convocatoria STR. El PPI debe estar vacio")



# VALIDACIONES PARA ACTUALIZAR DATOS CONVOCATORIAS
def validar_datos_conv_actualizar(db: Session, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Update, Dato_Conv_id: int):
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Conv.Fecha_Inicio_Vigen != None:
        try:
            datetime.strftime(Dato_Conv.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO VIGENCIA TENGA LA SINTAXIS CORRECTA
    if Dato_Conv.Fecha_Fin_Vigen != None:
        try:
            datetime.strftime(Dato_Conv.Fecha_Fin_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Año Invalida. Formato: YYYY-MM-DD")
    
    get_CP = DA_CON_crud.get_Proyecto_Dato_Conv(db, Dato_Conv_id)
    get_CP = get_CP.get("Proyecto")

    get_C = PRO_crud.get_Categoria_CP(db, get_CP)
    get_C = get_C.get("Categoria")

    # VERIFICAR QUE EL PPI TENGA INFORMACIÓN
    if get_C == "STN" and Dato_Conv.PPI == 0:
        raise HTTPException(status_code = 400, detail = "Es una Convocatoria STN. El PPI es Obligatorio")
    
    # VERIFICAR QUE EL PPI TENGA INFORMACIÓN
    if get_C == "STR" and Dato_Conv.PPI != 0:
        raise HTTPException(status_code = 400, detail = "Es una Convocatoria STR. El PPI debe estar vacio")


# VERIFICAR SI EXISTE UN AGENTE CON EL ASIC
def verificar_dato_conv(db: Session, Dato_Conv_id: int):

    # VERIFICAR QUE EL CP DEL PROYECTO ESTE EN EL SISTEMA
    db_ = DA_CON_crud.get_dato_convocatoria(db, Dato_Conv_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Dato Convocatoria {Dato_Conv_id} no existe en Base de Datos")