from .DA_CON_schema import *
from .DA_AMP_schema import *
from .DA_EXP_schema import *
from .SE_FPO_schema import *
from .LIQ_schema import *
from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Proyecto_Base(BaseModel):
    Rol_Agente: str
    Codigo_Proyecto: str
    UPME: str
    Res_CREG: str 
    Nombre: str
    Categoria: str
    Subcategoria: str
    Precio_Base: float


# CREAR DATOS 
class Proyecto_Create(Proyecto_Base):
    pass


# ACTUALIZAR DATOS 
class Proyecto_Update(Proyecto_Base):
    Rol_Agente: Optional[str] = None
    Codigo_Proyecto: Optional[str] = None
    UPME: Optional[str] = None
    Res_CREG: Optional[str] = None
    Nombre: Optional[str] = None
    Categoria: Optional[str] = None
    Subcategoria: Optional[str] = None
    Precio_Base: Optional[float] = None


# CAMPOS AUTORELLENABLES 
class Proyecto(Proyecto_Base):
    ID: int
    Agente: str
    FPO_Oficial: Optional[date] = None
    FPO_Real: Optional[date] = None
    FPO: list[Seguimiento_FPO] = [] 
    Liq: list[Liquidacion_PPA] = []
    Dato_Conv: list[Dato_Convocatoria] = []
    Dato_STN_Amp: list[Dato_Ampliacion_STN] = []
    Dato_STR_Exp: list[Dato_Expansion_OR_STR] = []

    class Config:
        orm_mode = True

class Proyecto_UPME(Proyecto):
    UPME: str

class Proyecto_CREG(Proyecto):
    Res_CREG: str

class Proyecto_Agente(Proyecto):
    Agente: str

class Proyecto_Categoria(Proyecto):
    Categoria: str

class Proyecto_Subcategoria(Proyecto):
    Subcategoria: str

class Proyecto_Categoria_Subcategoria(Proyecto):
    Categoria: str
    Subcategoria: str