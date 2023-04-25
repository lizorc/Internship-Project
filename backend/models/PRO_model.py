from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Proyecto(Base):
    __tablename__ = "Proyectos"

    ID = Column(Integer, index = True)
    Agente = Column(String, ForeignKey("Agentes.ASIC"))
    Rol_Agente = Column(String, nullable = False)
    Codigo_Proyecto = Column(String, nullable = True, primary_key = True)
    UPME = Column(String, nullable = True)
    Res_CREG = Column(String, nullable = True)
    Nombre = Column(String, nullable = False)
    Categoria = Column(String, nullable = False)
    Subcategoria = Column(String, nullable = False)
    FPO_Oficial =  Column(Date, nullable = True)
    FPO_Real = Column(Date, nullable = True)
    Precio_Base = Column(Float, nullable = True) 

    # RELACION 1 A SEGUIMIENTO FPO
    FPO = relationship("Seguimiento_FPO", back_populates = "Proyecto_FPO")

    # RELACION 1 A Liquidacion
    Liq = relationship("Liquidacion_PPA", back_populates = "Proyecto_Liq")
    
    # RELACION 1 A ANUALIDAD CONVOCATORIAS
    Dato_Conv = relationship("Dato_Convocatoria", back_populates = "Conv_Dato")

    # RELACION 1 A DATO AMPLIACION STN
    Dato_STN_Amp = relationship("Dato_Ampliacion_STN", back_populates = "Dato_Amp")

    # RELACION 1 A DATO EXPANSION OR STR
    Dato_STR_Exp = relationship("Dato_Expansion_OR_STR", back_populates = "Dato_Exp")

    # RELACION N A AGENTE
    Agente_re = relationship("Agente", back_populates = "Proyectos")