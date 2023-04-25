from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import CO_STN_schema
from ..validations import GENERAL_validation
from ..CRUD import DA_CON_crud, LIQ_crud, CO_STN_crud



# CREAR
def validar_convocatoria_STN_crear(db: Session, Conv_STN: CO_STN_schema.Convocatoria_STN_Create, Proyecto: str):

    get_C = LIQ_crud.get_Categ_LiqPro(db, Proyecto)
    get_C = get_C.get("Categoria")

    get_S = LIQ_crud.get_Subcateg_LiqPro(db, Proyecto)
    get_S = get_S.get("Subcategoria")

    # VERIFICAR SI SE PUEDE HACER ESTE CALCULO PARA LA LIQUIDACIÓN
    if not (get_C == "STN" and get_S == "Convocatoria"):
        raise HTTPException(status_code = 400, detail = f"El proyecto es {get_C} {get_S} no se puede hacer este calculo con STN Convocatoria")
 
    Rol_Agente = LIQ_crud.get_Rol_LiqPro(db, Proyecto)
    Rol_Agente = Rol_Agente.get("Rol_Agente")
    
    # VERIFICAR QUE LAS CAPACIDADES ESTEN VACIAS
    if (Rol_Agente == "Ejecutor" or Rol_Agente == "Usuario" or Rol_Agente == "Conexión") and (Conv_STN.Capacidad_T != 0 or Conv_STN.Capacidad_O != 0):
        raise HTTPException(status_code = 400, detail = "Capacidades Invalidas. Si el rol del Agente es Ejecutor, Conexón o Usuario, los campos Capacidad_T y Capacidad_O debe estar en cero")
    
    # VERIFICAR QUE LAS CAPACIDADES NO ESTEN VACIAS
    if (Rol_Agente == "Generador") and (Conv_STN.Capacidad_T == 0 or Conv_STN.Capacidad_O == 0):
        raise HTTPException(status_code = 400, detail = "Capacidades Vacias. Si el rol del Agente es Generador, los campos Capacidad_T y Capacidad_O deben tener información")

    
# LLENAR CAMPO TIPO DE PROYECTO 
def calcular_tipo_proyecto(Rol_Agente: str):

    # HACER QUE EL TIPO DE PROYECTO SEA EL VALOR CORRECTO  
    if Rol_Agente == "Ejecutor":
        return 2
    
    # HACER QUE EL TIPO DE PROYECTO SEA EL VALOR CORRECTO 
    if Rol_Agente == "Conexión" or Rol_Agente == "Generador" or Rol_Agente == "Usuario":
        return 1


# LLENAR CAMPO FACTOR TIPO DE PROYECTO
def llenar_factor_generador(Conv_STN: CO_STN_schema.Convocatoria_STN_Create, get_Rol: str):
    Rol_Agente = get_Rol.get("Rol_Agente")

    # HACER QUE EL FACTOR GENERADOR SEA EL VALOR CORRECTO 
    if Rol_Agente == "Generador":
        FG = (1 - (Conv_STN.Capacidad_O / Conv_STN.Capacidad_T)) * 100
        return FG
    
    # HACER QUE EL FACTOR GENERADOR SEA EL VALOR CORRECTO 
    if Rol_Agente == "Ejecutor" or Rol_Agente == "Usuario" or Rol_Agente == "Conexión":
        return 1


# CALCULAR LOS DIAS DE ATRASO 
def calcular_atraso_Conv_STN(get_FO: str, get_FR: str, Liquidacion: date):
    FO = get_FO.get("FPO_Oficial")
    FR = get_FR.get("FPO_Real")
    FA = Liquidacion

    if FR <= FO or FR < FA:
        return 0

    if FO.year == FR.year and FO.month == FR.month and FO > FR:
        return 0

    if FA.month == FR.month and FA.year == FR.year:
        return FR.day - 1

    if FA.month == FO.month and FA.year == FO.year:
        return GENERAL_validation.calcular_dias_mes(Liquidacion) - (FO.day + 1)

    else:
        return GENERAL_validation.calcular_dias_mes(Liquidacion)


# EXTRAER ANUALIDAD, PORCENTAJE Y PPI
class Return_datos_Conv_STN:
    def __init__(self, Anualidad, Porcentaje, PPI_Actual):
        self.Anualidad = Anualidad
        self.Porcentaje = Porcentaje
        self.PPI_Actual = PPI_Actual


def Buscar_datos_Conv_STN(db: Session, Proyecto: str, Liquidacion: date):
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

            if get_P == Proyecto and (Liquidacion >= get_I and get_F >= Liquidacion):
                Anualidad = DA_CON_crud.get_Anualidad_Dato_Conv(db, i) 
                Anualidad = Anualidad.get("Anualidad")

                Porcentaje = DA_CON_crud.get_Porcentaje_Dato_Conv(db, i)
                Porcentaje = Porcentaje.get("Porcentaje")

                PPI_Actual = DA_CON_crud.get_PPI_Dato_Conv(db, i)
                PPI_Actual = PPI_Actual.get("PPI")

                t = Return_datos_Conv_STN(Anualidad, Porcentaje, PPI_Actual)
                return t

            i = i + 1
    else: 
        raise HTTPException(status_code = 400, detail = "No existe registro de Anualidad para esta fecha")


# CALCULAR EL PPA
def calcular_Conv_STN(db: Session, get_TP: int, get_FG: float, get_PB: str, get_DA: int, TRM: float, get_FA: date, get_PRO: str):
    
    Dias_Mes = GENERAL_validation.calcular_dias_mes(get_FA)
    D = Buscar_datos_Conv_STN(db, get_PRO, get_FA)
    Conv_STN = round(round(round(round(round(round(D.Anualidad * (D.PPI_Actual / (get_PB.get("Precio_Base"))))/12) * get_TP * get_FG) * (get_DA/Dias_Mes)) * TRM)  * (D.Porcentaje / 100))
    return Conv_STN


# CALCULAR EL PPA
def actualizar_Conv_STN(db: Session,Conv_STN: CO_STN_schema.Convocatoria_STN_Update, get_TP: int, get_FG: float, get_PB: str, get_DA: int, TRM: float, get_FA: date, get_PRO: str):
    
    Dias_Mes = GENERAL_validation.calcular_dias_mes(get_FA)
    D = Buscar_datos_Conv_STN(db, get_FA, get_PRO)
    Conv_STN = round(round(round(round(round(round(D.Anualidad * (D.PPI_Actual / (get_PB.get("Precio_Base"))))/12) * get_TP * get_FG) * (get_DA/Dias_Mes)) * TRM)  * (D.Porcentaje / 100))
    return Conv_STN


# ACTUALIZAR
def validar_convocatoria_STN_actualizar(db: Session, Conv_STN: CO_STN_schema.Convocatoria_STN_Update, Conv_STN_id: int):

    get_PO = CO_STN_crud.get_proyecto_convocatoria_STN(db, Conv_STN_id)
    get_PO = get_PO.get("Proyecto")
    Rol_Agente = LIQ_crud.get_Rol_LiqPro(db, get_PO)
    Rol_Agente = Rol_Agente.get("Rol_Agente")
    
    # VERIFICAR QUE LAS CAPACIDADES ESTEN VACIAS
    if (Rol_Agente == "Ejecutor" or Rol_Agente == "Usuario" or Rol_Agente == "Conexión") and (Conv_STN.Capacidad_T != 0 or Conv_STN.Capacidad_O != 0):
        raise HTTPException(status_code = 400, detail = "Capacidades Invalidas. Si el rol del Agente es Ejecutor, Conexón o Usuario, los campos Capacidad_T y Capacidad_O debe estar en cero")
    
    # VERIFICAR QUE LAS CAPACIDADES NO ESTEN VACIAS
    if (Rol_Agente == "Generador") and (Conv_STN.Capacidad_T == 0 or Conv_STN.Capacidad_O == 0):
        raise HTTPException(status_code = 400, detail = "Capacidades Vacias. Si el rol del Agent es Generador, los campos Capacidad_T y Capacidad_O deben tener información")


# LLENAR CAMPO FACTOR TIPO DE PROYECTO
def actu_factor_generador(Conv_STN: CO_STN_schema.Convocatoria_STN_Update, get_Rol: str):
    Rol_Agente = get_Rol.get("Rol_Agente")

    # HACER QUE EL FACTOR GENERADOR SEA EL VALOR CORRECTO 
    if Rol_Agente == "Generador":
        FG = (1 - (Conv_STN.Capacidad_O / Conv_STN.Capacidad_T)) * 100
        return FG
    
    # HACER QUE EL FACTOR GENERADOR SEA EL VALOR CORRECTO 
    if (Rol_Agente == "Ejecutor" or Rol_Agente == "Usuario"):
        return 1


# CONFIRMAR EXISTENCIA 
def verificar_convocatoria_STN(db: Session, Conv_STN_id: int):

    # VERIFICAR QUE EL ID DE CONVOCATORIA ESTE EN EL SISTEMA
    db_ = CO_STN_crud.get_convocatoria_STN(db, Conv_STN_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Convocatoria STN {Conv_STN_id} no existe")