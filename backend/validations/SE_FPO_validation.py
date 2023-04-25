from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas import SE_FPO_schema
from ..models import SE_FPO_model
from ..CRUD import SE_FPO_crud, PRO_crud



# CREAR
def validar_seguimientos_FPO_crear(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, Proyecto: str):
    
    # VERIFICAR QUE LA FECHA OFICIAL TENGA LA SINTAXIS CORRECTA
    if seguimiento_FPO.Fecha_Oficial != None:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Oficial, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Oficial Invalida. Formato: YYYY-MM-DD")
    
    if seguimiento_FPO.Fecha_Oficial == None:
        poner_fecha_oficial(db, seguimiento_FPO, Proyecto)

    # VERIFICAR QUE LA FECHA REAL TENGA LA SINTAXIS CORRECTA
    if seguimiento_FPO.Fecha_Real != None:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Real, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Real Invalida. Formato: YYYY-MM-DD")
    
    if seguimiento_FPO.Fecha_Real == None:
        poner_fecha_real(db, seguimiento_FPO, Proyecto)

    # VERIFICAR QUE LA FECHA INICIO DE VIGENCIA TENGA LA SINTAXIS CORRECTA
    if True:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Inicio de Vigencia Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE EL TIPO TENGA INFORMACIÓN
    if len(seguimiento_FPO.Tipo_Doc) == 0:
        raise HTTPException(status_code = 400, detail = "Tipo de Documento sin información...")
    
    # VERIFICAR QUE EL TIPO DE DOCUMENTO TENGA LO CORRECTO
    if not (seguimiento_FPO.Tipo_Doc == 'MME' or seguimiento_FPO.Tipo_Doc == 'CC'  
            or seguimiento_FPO.Tipo_Doc == 'CREG' or seguimiento_FPO.Tipo_Doc == 'UPME'):
        raise HTTPException(status_code = 400, detail = "Tipo Documento invalido. Opciones permitidas: MME , CC , CREG o UPME")


#ACTUALIZAR 
def validar_seguimientos_FPO_actualizar(seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Update):

    # VERIFICAR QUE LA FECHA OFICIAL TENGA LA SINTAXIS CORRECTA
    if seguimiento_FPO.Fecha_Oficial != None:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Oficial, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Oficial Invalida. Formato: YYYY-MM-DD")

    # VERIFICAR QUE LA FECHA REAL TENGA LA SINTAXIS CORRECTA
    if seguimiento_FPO.Fecha_Real != None:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Real, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Real Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE LA FECHA INICIO DE VIGENCIA TENGA LA SINTAXIS CORRECTA
    if seguimiento_FPO.Fecha_Inicio_Vigen != None:
        try:
            datetime.strftime(seguimiento_FPO.Fecha_Inicio_Vigen, '%Y-%m-%d')
            pass
        except ValueError:
            raise HTTPException(status_code = 400, detail = "Fecha Inicio de Vigencia Invalida. Formato: YYYY-MM-DD")
    
    # VERIFICAR QUE EL TIPO DE DOCUMENTO TENGA LO CORRECTO
    if seguimiento_FPO.Tipo_Doc != None and not (seguimiento_FPO.Tipo_Doc == 'MME' or seguimiento_FPO.Tipo_Doc == 'CC' or seguimiento_FPO.Tipo_Doc == 'CREG' or seguimiento_FPO.Tipo_Doc == 'UPME'):
        raise HTTPException(status_code = 400, detail = "Tipo Documento invalido. Opciones permitidas: MME , CC , CREG o UPME")


# CONFIRMAR EXISTENCIA 
def verificar_seguimiento_FPO(db: Session, Seg_FPO_id: int):

    # VERIFICAR QUE EL ID DE LA seguimiento FPO ESTE EN EL SISTEMA
    db_= SE_FPO_crud.get_seguimiento_FPO(db, Seg_FPO_id)
    if not db_:
        raise HTTPException(status_code = 404, detail = f"seguimiento FPO {Seg_FPO_id} no existe en Base de Datos")


# PONER FECHA_OFICIAL
def poner_fecha_oficial(db: Session, Proyecto: str):
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
            get_CP = get_CP.get("Proyecto")
            if get_CP == Proyecto:
                get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                get_F = get_F.get("Fecha_Fin_Vigen")
                if get_F == None:
                    get_FO = SE_FPO_crud.get_Oficial_Seg_FPO_id(db, i)
                    get_FO = get_FO.get("Fecha_Oficial")
                    return get_FO
            i = i + 1

# PONER FECHA_OFICIAL
def poner_fecha_oficial1(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, Proyecto: str):
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
            get_CP = get_CP.get("Proyecto")
            if get_CP == Proyecto:
                get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                get_F = get_F.get("Fecha_Fin_Vigen")
                if get_F == None:
                    if seguimiento_FPO.Fecha_Oficial == None:
                        get_FO = SE_FPO_crud.get_Oficial_Seg_FPO_id(db, i)
                        get_FO = get_FO.get("Fecha_Oficial")
                        seguimiento_FPO.Fecha_Oficial = get_FO  
                        return seguimiento_FPO.Fecha_Oficial
                    else:
                        get_FO = SE_FPO_crud.get_Oficial_Seg_FPO_id(db, i)
                        get_FO = get_FO.get("Fecha_Oficial")
                        return get_FO
            i = i + 1
    
                    
# PONER FECHA_OFICIAL
def poner_fecha_real(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, Proyecto: str):
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
            get_CP = get_CP.get("Proyecto")
            if get_CP == Proyecto:
                get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                get_F = get_F.get("Fecha_Fin_Vigen")
                if get_F == None and seguimiento_FPO.Fecha_Real == None:
                    get_FR = SE_FPO_crud.get_Real_Seg_FPO_id(db, i)
                    get_FR = get_FR.get("Fecha_Real")
                    seguimiento_FPO.Fecha_Real = get_FR  
                    return seguimiento_FPO.Fecha_Real
            i = i + 1


# PONER FECHA_FIN_VIGENCIA
def poner_fecha_fin_crear(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, Proyecto: str):
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
            get_CP = get_CP.get("Proyecto")
            if get_CP == Proyecto:
                get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                get_F = get_F.get("Fecha_Fin_Vigen")
                if get_F == None:
                    get_F = SE_FPO_crud.get_seguimiento_FPO(db, i)
                    get_F.Fecha_Fin_Vigen = seguimiento_FPO.Fecha_Inicio_Vigen
                    db.commit()
            i = i + 1

# PONER FECHA_FIN_VIGENCIA
def poner_fecha_fin(db: Session, Proyecto: str):
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
            get_CP = get_CP.get("Proyecto")
            if get_CP == Proyecto:
                get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                get_F = get_F.get("Fecha_Fin_Vigen")
                if get_F == None:
                    get_F = SE_FPO_crud.get_seguimiento_FPO(db, i)
                    get_F.Fecha_Fin_Vigen = date.today()
                    db.commit()
            i = i + 1


# PONER FPOS DESDE LA API
def poner_fechas(db: Session, Proyecto: str, FO_API: date, FR_API: date):
    poner_fecha_fin(db, Proyecto)
    db_ = SE_FPO_model.Seguimiento_FPO(Proyecto = Proyecto, Fecha_Oficial = FO_API, Fecha_Real = FR_API, Fecha_Inicio_Vigen = date.today(), Fecha_Fin_Vigen = None, Tipo_Doc = "", Descrip_Doc = "", Documento = "")
    db.add(db_)
    get_P = PRO_crud.get_proyecto(db, Proyecto)
    get_P.FPO_Oficial = FO_API
    get_P.FPO_Real = FR_API
    db.commit()
    db.refresh(db_)
    return db_


# ACTUALIZAR FECHA_FIN_VIGEN
def actualizar_fecha_fin(db: Session, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Update, Seg_FPO_id: int):
    get_F_an = SE_FPO_crud.get_Fecha_Inicio_Seg_FPO_id(db, Seg_FPO_id)
    get_F_an = get_F_an.get("Fecha_Inicio_Vigen")
    get_CP = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, Seg_FPO_id)
    get_CP = get_CP.get("Proyecto")
    db__ = SE_FPO_crud.get_seguimientos_FPO(db)
    if db__:
        i = 1
        while SE_FPO_crud.get_seguimiento_FPO(db, i):
            if i != Seg_FPO_id:
                get_CP1 = SE_FPO_crud.get_Proyecto_Seg_FPO_id(db, i)
                get_CP1 = get_CP1.get("Proyecto")
                if get_CP1 == get_CP:
                    get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, i)
                    get_F = get_F.get("Fecha_Fin_Vigen")
                    if get_F == get_F_an:
                        get_F = SE_FPO_crud.get_seguimiento_FPO(db, i)
                        get_F.Fecha_Fin_Vigen = seguimiento_FPO.Fecha_Inicio_Vigen
                        db.commit()
            i = i + 1
    db1__ = SE_FPO_crud.get_seguimiento_FPO(db, Seg_FPO_id + 1)
    if not db1__:
        get_P = SE_FPO_crud.get_proyecto(db, get_CP)
        get_P.FPO_Oficial = seguimiento_FPO.Fecha_Oficial
        get_P.FPO_Real = seguimiento_FPO.Fecha_Real
        db.commit()


# CAMBIAR FECHA_FIN_VIGEN y FPOS
def cambiar_fechas_eliminar(db: Session, get_CP: str):
    db__ = SE_FPO_crud.get_Seg_FPO_proyecto(db, get_CP)
    if not db__:
        get_P = PRO_crud.get_proyecto(db, get_CP)
        get_P.FPO_Oficial = None
        get_P.FPO_Real = None
        db.commit()
    
    if db__:
        id = db__.pop()._asdict()
        id = id.get("ID")

        get_FO = SE_FPO_crud.get_Oficial_Seg_FPO_id(db, id)
        get_FO = get_FO.get("Fecha_Oficial")
        get_FR = SE_FPO_crud.get_Real_Seg_FPO_id(db, id)
        get_FR = get_FR.get("Fecha_Real")
        get_P = SE_FPO_crud.get_proyecto(db, get_CP)
        get_P.FPO_Oficial = get_FO
        get_P.FPO_Real = get_FR
        db.commit()

        get_F = SE_FPO_crud.get_Fecha_Fin_Seg_FPO_id(db, id)
        get_F = get_F.get("Fecha_Fin_Vigen")        
        get_F = SE_FPO_crud.get_seguimiento_FPO(db, id)
        get_F.Fecha_Fin_Vigen = None
        db.commit()     