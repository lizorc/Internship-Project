from ..CRUD import VAL_crud
from ..schemas import VAL_schema
from fastapi import HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from datetime import date, datetime



# VALIDACIONES PARA CREAR VALOR
def validar_valores_crear(db: Session, Val: VAL_schema.Valor_Create):
    
    if Val.Periodo == None:
        raise HTTPException(status_code = 400, detail = f"Periodo sin información")
    
    # VERIFICAR QUE EL PERIODO TENGA LA SINTAXIS CORRECTA
    if Val.Periodo != None:
        try:
            datetime.strftime(Val.Periodo, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 422, detail = "Periodo Invalido. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUEEL TIPO TENGA INFORMACIÓN
    if len(Val.Tipo) == 0:
        raise HTTPException(status_code = 400, detail = "Tipo sin información")
    
    # VERIFICAR QUEEL TIPO TENGA INFORMACIÓN
    if not (Val.Tipo == 'IPP' or Val.Tipo == 'TRM'):
        raise HTTPException(status_code = 400, detail = "Tipo invalido. Opciones permitidas: IPP y TRM")
    
    # VERIFICAR QUE EL VALOR TENGA INFORMACIÓN
    if Val.Valor == 0:
        raise HTTPException(status_code = 400, detail = "Valor sin información")
    
    # VERIFICAR QUE EL PERIODO Y EL TIPO NO SE REPITAN 
    if VAL_crud.get_valor(db, Val.Periodo, Val.Tipo):
        raise HTTPException(status_code = 400, detail = f"Ya existe un registro de Periodo {Val.Periodo} y Tipo {Val.Tipo}")


# VALIDACIONES PARA ACTUALIZAR VALOR
def validar_valores_actualizar(db: Session, Val: VAL_schema.Valor_Update, Periodo: date, Tipo: str):
    
    # VERIFICAR QUE EL PERIODO TENGA LA SINTAXIS CORRECTA
    if Val.Periodo != None:
        try:
            datetime.strftime(Val.Periodo, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Periodo Invalido. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUEEL TIPO TENGA INFORMACIÓN
    if Val.Tipo != None and not (Val.Tipo == 'IPP' or Val.Tipo == 'TRM'):
        raise HTTPException(status_code = 400, detail = "Tipo invalido. Opciones permitidas: IPP y TRM")
    
    db_ = VAL_crud.get_valor(db, Val.Periodo, Val.Tipo)
    if db_ and ((Val.Periodo != Periodo) and Val.Tipo != Tipo):
        raise HTTPException(status_code = 400, detail = f"Ya existe un registro de Periodo {Val.Periodo} y Tipo {Val.Tipo}")


# VERIFICAR SI EXISTE UN VALOR CON EL PERIODO Y TIPO
def verificar_valor(db: Session, Periodo: date, Tipo: str):

    # VERIFICAR QUE EL CP DEL PROYECTO ESTE EN EL SISTEMA
    db_ = VAL_crud.get_valor(db, Periodo, Tipo)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Valor del Periodo {Periodo} y Tipo {Tipo} no existe en Base de Datos")
