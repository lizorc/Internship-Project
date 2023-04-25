from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Ampliacion_STN_Base(BaseModel):
    pass


# CREAR DATOS
class Ampliacion_STN_Create(Ampliacion_STN_Base):
    pass 


# CAMPOS AUTORELLENABLES
class Ampliacion_STN(Ampliacion_STN_Base):
    ID: int
    Agente: str
    Liquidacion: date
    Version: str
    Proyecto: str
    IAT: float
    CRE: float
    PAOMR_Actual: float
    PAOMR_Aprobado: float
    IPP_Actual: float
    Dias_Atraso: int

    class Config:
        orm_mode = True

class Ampliacion_STN_Agente(Ampliacion_STN):
    Agente: str

class Ampliacion_STN_Proyecto(Ampliacion_STN):
    Proyecto: str

class Ampliacion_STN_Liquidacion(Ampliacion_STN):
    Liquidacion: date

class Ampliacion_STN_Proyecto_Liquidacion(Ampliacion_STN):
    Proyecto: str
    Liquidacion: date