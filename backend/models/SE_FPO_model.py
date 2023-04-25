from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Seguimiento_FPO(Base):
    __tablename__ = "Seguimientos_FPO"

    ID = Column(Integer, index = True, primary_key = True)
    Proyecto = Column(String, ForeignKey("Proyectos.Codigo_Proyecto"))
    Fecha_Oficial = Column(Date, nullable = True)
    Fecha_Real = Column(Date, nullable = True)
    Fecha_Inicio_Vigen = Column(Date, nullable = True)
    Fecha_Fin_Vigen = Column(Date, nullable = True)
    Tipo_Doc = Column(String, nullable =True)
    Descrip_Doc = Column(String, nullable = True)
    Documento = Column(String, nullable = True)

    # RELACION N A PROYECTO
    Proyecto_FPO = relationship("Proyecto", back_populates = "FPO")