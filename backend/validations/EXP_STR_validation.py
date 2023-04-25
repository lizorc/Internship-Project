from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import EXP_STR_schema
from ..CRUD import DA_EXP_crud, EXP_STR_crud, LIQ_crud
from ..validations import GENERAL_validation



class Return_datos_Exp_STR:
    def __init__(self, Tasa_Retorno, BRAEN, RC, BRT, NE, BRA_IAOM):
        self.Tasa_Retorno = Tasa_Retorno
        self.BRAEN = BRAEN
        self.RC = RC
        self.BRT = BRT
        self.NE = NE
        self.BRA_IAOM = BRA_IAOM

def Buscar_datos_Exp_STR(db: Session, Proyecto: str, Liquidacion: date):

    db_ = DA_EXP_crud.get_dato_expansiones_OR_STR(db)
    if db_:
        i = 1
        while DA_EXP_crud.get_dato_expansion_OR_STR(db, i):
            get_P = DA_EXP_crud.get_Proyecto_Dato_Exp_OR_STR(db, i) 
            get_P = get_P.get("Proyecto")

            get_I = DA_EXP_crud.get_Inicio_Dato_Exp_STR(db, i)
            get_I = get_I.get("Fecha_Inicio_Vigen")

            get_F = DA_EXP_crud.get_Fin_Dato_Exp_STR(db, i)
            get_F = get_F.get("Fecha_Fin_Vigen")

            if get_P == Proyecto and (Liquidacion >= get_I) and (get_F >= Liquidacion):
                TR = DA_EXP_crud.get_Tasa_Retorno_Dato_Exp_STR(db, i) 
                TR = TR.get("Tasa_Retorno")

                BRAEN = DA_EXP_crud.get_BRAEN_Dato_Exp_STR(db, i)
                BRAEN = BRAEN.get("BRAEN")

                RC = DA_EXP_crud.get_RC_Dato_Exp_STR(db, i)
                RC = RC.get("RC")

                BRT = DA_EXP_crud.get_BRT_Dato_Exp_STR(db, i)
                BRT = BRT.get("BRT")

                NE = DA_EXP_crud.get_NE_Dato_Exp_STR(db, i)
                NE = NE.get("NE")

                BRA_IAOM = DA_EXP_crud.get_BRA_IAOM_Dato_Exp_STR(db, i)
                BRA_IAOM = BRA_IAOM.get("BRA_IAOM")

                t = Return_datos_Exp_STR(TR, BRAEN, RC, BRT, NE, BRA_IAOM)
                return t
       
            i = i + 1
        else: 
            raise HTTPException(status_code = 400, detail = "No existe registro de Expansión del OR para esta fecha")

# CALCULAR IAA 
def calcular_IAA(db: Session, get_FA: str, get_PRO: str):
    P = Buscar_datos_Exp_STR(db, get_PRO, get_FA)

    BRAE = P.BRAEN - P.RC
    BRANE = (P.NE/100) * BRAE
    BRA = BRAE + BRANE
    IAA = BRA * (P.Tasa_Retorno/100) + P.RC + P.BRT
    return IAA

# CALCULAR IAOM 
def calcular_IAOM(db: Session, get_FA: str, get_PRO: str):
    P = Buscar_datos_Exp_STR(db, get_PRO, get_FA)

    BRAE = P.BRAEN - P.RC
    BRANE = (P.NE/100) * BRAE
    BRA = BRAE + BRANE
    IAOM = BRA * (P.BRA_IAOM/100)
    return IAOM

# CALCULAR FM 
def calcular_FM(db: Session, get_FA: str, get_PRO: str):
    P = Buscar_datos_Exp_STR(db, get_PRO, get_FA)

    FM = (((1 + (P.Tasa_Retorno/100))**(1/12)-1) / (P.Tasa_Retorno/100))*100
    return FM

# CALCULAR EL PPA
def calcular_Exp_STR(get_PB: str, IPP_Actual: float, get_DA: int, get_FA: str, get_IAA: float, get_IAOM: float, get_FM: float):
    
    Dias_Mes = GENERAL_validation.calcular_dias_mes(get_FA)
    Exp_STR = (get_IAA * (get_FM / 100) + get_IAOM/12) * (IPP_Actual/ (get_PB.get("Precio_Base"))) * (get_DA/Dias_Mes)
    return Exp_STR


# CONFIRMAR EXISTENCIA 
def verificar_expansion_OR_STR(db: Session, Exp_STR_id: int):

    # VERIFICAR QUE EL ID DE EXPANSION OR STR ESTE EN EL SISTEMA
    db_ = EXP_STR_crud.get_expansion_OR_STR(db, Exp_STR_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Expansión OR STR {Exp_STR_id} no existe!")