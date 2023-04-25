from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Convocatoria_STN(Base):
    __tablename__ = "Convocatorias_STN"

    ID = Column(Integer, index = True, primary_key = True)
    Agente = Column(String, nullable = False)
    Rol_Agente = Column(String, nullable = False)
    Liquidacion = Column(Date, ForeignKey("Liquidaciones_PPA.Periodo"))
    Version = Column(String, nullable = False)
    Proyecto = Column(String, nullable = False)
    Anualidad = Column(Float, nullable = False)
    Porcentaje = Column(Float, nullable = False)
    Factor_Generador = Column(Float, nullable = False)
    PPI_Actual = Column(Float, nullable = False)
    TRM = Column(Float, nullable = False)
    Dias_Atraso = Column(Integer, nullable = False)
    Capacidad_O = Column(Float, nullable = False)
    Capacidad_T = Column(Float, nullable = False)
    
    # RELACION 1 A LIQUIDACION
    Liq = relationship("Liquidacion_PPA", back_populates = "Calculo_Conv_STN")