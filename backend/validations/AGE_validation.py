from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import AGE_schema
from ..CRUD import AGE_crud



# VALIDACIONES PARA CREAR AGENTE
def validar_agentes_crear(db: Session, agente: AGE_schema.Agente_Create):

    # VERIFICAR QUE EL ASIC TENGA INFORMACIÓN
    if len(agente.ASIC) == 0:
        raise HTTPException(status_code = 400, detail = "Código ASIC sin información")
    
    # VERIFICAR QUE EL ASIC NO ESTE EN EL SISTEMA 
    db_ASIC = AGE_crud.get_agente(db, ASIC = agente.ASIC)
    if db_ASIC:
        raise HTTPException(status_code = 400, detail = f"Código ASIC {agente.ASIC} ya registrado")
    
    # VERIFICAR QUE EL NIT NO ESTE EN EL SISTEMA 
    db_NIT = AGE_crud.get_agente_NIT(db, NIT = agente.NIT)
    if db_NIT and len(agente.NIT) > 0:
        raise HTTPException(status_code = 400, detail = f"Código NIT {agente.NIT} ya registrado")
    
    # VERIFICAR QUE LA RAZON_SOCIAL NO ESTE EN EL SISTEMA 
    db_RS = AGE_crud.get_agente_Razon_Social(db, Razon_Social = agente.Razon_Social)
    if db_RS and len(agente.Razon_Social) > 0:
        raise HTTPException(status_code = 400, detail = f"Razón Social {agente.Razon_Social} ya registrado")


# VALIDACIONES PARA ACTUALIZAR AGENTE
def validar_agentes_actualizar(db: Session, agente: AGE_schema.Agente_Update, ASIC: str):
    
    # VERIFICAR QUE EL ASIC NO ESTE EN EL SISTEMA 
    db_ASIC = AGE_crud.get_agente(db, ASIC = agente.ASIC)
    if db_ASIC and (agente.ASIC != ASIC):
        raise HTTPException(status_code = 400, detail = f"Código ASIC {agente.ASIC} ya registrado")
    
    # VERIFICAR QUE EL NIT NO ESTE EN EL SISTEMA 
    db_NIT = AGE_crud.get_agente_NIT(db, NIT = agente.NIT)
    if db_NIT and len(agente.NIT) > 0:
        raise HTTPException(status_code = 400, detail = f"Código NIT {agente.NIT} ya registrado")
    
    # VERIFICAR QUE EL RS NO ESTE EN EL SISTEMA 
    db_RS = AGE_crud.get_agente_Razon_Social(db, Razon_Social = agente.Razon_Social)
    if db_RS and len(agente.Razon_Social) > 0:
        raise HTTPException(status_code = 400, detail = f"Razón Social {agente.Razon_Social} ya registrado")


# VERIFICAR SI EXISTE UN AGENTE CON EL ASIC
def verificar_agente(db: Session, ASIC: str):

    # VERIFICAR QUE EL ASIC DEL AGENTE ESTE EN EL SISTEMA
    db_ = AGE_crud.get_agente(db, ASIC)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Agente {ASIC} no existe en Base de Datos")