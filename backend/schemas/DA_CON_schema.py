from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Dato_Convocatoria_Base(BaseModel):
    Fecha_Inicio_Vigen: date
    Fecha_Fin_Vigen: date
    Anualidad: float
    Porcentaje: float
    PPI: float


# CREAR DATOS
class Dato_Convocatoria_Create(Dato_Convocatoria_Base):
    pass 


# ACTUALIZAR DATOS 
class Dato_Convocatoria_Update(BaseModel):
    Fecha_Inicio_Vigen: Optional[date] = None
    Fecha_Fin_Vigen: Optional[date] = None
    Anualidad: Optional[float] = None
    Porcentaje: Optional[float] = None
    PPI: Optional[float] = None


# CAMPOS AUTORELLENABLES
class Dato_Convocatoria(Dato_Convocatoria_Base):
    ID: int
    Proyecto: str
    Categoria: str

    class Config:
        orm_mode = True

class Dato_Convocatoria_Proyecto(Dato_Convocatoria):
    Proyecto: str

class Dato_Convocatoria_Proyecto_Fechas(Dato_Convocatoria):
    Proyecto: str
    Fecha_Inicio_Vigen: Optional[date]
    Fecha_Fin_Vigen: Optional[date]

class Dato_Convocatoria_Fechas(Dato_Convocatoria):
    Fecha_Inicio_Vigen: Optional[date]
    Fecha_Fin_Vigen: Optional[date]