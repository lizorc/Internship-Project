from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Dato_Ampliacion_STN(Base):
    __tablename__ = "Datos_Ampliaciones_STN"

    ID = Column(Integer, index = True, primary_key = True)
    Proyecto = Column(String, ForeignKey("Proyectos.Codigo_Proyecto"))
    Fecha_Inicio_Vigen = Column(Date, nullable = False)
    Fecha_Fin_Vigen = Column(Date, nullable = False)
    IAT = Column(Float, nullable = False)
    CRE = Column(Float, nullable = False)
    PAOMR_Actual = Column(Float, nullable = False)
    PAOMR_Aprobado = Column(Float, nullable = False)
    
    # RELACION 1 A PROYECTO
    Dato_Amp = relationship("Proyecto", back_populates = "Dato_STN_Amp")