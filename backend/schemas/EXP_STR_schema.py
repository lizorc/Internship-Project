from datetime import date
from typing import Optional
from pydantic import BaseModel


 
# CAMPOS RELLENABLES POR EL USUARIO 
class Expansion_OR_STR_Base(BaseModel):
    pass


# CREAR DATOS
class Expansion_OR_STR_Create(Expansion_OR_STR_Base):
    pass 


# CAMPOS AUTORELLENABLES
class Expansion_OR_STR(Expansion_OR_STR_Base):
    ID: int
    Agente: str
    Liquidacion: date
    Version: str
    Proyecto: str
    IAA: float 
    IAOM: float 
    FM: float
    IPP_Actual: float
    Dias_Atraso: int

    class Config:
        orm_mode = True

class Expansion_OR_STR_Agente(Expansion_OR_STR):
    Agente: str

class Expansion_OR_STR_Proyecto(Expansion_OR_STR):
    Proyecto: str

class Expansion_OR_STR_Liquidacion(Expansion_OR_STR):
    Liquidacion: date

class Expansion_OR_STR_Proyecto_Liquidacion(Expansion_OR_STR):
    Proyecto: str
    Liquidacion: date