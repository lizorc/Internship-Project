from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Ampliacion_STN(Base):
    __tablename__ = "Ampliaciones_STN"

    ID = Column(Integer, index = True, primary_key = True)
    Agente = Column(String, nullable = False)
    Liquidacion = Column(Date, ForeignKey("Liquidaciones_PPA.Periodo"))
    Version = Column(String, nullable = False)
    Proyecto = Column(String, nullable = False)
    IAT = Column(Float, nullable = False)
    CRE = Column(Float, nullable = False)
    PAOMR_Actual = Column(Float, nullable = False)
    PAOMR_Aprobado = Column(Float, nullable = False)
    IPP_Actual = Column(Float, nullable = False)
    Dias_Atraso = Column(Integer, nullable = False)
    
    # RELACION 1 A LIQUIDACION
    Liq  = relationship("Liquidacion_PPA", back_populates = "Calculo_Amp_STN")