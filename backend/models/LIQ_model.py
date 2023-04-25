from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Liquidacion_PPA(Base):
    __tablename__ = "Liquidaciones_PPA"

    ID = Column(Integer, index = True, primary_key = True)
    Agente = Column(String)
    Rol_Agente = Column(String)
    Proyecto = Column(String, ForeignKey("Proyectos.Codigo_Proyecto"))
    Categoria = Column(String)
    Subcategoria = Column(String)
    Periodo = Column(Date, nullable = False)
    Valor_PPA = Column(Float, nullable = True)
    Version = Column(String, nullable = False)

    # RELACION 1 A CONVOCATORIA STN
    Calculo_Conv_STN = relationship("Convocatoria_STN", back_populates = "Liq")

    # RELACION 1 A CONVOCATORIA STR
    Calculo_Conv_STR = relationship("Convocatoria_STR", back_populates = "Liq")

    # RELACION 1 A AMPLIACION STN
    Calculo_Amp_STN = relationship("Ampliacion_STN", back_populates = "Liq")

    # RELACION 1 A EXPANSION OR STR
    Calculo_Exp_STR = relationship("Expansion_OR_STR", back_populates = "Liq")

    # RELACION N A PROYECTO
    Proyecto_Liq = relationship("Proyecto", back_populates = "Liq")