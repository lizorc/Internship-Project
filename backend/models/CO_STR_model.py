from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Convocatoria_STR(Base):
    __tablename__ = "Convocatorias_STR"

    ID = Column(Integer, index = True, primary_key = True)
    Agente = Column(String, nullable = False)
    Rol_Agente = Column(String, nullable = False)
    Liquidacion = Column(Date, ForeignKey("Liquidaciones_PPA.Periodo"))
    Version = Column(String, nullable = False)
    Proyecto = Column(String, nullable = False)
    Anualidad = Column(Float, nullable = False)
    Porcentaje = Column(Float, nullable = False)
    IPP_Actual = Column(Float, nullable = False)
    Dias_Atraso = Column(Integer, nullable = False)

    # RELACION 1 A LIQUIDACION
    Liq = relationship("Liquidacion_PPA", back_populates = "Calculo_Conv_STR")