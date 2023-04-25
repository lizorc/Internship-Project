from sqlalchemy.orm import Session
from ..models import PRO_model
from ..schemas import PRO_schema



# OBTENER TODOS LOS PROYECTOS
def get_proyectos(db: Session):
    return db.query(PRO_model.Proyecto).all()

# FILTRAR PROYECTO POR ID
def get_proyecto_id(db: Session, ID: int):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.ID == ID).first()

# FILTRAR PROYECTO POR UPME
def get_proyecto_UPME(db: Session, UPME: str): 
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.UPME == UPME).first()

# FILTRAR PROYECTO POR AGENTE
def get_proyecto_agente(db: Session, Agente: str):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Agente == Agente).all()

# FILTRAR PROYECTO POR CATEGORIA
def get_proyecto_categoria(db: Session, Categoria: str):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Categoria == Categoria).all()

# FILTRAR PROYECTO POR CR
def get_proyecto_Res_CREG(db: Session, Res_CREG: str): 
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Res_CREG == Res_CREG).first() 

# FILTRAR PROYECTO POR SUBCATEGORIA
def get_proyecto_subcategoria(db: Session, Subcategoria: str):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Subcategoria == Subcategoria).all()

# FILTRAR PROYECTO POR CP
def get_proyecto(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()

# FILTRAR PROYECTO POR ID
def get_proyecto_id_CP(db: Session, ID: int):
    return db.query(PRO_model.Proyecto.Codigo_Proyecto).filter(PRO_model.Proyecto.ID == ID).first()._asdict()

# CONSULTAR DATO DE FPO OFICIAL EN PROYECTO
def get_FO_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.FPO_Oficial).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTAR DATO DE FPO REAL EN PROYECTO
def get_FR_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.FPO_Real).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTAR DATO DE PRECIO EN PROYECTO
def get_Precio_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Precio_Base).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTA DE CATEGORIA EN PROYECTO
def get_Categoria_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Categoria).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTA DE SUBCATEGORIA EN PROYECTO
def get_Subcategoria_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Subcategoria).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTA DE ROL EN PROYECTO
def get_Rol_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Rol_Agente).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTA DE AGENTE EN PROYECTO
def get_Agente_CP(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Agente).filter(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto).first()._asdict()

# CONSULTA DE AGENTE EN PROYECTO
def get_Agente_proyecto(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Agente).select_from(PRO_model.Proyecto).where(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto)

# CONSULTA DE ROL AGENTE EN PROYECTO
def get_Rol_proyecto(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Rol_Agente).select_from(PRO_model.Proyecto).where(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto)

# CONSULTA DE CATEGORIA EN PROYECTO 
def get_Categoria_proyecto(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Categoria).select_from(PRO_model.Proyecto).where(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto)

# CONSULTA DE SUBCATEGORIA EN PROYECTO
def get_Subcategoria_proyecto(db: Session, Codigo_Proyecto: str):
    return db.query(PRO_model.Proyecto.Subcategoria).select_from(PRO_model.Proyecto).where(PRO_model.Proyecto.Codigo_Proyecto == Codigo_Proyecto)

# FILTRAR PROYECTO POR CATEGORIA Y SUBCATEGORIA
def get_proyecto_categoria_subcategoria(db: Session, Categoria: str, Subcategoria: str):
    return db.query(PRO_model.Proyecto).filter(PRO_model.Proyecto.Categoria == Categoria).filter(PRO_model.Proyecto.Subcategoria == Subcategoria).all()

# CREAR PROYECTO ASOCIADO A UN AGENTE 
def create_proyecto_en_agente(db: Session, proyecto: PRO_schema.Proyecto_Create, Agente: str):
    db_ = PRO_model.Proyecto(**proyecto.dict(), Agente = Agente, FPO_Oficial = None, FPO_Real = None)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ACTUALIZAR PROYECTO
def update_proyecto(db: Session, proyecto: PRO_schema.Proyecto_Update, Codigo_Proyecto: str):
    db_ = get_proyecto(db, Codigo_Proyecto)
    data = proyecto.dict(exclude_unset = True)
    for key, value in data.items():
        setattr(db_, key, value)
    db.add(db_)
    db.commit()
    db.refresh(db_)
    return db_

# ELIMINAR PROYECTO
def delete_proyecto(db: Session, Codigo_Proyecto: str):
    Codigo_Proyecto = get_proyecto(db, Codigo_Proyecto)
    db.delete(Codigo_Proyecto)
    db.commit()
    return {f"Proyecto {Codigo_Proyecto} eliminado"}