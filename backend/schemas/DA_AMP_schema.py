from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Dato_Ampliacion_STN_Base(BaseModel):
    Fecha_Inicio_Vigen: date
    Fecha_Fin_Vigen: date
    IAT: float
    CRE: float
    PAOMR_Actual: float
    PAOMR_Aprobado: float


# CREAR DATOS
class Dato_Ampliacion_STN_Create(Dato_Ampliacion_STN_Base):
    pass 


# ACTUALIZAR DATOS 
class Dato_Ampliacion_STN_Update(BaseModel):
    Fecha_Inicio_Vigen: Optional[date] = None
    Fecha_Fin_Vigen: Optional[date] = None
    IAT: Optional[float] = None
    CRE: Optional[float] = None
    PAOMR_Actual: Optional[float] = None
    PAOMR_Aprobado: Optional[float] = None


# CAMPOS AUTORELLENABLES
class Dato_Ampliacion_STN(Dato_Ampliacion_STN_Base):
    ID: int
    Proyecto: str

    class Config:
        orm_mode = True


class Dato_AMP_STN_Proyecto(Dato_Ampliacion_STN):
    Proyecto: str

class Dato_AMP_STN_Fechas(Dato_Ampliacion_STN):
    Fecha_Inicio_Vigen: Optional[date]
    Fecha_Fin_Vigen: Optional[date]

class Dato_AMP_STN_Proyecto_Fechas(Dato_Ampliacion_STN):
    Proyecto: str
    Fecha_Inicio_Vigen: Optional[date] = None
    Fecha_Fin_Vigen: Optional[date]
