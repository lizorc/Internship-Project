from sqlalchemy import *
from sqlalchemy.orm import relationship
from ..database import Base



class Agente(Base):
    __tablename__ = "Agentes"

    ASIC = Column(String, primary_key = True)
    NIT = Column(String, nullable = True)
    Razon_Social = Column(String, nullable = True)

    # RELACION 1 A PROYECTOS
    Proyectos = relationship("Proyecto", back_populates = "Agente_re")