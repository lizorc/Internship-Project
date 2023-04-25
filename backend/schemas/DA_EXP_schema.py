from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Dato_Expansion_OR_STR_Base(BaseModel):
    Fecha_Inicio_Vigen: date
    Fecha_Fin_Vigen: date
    Tasa_Retorno: float
    BRAEN: float
    RC: float
    BRT: float
    NE: float
    BRA_IAOM: float


# CREAR DATOS
class Dato_Expansion_OR_STR_Create(Dato_Expansion_OR_STR_Base):
    pass 


# ACTUALIZAR DATOS 
class Dato_Expansion_OR_STR_Update(BaseModel):
    Fecha_Inicio_Vigen: Optional[date] = None
    Fecha_Fin_Vigen: Optional[date] = None
    Tasa_Retorno:  Optional[float] = None
    BRAEN:  Optional[float] = None
    RC:  Optional[float] = None
    BRT:  Optional[float] = None
    NE:  Optional[float] = None
    BRA_IAOM: Optional[float] = None


# CAMPOS AUTORELLENABLES
class Dato_Expansion_OR_STR(Dato_Expansion_OR_STR_Base):
    ID: int
    Proyecto: str


    class Config:
        orm_mode = True


class Dato_EXP_STR_Proyecto(Dato_Expansion_OR_STR):
    Proyecto: str

class Dato_EXP_STR_Fechas(Dato_Expansion_OR_STR):
    Fecha_Inicio_Vigen: date
    Fecha_Fin_Vigen: date

