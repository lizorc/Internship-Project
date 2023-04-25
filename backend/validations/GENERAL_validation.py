from calendar import calendar
import calendar
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..CRUD import VAL_crud
from datetime import date



# CALCULAR LOS DIAS DE ATRASO 
def calcular_atraso(get_FO: date, get_FR: date, Periodo: str):
    FO = get_FO.get("FPO_Oficial")
    FR = get_FR.get("FPO_Real")
    FA = Periodo

    if FR <= FO or FA < FO or FR < FA:
        return 0
    if FO.year == FR.year and FO.month == FR.month and FO > FR:
        return 0
    if FA.month == FR.month and FA.year == FR.year:
        return FR.day - 1
    if FA.month == FO.month and FA.year == FO.year:
        return calcular_dias_mes(Periodo) - (FO.day + 1)
    else:
        return calcular_dias_mes(Periodo)

# CALCULAR CUANTOS DIAS TIENE ESE MES
def calcular_dias_mes(get_FA: date):
    Mes = get_FA
    Dias = calendar.monthrange(Mes.year, Mes.month)[1]

    return Dias


def atraso(get_FO: str, get_FR: str, get_FA: str):
    FO = get_FO.get("FPO_Oficial")
    FR = get_FR.get("FPO_Real")
    FA = get_FA

    if FR <= FO or FA < FO or FR < FA:
        return 0
    if FO.year == FR.year and FO.month == FR.month and FO > FR:
        return 0
    



# BUSCAR TRM DE ACUERDO AL AÑO Y MES
def Buscar_TRM(db: Session, Liquidacion: date):
    db_ = VAL_crud.get_valores(db)
    if db_:
        i = 1
        while VAL_crud.get_valor_ID(db, i):
            Periodo = VAL_crud.get_valor_ID_periodo(db, i)
            Periodo = Periodo.get("Periodo")
            Tipo = VAL_crud.get_valor_ID_tipo(db, i)
            Tipo = Tipo.get("Tipo")
            if Liquidacion.year == Periodo.year and Liquidacion.month == Periodo.month:
                TRM = VAL_crud.get_valor_Valor(db, Periodo, Tipo)
                TRM = TRM.get("Valor")
                return TRM
            i = i + 1
        else:
            raise HTTPException(status_code = 400, detail = "No existe registro de TRM para esta fecha")


# BUSCAR IPP DE ACUERDO AL AÑO Y MES
def Buscar_IPP(db: Session, Liquidacion: date):
    db_ = VAL_crud.get_valores(db)
    if db_:
        i = 1
        while VAL_crud.get_valor_ID(db, i):
            Periodo = VAL_crud.get_valor_ID_periodo(db, i)
            Periodo = Periodo.get("Periodo")
            if Liquidacion.year == Periodo.year and Liquidacion.month == Periodo.month:
                IPP = VAL_crud.get_valor_Valor(db, Liquidacion, Tipo = "IPP") 
                IPP = IPP.get("Valor")
                return IPP
            i = i + 1
        else:
            raise HTTPException(status_code = 400, detail = "No existe registro de IPP para esta fecha")
