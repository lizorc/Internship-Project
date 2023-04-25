from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Dato_Expansion_OR_STR(Base):
    __tablename__ = "Datos_Expansiones_OR_STR"

    ID = Column(Integer, index = True, primary_key = True)
    Proyecto = Column(String, ForeignKey("Proyectos.Codigo_Proyecto"))
    Fecha_Inicio_Vigen = Column(Date, nullable = False)
    Fecha_Fin_Vigen = Column(Date, nullable = False)
    Tasa_Retorno = Column(Float, nullable = False)
    BRAEN = Column(Float, nullable = False)
    RC = Column(Float, nullable = False)
    BRT = Column(Float, nullable = False)
    NE = Column(Float, nullable = False)
    BRA_IAOM = Column(Float, nullable = False)
    
    # RELACION 1 A PROYECTO
    Dato_Exp = relationship("Proyecto", back_populates = "Dato_STR_Exp")