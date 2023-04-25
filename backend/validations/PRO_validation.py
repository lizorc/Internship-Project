from datetime import datetime 
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import PRO_schema
from ..CRUD import PRO_crud



# CREAR
def validar_proyectos_crear(db: Session, proyecto: PRO_schema.Proyecto_Create): 
    
    # VERIFICAR QUE EL CODIGO_PROYECTO TENGA INFORMACIÓN
    if len(proyecto.Codigo_Proyecto) == 0:
        raise HTTPException(status_code = 400, detail = "Código del Proyecto sin información")
    
    # VERIFICAR QUE EL CODIGO_PROYECTO NO ESTE EN EL SISTEMA 
    db_CP = PRO_crud.get_proyecto(db, Codigo_Proyecto = proyecto.Codigo_Proyecto)
    if db_CP:
        raise HTTPException(status_code = 400, detail = f"Código del Proyecto {proyecto.Codigo_Proyecto} ya registrado")

    # VERIFICAR QUE EL UPME NO ESTE EN EL SISTEMA 
    db_UPME = PRO_crud.get_proyecto_UPME(db, UPME = proyecto.UPME) 
    if db_UPME and len(proyecto.UPME) > 0:
        raise HTTPException(status_code = 400, detail = f"Código UPME {proyecto.UPME} ya registrado")
    
    # VERIFICAR QUE EL Res_CREG NO ESTE EN EL SISTEMA 
    db_CR = PRO_crud.get_proyecto_Res_CREG(db, Res_CREG = proyecto.Res_CREG)
    if db_CR and len(proyecto.Res_CREG) > 0:
        raise HTTPException(status_code = 400, detail = f"Resolución CREG {proyecto.Res_CREG} ya registrado")

    # VERIFICAR QUE EL NOMBRE DEL PROYECTO TENGA INFORMACIÓN
    if len(proyecto.Nombre) == 0:
        raise HTTPException(status_code = 400, detail = "Nombre del Proyecto sin información")
    
    # VERIFICAR QUE LA CATEGORIA TENGA INFORMACIÓN
    if len(proyecto.Categoria) == 0:
        raise HTTPException(status_code = 400, detail = "Categoría sin información")
    
    # VERIFICAR QUE LA CATEGORIA TENGA LO CORRECTO
    if not (proyecto.Categoria == 'STN' or proyecto.Categoria == 'STR'):
        raise HTTPException(status_code = 400, detail = "Categoría invalida. Opciones permitidas: STN o STR")
    
    # VERIFICAR QUE LA SUBCATEGORIA TENGA INFORMACIÓN
    if len(proyecto.Subcategoria) == 0:
        raise HTTPException(status_code = 400, detail = "Subcategoría sin información")
    
    # VERIFICAR QUE LA SUBCATEGORIA TENGA LO CORRECTO
    if proyecto.Categoria == 'STN' and not (proyecto.Subcategoria == 'Convocatoria' or proyecto.Subcategoria == 'Ampliación'):
        raise HTTPException(status_code = 400, detail = "Subcategoría invalida. Opciones permitidas: Convocatoria o Ampliación")
    
        # VERIFICAR QUE LA SUBCATEGORIA TENGA LO CORRECTO
    if proyecto.Categoria == 'STR' and not (proyecto.Subcategoria == 'Convocatoria' or proyecto.Subcategoria == 'Expansión OR'):
        raise HTTPException(status_code = 400, detail = "Subcategoría invalida. Opciones permitidas: Convocatoria o Expansión OR")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STN' and proyecto.Subcategoria == 'Convocatoria') and not (proyecto.Rol_Agente == 'Ejecutor' or proyecto.Rol_Agente == 'Conexión' or proyecto.Rol_Agente == 'Usuario' or proyecto.Rol_Agente == 'Generador'):
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Convocatorias del STN las opciones permitidas son: Ejecutor, Conexión, Usuario y Generador")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STR' and proyecto.Subcategoria == 'Convocatoria') and not (proyecto.Rol_Agente == 'Ejecutor' or proyecto.Rol_Agente == 'Conexión'):
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Convocatorias del STR las opciones permitidas son: Ejecutor y Conexión")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STN' and proyecto.Subcategoria == 'Ampliación') and not proyecto.Rol_Agente == 'Ejecutor':
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Ampliaciones del STN y la opción permitida es: Ejecutor")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STR' and proyecto.Subcategoria == 'Expansión OR') and not proyecto.Rol_Agente == 'Ejecutor':
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Expansiones OR del STR la opción permitida es: Ejecutor")


# ACTUALIZAR
def validar_proyectos_actualizar(db: Session, proyecto: PRO_schema.Proyecto_Update, Codigo_Proyecto: str):
    
    # VERIFICAR QUE EL CODIGO_PROYECTO NO ESTE EN EL SISTEMA 
    db_CP = PRO_crud.get_proyecto(db, Codigo_Proyecto = proyecto.Codigo_Proyecto)
    if db_CP and (proyecto.Codigo_Proyecto != Codigo_Proyecto):
        raise HTTPException(status_code = 400, detail = f"Código del Proyecto {proyecto.Codigo_Proyecto} ya registrado")

    # VERIFICAR QUE EL UPME NO ESTE EN EL SISTEMA 
    db_UPME = PRO_crud.get_proyecto_UPME(db, UPME = proyecto.UPME) 
    if db_UPME and len(proyecto.UPME) > 0:
        raise HTTPException(status_code = 400, detail = f"Código UPME {proyecto.UPME} ya registrado")
    
    # VERIFICAR QUE EL Res_CREG NO ESTE EN EL SISTEMA 
    db_CR = PRO_crud.get_proyecto_Res_CREG(db, Res_CREG = proyecto.Res_CREG)
    if db_CR and len(proyecto.Res_CREG) > 0:
        raise HTTPException(status_code = 400, detail = f"Resolución CREG {proyecto.Res_CREG} ya registrado")
    
    # VERIFICAR QUE LA CATEGORIA TENGA LO CORRECTO
    if proyecto.Categoria != None and not (proyecto.Categoria == 'STN' or proyecto.Categoria == 'STR'):
        raise HTTPException(status_code = 400, detail = "Categoría invalida. Opciones permitidas: STN o STR")
    
    # VERIFICAR QUE LA SUBCATEGORIA TENGA LO CORRECTO
    if (proyecto.Categoria != None and proyecto.Subcategoria != None) or (proyecto.Subcategoria != None):
        db_C = PRO_crud.get_Categoria_CP(db, Codigo_Proyecto)
        if (proyecto.Categoria == 'STN' or db_C == 'STN') and not (proyecto.Subcategoria == 'Convocatoria' or proyecto.Subcategoria == 'Ampliación'):
            raise HTTPException(status_code = 400, detail = "Subcategoría invalida. Opciones permitidas: Convocatoria o Ampliación")
    
        if (proyecto.Categoria == 'STR'  or db_C == 'STR') and not (proyecto.Subcategoria == 'Convocatoria' or proyecto.Subcategoria == 'Expansión OR'):
            raise HTTPException(status_code = 400, detail = "Subcategoría invalida. Opciones permitidas: Convocatoria o Expansión OR")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STN'  and proyecto.Subcategoria == 'Convocatoria') and not (proyecto.Rol_Agente == 'Ejecutor' or proyecto.Rol_Agente == 'Conexión' or proyecto.Rol_Agente == 'Usuario' or proyecto.Rol_Agente == 'Generador'):
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Convocatorias del STN las opciones permitidas son: Ejecutor, Conexión, Usuario y Generador")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STR' and proyecto.Subcategoria == 'Convocatoria') and not (proyecto.Rol_Agente == 'Ejecutor' or proyecto.Rol_Agente == 'Conexión'):
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Convocatorias del STR las opciones permitidas son: Ejecutor y Conexión")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STN' and proyecto.Subcategoria == 'Ampliación') and not proyecto.Rol_Agente == 'Ejecutor':
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Ampliaciones del STN y la opción permitida es: Ejecutor")
    
    # VERIFICAR QUE EL ROL Y LA SUBCATEGORIA CONCUERDEN
    if (proyecto.Categoria == 'STR' and proyecto.Subcategoria == 'Expansión OR') and not proyecto.Rol_Agente == 'Ejecutor':
        raise HTTPException(status_code = 400, detail = "Categoria y Rol del Agente no concuerdan. Para Expansiones OR del STR la opción permitida es: Ejecutor")


# CONFIRMAR EXISTENCIA 
def verificar_proyecto(db: Session, Codigo_Proyecto: str):

    # VERIFICAR QUE EL CODIGO_PROYECTO DEL PROYECTO ESTE EN EL SISTEMA
    db_ = PRO_crud.get_proyecto(db, Codigo_Proyecto)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Proyecto {Codigo_Proyecto} no existe en Base de Datos")


# CONFIRMAR EXISTENCIA 
def verificar_UPME(db: Session, UPME: str):

    # VERIFICAR QUE EL CODIGO_PROYECTO DEL PROYECTO ESTE EN EL SISTEMA
    db_ = PRO_crud.get_proyecto_UPME(db, UPME)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"UPME {UPME} no existe")


# CONFIRMAR EXISTENCIA 
def verificar_CREG(db: Session, Res_CREG: str):
    
    # VERIFICAR QUE EL CODIGO_PROYECTO DEL PROYECTO ESTE EN EL SISTEMA
    db_ = PRO_crud.get_proyecto_Res_CREG(db, Res_CREG)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"Resolución CREG {Res_CREG} no existe")