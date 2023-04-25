from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Convocatoria_STN_Base(BaseModel):
    Capacidad_O: float
    Capacidad_T: float


# CREAR DATOS
class Convocatoria_STN_Create(Convocatoria_STN_Base):
    pass 


# ACTUALIZAR DATOS 
class Convocatoria_STN_Update(BaseModel):
    Capacidad_O: Optional[float] = None
    Capacidad_T: Optional[float] = None


# CAMPOS AUTORELLENABLES
class Convocatoria_STN(Convocatoria_STN_Base):
    ID: int
    Agente: str
    Rol_Agente: str
    Liquidacion: date
    Version: str
    Proyecto: str
    Anualidad: float
    Porcentaje: float
    Factor_Generador: float 
    Dias_Atraso: int
    PPI_Actual: float
    TRM: float

    class Config:
        orm_mode = True

class Convocatoria_STN_Agente(Convocatoria_STN):
    Agente: str

class Convocatoria_STN_Proyecto(Convocatoria_STN):
    Proyecto: str

class Convocatoria_STN_Liquidacion(Convocatoria_STN):
    Liquidacion: date

class Convocatoria_STN_Proyecto_Liquidacion(Convocatoria_STN):
    Proyecto: str
    Liquidacion: date