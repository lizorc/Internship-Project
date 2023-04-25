from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import AMP_STN_schema
from ..validations import GENERAL_validation
from ..CRUD import AMP_STN_crud, DA_AMP_crud



# EXTRAER DATOS
class Return_datos_Amp_STN:
    def __init__(self, IAT, CRE, PAOMR_Actual, PAOMR_Aprobado):
        self.IAT = IAT
        self.CRE = CRE
        self.PAOMR_Actual = PAOMR_Actual
        self.PAOMR_Aprobado = PAOMR_Aprobado


def Buscar_datos_Amp_STN(db: Session, Proyecto: str, Liquidacion: date):

    if DA_AMP_crud.get_dato_ampliaciones_STN(db):
        i = 1
        while DA_AMP_crud.get_dato_ampliacion_STN(db, i):
            get_P = DA_AMP_crud.get_Proyecto_Dato_Amp_STN(db, i) 
            get_P = get_P.get("Proyecto")

            get_I = DA_AMP_crud.get_Inicio_Dato_Amp_STN(db, i)
            get_I = get_I.get("Fecha_Inicio_Vigen")

            get_F = DA_AMP_crud.get_Fin_Dato_Amp_STN(db, i)
            get_F = get_F.get("Fecha_Fin_Vigen")

            if get_P == Proyecto and (Liquidacion >= get_I) and (get_F >= Liquidacion):
                IAT = DA_AMP_crud.get_IAT_Dato_Amp_STN(db, i)
                IAT = IAT.get("IAT")

                CRE = DA_AMP_crud.get_CRE_Dato_Amp_STN(db, i)
                CRE = CRE.get("CRE")

                PAC = DA_AMP_crud.get_PAOMR_Actual_Dato_Amp_STN(db, i)
                PAC = PAC.get("PAOMR_Actual")

                PAP = DA_AMP_crud.get_PAOMR_Aprobado_Dato_Amp_STN(db, i)
                PAP = PAP.get("PAOMR_Aprobado")

                t = Return_datos_Amp_STN(IAT, CRE, PAC, PAP)
                return t

            i = i + 1
        else: 
            raise HTTPException(status_code = 400, detail = "No existe registro de Ampliación para esta fecha")


# CALCULAR EL PPA
def calcular_Amp_STN(db: Session, get_PB: str, IPP_Actual: float, get_DA: int, get_FA: str, get_PRO: str):
    
    Dias_Mes = GENERAL_validation.calcular_dias_mes(get_FA)
    D = Buscar_datos_Amp_STN(db, get_PRO, get_FA)
    Amp_STN = ((D.IAT + D.CRE * ((D.PAOMR_Actual / 100) - (D.PAOMR_Aprobado / 100))) * 1/12 * (IPP_Actual/ (get_PB.get("Precio_Base")))) * (get_DA/Dias_Mes)
    return Amp_STN


# CONFIRMAR EXISTENCIA 
def verificar_ampliacion_STN(db: Session, Amp_id: int):

    # VERIFICAR QUE EL ID DE PPA AMPLIACION STN ESTE EN EL SISTEMA
    db_ = AMP_STN_crud.get_ampliacion_STN(db, Amp_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Ampliación de STN {Amp_id} no existe!")