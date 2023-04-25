from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..CRUD import CO_STR_crud, DA_CON_crud
from ..validations import GENERAL_validation



# EXTRAER ANUALIDAD
class Return_datos_Conv:
    def __init__(self, Anualidad, Porcentaje):
        self.Anualidad = Anualidad
        self.Porcentaje = Porcentaje

def Buscar_datos_Conv(db: Session, Proyecto: str, Liquidacion: date):

    db_ = DA_CON_crud.get_datos_convocatorias(db)
    if db_:
        i = 1
        while DA_CON_crud.get_dato_convocatoria(db, i):
            get_P = DA_CON_crud.get_Proyecto_Dato_Conv(db, i) 
            get_P = get_P.get("Proyecto")

            get_I = DA_CON_crud.get_Inicio_Dato_Conv(db, i)
            get_I = get_I.get("Fecha_Inicio_Vigen")

            get_F = DA_CON_crud.get_Fin_Dato_Conv(db, i)
            get_F = get_F.get("Fecha_Fin_Vigen")

            if get_P == Proyecto and (Liquidacion >= get_I) and (get_F >= Liquidacion):
                Anualidad = DA_CON_crud.get_Anualidad_Dato_Conv(db, i) 
                Anualidad = Anualidad.get("Anualidad")

                Porcentaje = DA_CON_crud.get_Porcentaje_Dato_Conv(db, i)
                Porcentaje = Porcentaje.get("Porcentaje")

                t = Return_datos_Conv(Anualidad, Porcentaje)
                return t

            i = i + 1
        else:
            raise HTTPException(status_code = 400, detail = "No existe registro de Anualidad para esta fecha")



# CALCULAR EL PPA
def calcular_Conv_STR(db: Session, get_PB: str, IPP_Actual: float, get_DA: int, get_FA: str, get_PRO: str):
    
    Dias_Mes = GENERAL_validation.calcular_dias_mes(get_FA)
    D = Buscar_datos_Conv(db, get_PRO, get_FA)
    Conv_STR = round(round(round(round(D.Anualidad * (IPP_Actual/(get_PB.get("Precio_Base"))))/12)*(D.Porcentaje/100)) * (get_DA/Dias_Mes))
    return Conv_STR


# CONFIRMAR EXISTENCIA 
def verificar_convocatoria_STR(db: Session, Conv_STR_id: int):

    # VERIFICAR QUE EL ID DE CONVOCATORIA ESTE EN EL SISTEMA
    db_ = CO_STR_crud.get_convocatoria_STR(db, Conv_STR_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Convocatoria STR {Conv_STR_id} no existe")