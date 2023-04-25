from datetime import date
from typing import Optional
from pydantic import BaseModel, Field



# CAMPOS RELLENABLES POR EL USUARIO 
class Valor_Base(BaseModel):
    Periodo: Optional[date] = Field(None)
    Tipo: str
    Valor: float


# CREAR DATOS
class Valor_Create(Valor_Base):
    pass 


# ACTUALIZAR DATOS 
class Valor_Update(BaseModel):
    Periodo:  Optional[date] = None
    Tipo:  Optional[str] = None
    Valor: Optional[float] = None


# CAMPOS AUTORELLENABLES
class Valor(Valor_Base):
    ID: int
    
    class Config:
        orm_mode = True


class Valor_Periodo(Valor):
    Periodo: date 

class Valor_Tipo(Valor):
    Tipo: str