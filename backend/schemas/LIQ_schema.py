from .CO_STN_schema import *
from .CO_STR_schema import *
from .AMP_STN_schema import *
from .EXP_STR_schema import *
from datetime import date
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Liquidacion_PPA_Base(BaseModel):
    Periodo: date
    Version: str
    


# CREAR DATOS
class Liquidacion_PPA_Create(Liquidacion_PPA_Base):
    pass
    


# ACTUALIZAR DATOS 
class Liquidacion_PPA_Update(BaseModel):
    Periodo: Optional[date] = None
    Version: Optional[str] = None



# CAMPOS AUTORELLENABLES
class Liquidacion_PPA(Liquidacion_PPA_Base):
    ID = int
    Agente: str
    Rol_Agente: str
    Proyecto: str
    Categoria: str
    Subcategoria: str
    Valor_PPA: float
    Calculo_Conv_STN: list[Convocatoria_STN] = []
    Calculo_Conv_STR: list[Convocatoria_STR] = []
    Calculo_Amp_STN: list[Ampliacion_STN] = []
    Calculo_Exp_STR: list[Expansion_OR_STR] = [] 

    class Config:
        orm_mode = True

class Liquidacion_PPA_Agente(Liquidacion_PPA):
    Agente: str

class Liquidacion_PPA_Proyecto(Liquidacion_PPA):
    Proyecto: str

class Liquidacion_PPA_Periodo(Liquidacion_PPA):
    Periodo: date

class Liquidacion_PPA_Proyecto_Periodo(Liquidacion_PPA):
    Proyecto: str
    Periodo: date

class Liquidacion_PPA_Categoria(Liquidacion_PPA):
    Categoria: str

class Liquidacion_PPA_Subcategoria(Liquidacion_PPA):
    Subcategoria: str

class Liquidacion_PPA_Categoria_Subcategoria(Liquidacion_PPA):
    Categoria: str
    Subcategoria: str