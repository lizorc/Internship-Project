from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Convocatoria_STR_Base(BaseModel): 
    pass

# CREAR DATOS
class Convocatoria_STR_Create(Convocatoria_STR_Base):
    pass 

# CAMPOS AUTORELLENABLES
class Convocatoria_STR(Convocatoria_STR_Base):
    ID: int
    Liquidacion: date
    Proyecto: str
    Agente: str
    Rol_Agente: str
    Anualidad: float
    Porcentaje: float
    IPP_Actual: float 
    Dias_Atraso: int

    class Config:
        orm_mode = True
    
class Convocatoria_STR_Agente(Convocatoria_STR):
    Agente: str

class Convocatoria_STR_Proyecto(Convocatoria_STR):
    Proyecto: str

class Convocatoria_STR_Liquidacion(Convocatoria_STR):
    Liquidacion: date

class Convocatoria_STR_Proyecto_Liquidacion(Convocatoria_STR):
    Proyecto: str
    Liquidacion: date