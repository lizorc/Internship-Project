from sqlalchemy import *
from ..database import Base



class Valor(Base):
    __tablename__ = "Valores"

    ID = Column(Integer, index = True, primary_key = True)
    Periodo = Column(Date, nullable = False)
    Tipo = Column(String, nullable = False)
    Valor = Column(Float, nullable = False)