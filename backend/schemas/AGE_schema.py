from .PRO_schema import *
from typing import Optional
from pydantic import BaseModel



# CAMPOS RELLENABLES POR EL USUARIO 
class Agente_Base(BaseModel):
    ASIC: str
    NIT: str
    Razon_Social: str


# CREAR DATOS 
class Agente_Create(Agente_Base):
    pass


# ACTUALIZAR DATOS 
class Agente_Update(Agente_Base):
    ASIC: Optional[str] = None
    NIT: Optional[str] = None
    Razon_Social: Optional[str] = None


# CAMPOS AUTORELLENABLES 
class Agente(Agente_Base):
    Proyectos: list[Proyecto] = []

    class Config:
        orm_mode = True