from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Dato_Convocatoria(Base):
    __tablename__ = "Datos_Convocatorias"

    ID = Column(Integer, index = True, primary_key = True)
    Proyecto = Column(String, ForeignKey("Proyectos.Codigo_Proyecto"))
    Categoria = Column(String, nullable = False)
    Fecha_Inicio_Vigen = Column(Date, nullable = False)
    Fecha_Fin_Vigen = Column(Date, nullable = False)
    Anualidad = Column(Float, nullable = False)
    Porcentaje = Column(Float, nullable = False)
    PPI = Column(Float, nullable = False)
    
    # RELACION 1 A PROYECTO
    Conv_Dato = relationship("Proyecto", back_populates = "Dato_Conv") 