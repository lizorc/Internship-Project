from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Seguimiento_FPO_Base(BaseModel):
    Fecha_Oficial: Optional[date] = None
    Fecha_Real: Optional[date] = None
    Fecha_Inicio_Vigen: date
    Tipo_Doc: str
    Descrip_Doc: str
    Documento: Optional[str] = None


# CREAR DATOS
class Seguimiento_FPO_Create(Seguimiento_FPO_Base):
    pass


# ACTUALIZAR DATOS 
class Seguimiento_FPO_Update(BaseModel):
    Fecha_Oficial:  Optional[date] = None
    Fecha_Real:  Optional[date] = None
    Fecha_Inicio_Vigen:  Optional[date] = None
    Tipo_Doc: Optional[str] = None
    Descrip_Doc:  Optional[str] = None
    Documento: Optional[str] = None


class Seguimiento_FPO_Crear(BaseModel):
    pass

# CAMPOS AUTORELLENABLES
class Seguimiento_FPO(Seguimiento_FPO_Base):
    ID: int
    Proyecto: str
    Fecha_Oficial: Optional[date] = None
    Fecha_Real: Optional[date] = None
    Fecha_Fin_Vigen: Optional[date] = None

    class Config:
        orm_mode = True


class Seguimiento_FPO_Proyecto(Seguimiento_FPO):
    Proyecto: str
    Documento: Optional[str] = None

class Seguimiento_FPO_Oficial(Seguimiento_FPO):
    Fecha_Oficial: date
    Documento: Optional[str] = None

class Seguimiento_FPO_Real(Seguimiento_FPO):
    Fecha_Real: date
    Documento: Optional[str] = None

class Seguimiento_FPO_Oficial_Real(Seguimiento_FPO):
    Fecha_Oficial: date
    Fecha_Real: date
    Documento: Optional[str] = None