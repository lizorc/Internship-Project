from datetime import date
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from .database import SessionLocal, engine
from starlette.responses import RedirectResponse
from .models import VAL_model, AGE_model, PRO_model, DA_CON_model, DA_AMP_model, DA_EXP_model, SE_FPO_model, LIQ_model, CO_STN_model, CO_STR_model, AMP_STN_model, EXP_STR_model
from .schemas import VAL_schema, AGE_schema, PRO_schema, DA_CON_schema, DA_AMP_schema, DA_EXP_schema, SE_FPO_schema, LIQ_schema, CO_STN_schema, CO_STR_schema, AMP_STN_schema, EXP_STR_schema
from .CRUD import VAL_crud, AGE_crud, PRO_crud, DA_CON_crud, DA_AMP_crud, DA_EXP_crud, SE_FPO_crud, LIQ_crud, CO_STN_crud, CO_STR_crud, AMP_STN_crud, EXP_STR_crud
from .validations import VAL_validation, AGE_validation, PRO_validation, DA_CON_validation, DA_AMP_validation, DA_EXP_validation, SE_FPO_validation, LIQ_validation, CO_STN_validation, CO_STR_validation, AMP_STN_validation, EXP_STR_validation
 

VAL_model.Base.metadata.create_all(bind = engine)
AGE_model.Base.metadata.create_all(bind = engine)
PRO_model.Base.metadata.create_all(bind = engine)
DA_CON_model.Base.metadata.create_all(bind = engine)
DA_AMP_model.Base.metadata.create_all(bind = engine)
DA_EXP_model.Base.metadata.create_all(bind = engine)
SE_FPO_model.Base.metadata.create_all(bind = engine)
LIQ_model.Base.metadata.create_all(bind = engine)
CO_STN_model.Base.metadata.create_all(bind = engine)
CO_STR_model.Base.metadata.create_all(bind = engine)
AMP_STN_model.Base.metadata.create_all(bind = engine)
EXP_STR_model.Base.metadata.create_all(bind = engine)

app = FastAPI(title= "Automatización del seguimiento a la expansión del STN y STR")


#* Dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#* PAGINA INICIAL 
@app.get('/', tags = ["Default"])
async def root():
    return RedirectResponse(url = "/docs")



#* FUNCIONES DE VALORES
# CREAR VALOR
@app.post("/Valor/", response_model = VAL_schema.Valor, tags = ["Valores de IPP y TRM"])
def crear_valor(Val: VAL_schema.Valor_Create, db: Session = Depends(get_db)):
    """
        Crear valor mensual de IPP o TRM

    - **Periodo**: Mes de validez para el dato con formato YYYY-mm-dd. Requerido
    - **Tipo**: Nombre identificador que puede ser IPP o TRM. Requerido
    - **Valor**: Valor del dato numerico. Requerido

    **Importante**: 
    
    No se permite que existan varias fechas iguales para un mismo tipo.

    """
    VAL_validation.validar_valores_crear(db, Val)
    return VAL_crud.create_valor(db, Val)


# ACTUALIZAR VALOR
@app.put("/Valor/{Periodo}/Periodo/{Tipo}/Tipo", response_model = VAL_schema.Valor, tags = ["Valores de IPP y TRM"])
def actualizar_valor(Periodo: date, Tipo: str, Val: VAL_schema.Valor_Update, db: Session = Depends(get_db)):
    """
        Actualizar valor mensual de IPP o TRM de acuerdo a:

    - **Periodo**: YYYY-mm-dd 
    - **Tipo**: IPP o TRM

    **Datos cambiables:**

    - **Periodo**: Mes de validez para el dato con formato YYYY-mm-dd
    - **Tipo**: Nombre identificador para el dato. Puede ser IPP o TRM
    - **Valor**: Valor del dato numerico. 

    """
    VAL_validation.verificar_valor(db, Periodo, Tipo)
    VAL_validation.validar_valores_actualizar(db, Val, Periodo, Tipo)
    return VAL_crud.update_valor(db, Val, Periodo, Tipo)


# ELIMINAR VALOR
@app.delete("/Valor/{Periodo}/Periodo/{Tipo}/Tipo", tags = ["Valores de IPP y TRM"])
def eliminar_valor(Periodo: date, Tipo: str, db: Session = Depends(get_db)):
    """
            Eliminar valor mensual de IPP o TRM de acuerdo a:
        
        - **Periodo**: YYYY-mm-dd 
        - **Tipo**: IPP o TRM

    """
    VAL_validation.verificar_valor(db, Periodo, Tipo)
    return VAL_crud.delete_valor(db, Periodo, Tipo)


# MOSTRAR TODOS LOS VALORES
@app.get("/Valores/", response_model = list[VAL_schema.Valor], tags = ["Valores de IPP y TRM"])
def leer_valores(db: Session = Depends(get_db)):
    """
            Buscar todos los valores
        No se requiere introducir datos

    """
    return VAL_crud.get_valores(db)


# MOSTRAR VALOR
@app.get("/Valor/{Periodo}/Periodo/{Tipo}/Tipo", response_model = VAL_schema.Valor, tags = ["Valores de IPP y TRM"])
def leer_valor(Periodo: date, Tipo: str, db: Session = Depends(get_db)):
    """
            Buscar un valor de acuerdo a:
        
        - **Periodo**: YYYY-mm-dd 
        - **Tipo**: IPP o TRM

    """
    VAL_validation.verificar_valor(db, Periodo, Tipo)
    return VAL_crud.get_valor(db, Periodo, Tipo)


# MOSTRAR VALOR POR PERIODO
@app.get("/Valor/{Periodo}/Periodo/", response_model = list[VAL_schema.Valor_Periodo], tags = ["Valores de IPP y TRM"])
def leer_valor(Periodo: date, db: Session = Depends(get_db)):
    """
            Buscar uno o mas valores de acuerdo a:
        
        - **Periodo**: YYYY-mm-dd 

    """
    if VAL_crud.get_Periodo_valor(db, Periodo):
        return VAL_crud.get_Periodo_valor(db, Periodo)
    else:
        raise HTTPException(status_code = 404, detail = f"No hay registro para el Periodo {Periodo}")


# MOSTRAR VALOR POR TIPO
@app.get("/Valor/{Tipo}/Tipo/", response_model = list[VAL_schema.Valor_Tipo], tags = ["Valores de IPP y TRM"])
def leer_valor(Tipo: str, db: Session = Depends(get_db)):
    """
            Buscar uno o mas valores de acuerdo a:
        
        - **Tipo**: IPP o TRM

    """
    if VAL_crud.get_Tipo_valor(db, Tipo):
        return VAL_crud.get_Tipo_valor(db, Tipo)
    else:
        raise HTTPException(status_code = 404, detail = f"No hay registro para el Tipo {Tipo}")






#* FUNCIONES DE AGENTE
# CREAR AGENTE
@app.post("/Agente/", response_model = AGE_schema.Agente, tags = ["Agentes"])
def crear_agente(agente: AGE_schema.Agente_Create, db: Session = Depends(get_db)):
    """
        Crear Agente

    - **ASIC**: Codigo identificador del Agente. Requerido
    - **NIT**: Numero de Identificación Tributaria del Agente. Opcional
    - **Razon_Social**: Dominicio legal por el que se conoce al Agente. Opcional

    **Importante**: No se permite que exista mas de un ASIC igual.

    """
    AGE_validation.validar_agentes_crear(db, agente)
    return AGE_crud.create_agente(db, agente)


# ACTUALIZAR AGENTE
@app.put("/Agente/{ASIC}", response_model = AGE_schema.Agente, tags = ["Agentes"])
def actualizar_agente(ASIC: str, agente: AGE_schema.Agente_Update, db: Session = Depends(get_db)):
    """
        Actualizar Agente de acuerdo a:

    - **ASIC**: Codigo identificador del Agente

    **Datos cambiables:**

    - **ASIC**: Codigo identificador del Agente.
    - **NIT**: Numero de Identificación Tributaria del Agente.
    - **Razon_Social**: Dominicio legal por el que se conoce al Agente.

    """
    AGE_validation.verificar_agente(db, ASIC)
    AGE_validation.validar_agentes_actualizar(db, agente, ASIC)
    return AGE_crud.update_agente(db, agente, ASIC)
    

# ELIMINAR AGENTE
@app.delete("/Agente/{ASIC}", tags = ["Agentes"])
def eliminar_agente(ASIC: str, db: Session = Depends(get_db)):
    """
            Eliminar Agente de acuerdo a:
        
        - **ASIC**: Codigo identificador del Agente

    """
    AGE_validation.verificar_agente(db, ASIC)
    return AGE_crud.delete_agente(db, ASIC)


# MOSTRAR TODOS LOS AGENTES
@app.get("/Agentes/", response_model = list[AGE_schema.Agente], tags = ["Agentes"])
def leer_agentes(db: Session = Depends(get_db)):
    """
            Buscar todos los agentes
        No se requiere introducir datos

    """
    return AGE_crud.get_agentes(db)


# MOSTRAR AGENTE POR ASIC 
@app.get("/Agente/{ASIC}", response_model = AGE_schema.Agente, tags = ["Agentes"])
def leer_agente(ASIC: str, db: Session = Depends(get_db)):
    """
            Buscar un agente de acuerdo a:
        
        - **ASIC**: Codigo identificador del Agente

    """
    AGE_validation.verificar_agente(db, ASIC)
    return AGE_crud.get_agente(db, ASIC)






#* FUNCIONES DE PROYECTO
# CREAR PROYECTO ASOCIADO A UN AGENTE
@app.post("/Proyecto/{Agente}/Agente/", response_model = PRO_schema.Proyecto, tags = ["Proyectos"])
def crear_proyecto_por_agente(Agente: str, proyecto: PRO_schema.Proyecto_Create, db: Session = Depends(get_db)):
    """
        Crear Proyecto

    - **Agente**: Codigo identificador del Agente (ASIC)

    **Datos Solicitados** 

    - **Rol_Agente**: Rol que tiene el Agente en el Proyecto. Requerido
        - **STN - Ampliación**: Ejecutor
        - **STR - Expansión OR**: Ejecutor
        - **STR - Convocatoria**: Ejecutor o Conexión
        - **STN - Convocatoria**: Ejecutor, Conexión, Usuario o Generador
    - **Codigo_Proyecto**: Codigo identificador del Proyecto. Requerido
    - **UPME**: Numero de la Convocatoria del Proyecto. Opcional
    - **Res_CREG**: Resolución CREG del Proyecto. Opcional
    - **Nombre**: Nombre del Proyecto. Requerido
    - **Categoria**: Categoria a la que pertenece el Proyectoque que puede ser STN o STR. Requerido
    - **Subcategoria**: Subcategoria a la que pertenece el Proyecto dependiendo de la categoria. Requerido
        - **STN**: Convocatoria o Ampliación 
        - **STR**: Convocatoria o Expansión OR
    - **Precio_Base**: IPP o PPI Base para el Proyecto. Opcional

    **Importante**: No se permite que exista mas de un Codigo_Proyecto igual.
    """
    AGE_validation.verificar_agente(db, Agente)
    PRO_validation.validar_proyectos_crear(db, proyecto)
    return PRO_crud.create_proyecto_en_agente(db, proyecto, Agente)


# ACTUALIZAR PROYECTO
@app.put("/Proyecto/{Codigo_Proyecto}", response_model = PRO_schema.Proyecto, tags = ["Proyectos"])
def actualizar_proyecto(Codigo_Proyecto: str, proyecto: PRO_schema.Proyecto_Update, db: Session = Depends(get_db)):
    """
        Actualizar Proyecto de acuerdo a:

    - **Codigo_Proyecto**: ASIC del Agente

    **Datos cambiables:**

    - **Rol_Agente**: Rol que tiene el Agente en el Proyecto.
        - **STN - Ampliación**: Ejecutor
        - **STR - Expansión OR**: Ejecutor
        - **STR - Convocatoria**: Ejecutor o Conexión
        - **STN - Convocatoria**: Ejecutor, Conexión, Usuario o Generador
    - **Codigo_Proyecto**: Codigo identificador del Proyecto.
    - **UPME**: Numero de la Convocatoria del Proyecto.
    - **Res_CREG**: Resolución CREG del Proyecto.
    - **Nombre**: Nombre del Proyecto.
    - **Categoria**: Categoria a la que pertenece el Proyectoque que puede ser STN o STR.
    - **Subcategoria**: Subcategoria a la que pertenece el Proyecto dependiendo de la categoria.
        - **STN**: Convocatoria o Ampliación 
        - **STR**: Convocatoria o Expansión OR
    - **Precio_Base**: IPP o PPI Base para el Proyecto.

    """
    PRO_validation.verificar_proyecto(db, Codigo_Proyecto)
    PRO_validation.validar_proyectos_actualizar(db, proyecto, Codigo_Proyecto)
    return PRO_crud.update_proyecto(db, proyecto, Codigo_Proyecto)


# ELIMINAR PROYECTO
@app.delete("/Proyecto/{Codigo_Proyecto}", tags = ["Proyectos"])
def eliminar_proyecto(Codigo_Proyecto: str, db: Session = Depends(get_db)):
    """
            Eliminar Proyecto de acuerdo a:
        
        - **Codigo_Proyecto**: Codigo identificador del Proyecto

    """
    PRO_validation.verificar_proyecto(db, Codigo_Proyecto)
    return PRO_crud.delete_proyecto(db, Codigo_Proyecto)


# MOSTRAR TODOS LOS PROYECTOS 
@app.get("/Proyectos/", response_model = list[PRO_schema.Proyecto], tags = ["Proyectos"])
def leer_proyectos(db: Session = Depends(get_db)):
    """
            Buscar todos los proyectos
        No se requiere introducir datos

    """
    return PRO_crud.get_proyectos(db)


# MOSTRAR PROYECTO
@app.get("/Proyecto/{Codigo_Proyecto}", response_model = PRO_schema.Proyecto, tags = ["Proyectos"])
def leer_proyecto(Codigo_Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Codigo_Proyecto**: Codigo identificador del Proyecto

    """
    PRO_validation.verificar_proyecto(db, Codigo_Proyecto)
    return PRO_crud.get_proyecto(db, Codigo_Proyecto)


# MOSTRAR PROYECTO POR UPME
@app.get("/Proyecto/{UPME}/UPME", response_model = PRO_schema.Proyecto_UPME, tags = ["Proyectos"])
def leer_proyecto_por_convocatoria_UPME(UPME: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **UPME**: Numero de la Convocatoria del Proyecto.

    """
    PRO_validation.verificar_UPME(db,UPME)
    return PRO_crud.get_proyecto_UPME(db, UPME)


# MOSTRAR PROYECTO POR RES CREG
@app.get("/Proyecto/{Res_CREG}/Res_CREG", response_model = PRO_schema.Proyecto_CREG, tags = ["Proyectos"])
def leer_proyecto_por_resolucion_CREG(Res_CREG: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Res_CREG**: Resolución CREG del Proyecto.

    """
    PRO_validation.verificar_CREG(db, Res_CREG)
    return PRO_crud.get_proyecto_Res_CREG(db, Res_CREG)


# MOSTRAR PROYECTO POR AGENTE
@app.get("/Proyectos/{Agente}/Agente", response_model = list[PRO_schema.Proyecto_Agente], tags = ["Proyectos"])
def leer_proyecto_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Agente**: ASIC del Agente

    """
    AGE_validation.verificar_agente(db, Agente)
    if PRO_crud.get_proyecto_agente(db, Agente):
        return PRO_crud.get_proyecto_agente(db, Agente)
    else:
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR PROYECTO POR CATEGORIA
@app.get("/Proyectos/{Categoria}/Categoria", response_model = list[PRO_schema.Proyecto_Categoria], tags = ["Proyectos"])
def leer_proyecto_por_categoria(Categoria: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Categoria**: STN o STR

    """
    # VERIFICAR QUE LA CATEGORIA TENGA LO CORRECTO
    if not (Categoria == 'STN' or Categoria == 'STR'):
        raise HTTPException(status_code = 400, detail = "Categoría invalida. Opciones permitidas: STN o STR")
    
    return PRO_crud.get_proyecto_categoria(db, Categoria)


# MOSTRAR PROYECTO POR SUBCATEGORIA
@app.get("/Proyectos/{Subcategoria}/Subcategoria", response_model = list[PRO_schema.Proyecto_Subcategoria], tags = ["Proyectos"])
def leer_proyecto_por_subcategoria(Subcategoria: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Subcategoria**: Convocatoria, Ampliación o Expansión OR

    """
    # VERIFICAR QUE LA CATEGORIA TENGA LO CORRECTO
    if not (Subcategoria == 'Convocatoria' or Subcategoria == 'Ampliación' or Subcategoria == 'Expansión OR'):
        raise HTTPException(status_code = 400, detail = "Subcategoría invalida. Opciones permitidas: Convocatoria, Ampliación o Expansión OR")
    
    return PRO_crud.get_proyecto_subcategoria(db, Subcategoria)


# MOSTRAR PROYECTO POR CATEGORIA Y SUBCATEGORIA
@app.get("/Proyectos/{Categoria}/Categoria/{Subcategoria}/Subcategoria", response_model = list[PRO_schema.Proyecto_Categoria_Subcategoria], tags = ["Proyectos"])
def leer_proyecto_por_categoria_y_subcategoria(Categoria: str, Subcategoria: str, db: Session = Depends(get_db)):
    """
            Buscar un proyecto de acuerdo a:
        
        - **Categoria**: STN o STR
        - **Subcategoria**: Convocatoria, Ampliación o Expansión OR

    """
    # VERIFICAR QUE LA CATEGORIA TENGA LO CORRECTO
    if not (Categoria == 'STN' or Categoria == 'STR'):
        raise HTTPException(status_code = 400, detail = "Categoría invalida. Opciones permitidas: STN o STR")

    # VERIFICAR QUE LA SUBCATEGORIA TENGA LO CORRECTO
    if Categoria == 'STN' and not (Subcategoria == 'Convocatoria' or Subcategoria == 'Ampliación'):
        raise HTTPException(status_code = 400, detail = "Categoria y Subcategoría no coinciden. Opciones permitidas para STN: Convocatoria o Ampliación")
    
    # VERIFICAR QUE LA SUBCATEGORIA TENGA LO CORRECTO
    if Categoria == 'STR' and not (Subcategoria == 'Convocatoria' or Subcategoria == 'Expansión OR'):
        raise HTTPException(status_code = 400, detail = "Categoria y Subcategoría no coinciden. Opciones permitidas para STR: Convocatoria o Expansión OR")
    return PRO_crud.get_proyecto_categoria_subcategoria(db, Categoria, Subcategoria)






#* FUNCIONES DE DATO CONVOCATORIA
# CREAR DATO CONVOCATORIA ASOCIADO A UN PROYECTO
@app.post("/Dato_Convocatoria/{Proyecto}/Proyecto", response_model = DA_CON_schema.Dato_Convocatoria, tags = ["Datos de Anualidades para Convocatorias"])
def crear_dato_convocatoria_por_proyecto(Proyecto: str, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Create, db: Session = Depends(get_db)):
    """
        Crear Dato para Convocatoria STN o STR
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    **Datos Solicitados** 

    - **Fecha_Inicio_Vigen**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. Opcional
    - **Fecha_Fin_Vigen**: Fecha donde deja de ser valido los datos con formato YYYY-mm-dd. Opcional
    - **Anualidad**: Valor del ingreso anual esperado de la Convocatoria. Requerido
    - **Porcentaje**: Porcentaje de proiedad para el proyecto. Requerido
    - **PPI**: Producer Price Index del año en cuestión.
        - **STN**: Requerido
        - **STR**: Campo vacio

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    DA_CON_validation.validar_datos_conv_crear(db, Dato_Conv, Proyecto)
    return DA_CON_crud.create_dato_conv_en_proyecto(db, Dato_Conv, Proyecto)


# ACTUALIZAR DATO CONVOCATORIA
@app.put("/Dato_Convocatoria/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_CON_schema.Dato_Convocatoria, tags = ["Datos de Anualidades para Convocatorias"])
def actualizar_dato_convocatoria(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, Dato_Conv: DA_CON_schema.Dato_Convocatoria_Update, db: Session = Depends(get_db)):
    """
        Actualizar Dato para Convocatoria STN o STR de acuerdo a:

    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
    - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd

    **Datos cambiables:**

    - **Fecha_Inicio_Vigen**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd.
    - **Fecha_Fin_Vigen**: Fecha donde deja de ser valido los datos con formato YYYY-mm-dd.
    - **Anualidad**: Valor del ingreso anual esperado de la Convocatoria.
    - **Porcentaje**: Porcentaje de proiedad para el proyecto.
    - **PPI**: Producer Price Index del año en cuestión.
        - **STN**: Requerido
        - **STR**: Campo vacio

    """
    if not DA_CON_crud.get_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")
    
    Dato_Conv_id = DA_CON_crud.get_ID_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Conv_id = Dato_Conv_id.get("ID")
    DA_CON_validation.verificar_dato_conv(db, Dato_Conv_id)
    DA_CON_validation.validar_datos_conv_actualizar(db, Dato_Conv, Dato_Conv_id)
    return DA_CON_crud.update_dato_conv(db, Dato_Conv, Dato_Conv_id)


# ELIMINAR DATO CONVOCATORIA
@app.delete("/Dato_Convocatoria/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", tags = ["Datos de Anualidades para Convocatorias"])
def eliminar_dato_convocatoria(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Eliminar Dato para Convocatoria STN o STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd

    """
    if not DA_CON_crud.get_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")
    
    Dato_Conv_id = DA_CON_crud.get_ID_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Conv_id = Dato_Conv_id.get("ID")
    DA_CON_validation.verificar_dato_conv(db, Dato_Conv_id)
    return DA_CON_crud.delete_dato_conv(db, Dato_Conv_id)
    
    
    


# MOSTRAR TODOS LOS DATOS CONVOCATIRIAS
@app.get("/Datos_Convocatorias/", response_model = list[DA_CON_schema.Dato_Convocatoria], tags = ["Datos de Anualidades para Convocatorias"])
def leer_datos_convocatorias(db: Session = Depends(get_db)):
    """
            Buscar todos los datos de Convocatorias STN o STR
        No se requiere introducir datos

    """
    return DA_CON_crud.get_datos_convocatorias(db)


# MOSTRAR DATO CONVOCATORIA POR PROYECTO
@app.get("/Datos_Convocatorias/{Proyecto}/Proyecto", response_model = list[DA_CON_schema.Dato_Convocatoria_Proyecto], tags = ["Datos de Anualidades para Convocatorias"])
def leer_datos_convocatorias_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar un dato de Convocatoria STN o STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_CON_crud.get_dato_convocatoria_proyecto(db, Proyecto):
        return DA_CON_crud.get_dato_convocatoria_proyecto(db, Proyecto)
    else:
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR TODAS LOS DATOS CONVOCATORIAS POR FECHAS Y PROYECTOS
@app.get("/Datos_Convocatorias/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_CON_schema.Dato_Convocatoria_Proyecto_Fechas, tags = ["Datos de Anualidades para Convocatorias"])
def leer_dato_convocatoria_por_proyectos_y_fechas(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios datos de Convocatorias STN o STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_CON_crud.get_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        return DA_CON_crud.get_dato_convocatoria_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")


# MOSTRAR TODAS LOS DATOS CONVOCATORIAS POR FECHAS 
@app.get("/Datos_Convocatorias/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_CON_schema.Dato_Convocatoria_Fechas, tags = ["Datos de Anualidades para Convocatorias"])
def leer_dato_convocatoria_por_fechas(Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios datos de Convocatorias STN o STR de acuerdo a:
        
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    if DA_CON_crud.get_dato_convocatoria_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        return DA_CON_crud.get_dato_convocatoria_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fechas{Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")







#* FUNCIONES DE DATO AMPLIACION STN
# CREAR DATO AMPLIACION STN ASOCIADO A UN PROYECTO
@app.post("/Dato_Ampliacion_STN/{Proyecto}/Proyecto", response_model = DA_AMP_schema.Dato_Ampliacion_STN, tags = ["Datos Ampliaciones del STN"])
def crear_dato_ampliacion_STN_por_proyecto(Proyecto: str, Dato_AMP_STN: DA_AMP_schema.Dato_Ampliacion_STN_Create, db: Session = Depends(get_db)):
    """
        Crear Dato para Ampliación STN
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    **Datos Solicitados** 

    - **Periodo**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. Requerido
    - **IAT**: . Requerido
    - **CRE**: . Requerido
    - **PAOMR_Actual**: . Requerido
    - **PAOMR_Aprobado**: . Requerido

    **Importante**: No se permite que exista mas de un Periodo igual para un Proyecto.

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    DA_AMP_validation.validar_datos_Amp_STN_crear(db, Dato_AMP_STN, Proyecto)
    return DA_AMP_crud.create_dato_ampliacion_STN_en_proyecto(db, Dato_AMP_STN, Proyecto)


# ACTUALIZAR DATO AMPLIACION STN
@app.put("/Dato_Ampliacion_STN/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_AMP_schema.Dato_Ampliacion_STN, tags = ["Datos Ampliaciones del STN"])
def actualizar_dato_ampliacion_STN(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, Dato_AMP_STN: DA_AMP_schema.Dato_Ampliacion_STN_Update, db: Session = Depends(get_db)):
    """
        Actualizar Dato para Ampliación STN de acuerdo a:

    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
    - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd

    **Datos cambiables:**

    - **Periodo**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd.
    - **IAT**: 
    - **CRE**: 
    - **PAOMR_Actual**: 
    - **PAOMR_Aprobado**: 

    """
    if not DA_AMP_crud.get_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")

    Dato_Amp_id = DA_AMP_crud.get_ID_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Amp_id = Dato_Amp_id.get("ID")
    DA_AMP_validation.verificar_dato_Amp_STN(db, Dato_Amp_id)
    DA_AMP_validation.validar_datos_Amp_STN_actualizar(db, Dato_AMP_STN, Dato_Amp_id)
    return DA_AMP_crud.update_dato_ampliacion_STN(db, Dato_AMP_STN, Dato_Amp_id)


# ELIMINAR DATO AMPLIACION STN
@app.delete("/Dato_Ampliacion_STN/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", tags = ["Datos Ampliaciones del STN"])
def eliminar_dato_expansion_OR_STR(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Eliminar Dato para Ampliación STN de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    if not DA_AMP_crud.get_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")
    
    Dato_Amp_id = DA_AMP_crud.get_ID_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Amp_id = Dato_Amp_id.get("ID")
    DA_AMP_validation.verificar_dato_Amp_STN(db, Dato_Amp_id)
    return DA_AMP_crud.delete_dato_ampliacion_STN(db, Dato_Amp_id)


# MOSTRAR TODOS LOS DATOS AMPLIACIONES STN
@app.get("/Datos_Ampliaciones_STN/", response_model = list[DA_AMP_schema.Dato_Ampliacion_STN], tags = ["Datos Ampliaciones del STN"])
def leer_datos_ampliaciones_STN(db: Session = Depends(get_db)):
    """
            Buscar todos los datos de Ampliación STN
        No se requiere introducir datos

    """
    return DA_AMP_crud.get_dato_ampliaciones_STN(db)


# MOSTRAR DATO AMPLIACION STN POR PROYECTO
@app.get("/Datos_Ampliacion_STN/{Proyecto}/Proyecto", response_model = list[DA_AMP_schema.Dato_AMP_STN_Proyecto], tags = ["Datos Ampliaciones del STN"])
def leer_datos_ampliaciones_STN_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar un dato de Ampliación STN de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_AMP_crud.get_dato_ampliacion_STN_proyecto(db, Proyecto):
        return DA_AMP_crud.get_dato_ampliacion_STN_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR TODAS LOS DATOS AMPLIACIONES STN POR FECHAS Y PROYECTOS
@app.get("/Datos_Ampliacion_STN/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_AMP_schema.Dato_AMP_STN_Proyecto_Fechas, tags = ["Datos Ampliaciones del STN"])
def leer_dato_ampliacion_STN_por_proyectos_y_fechas(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios datos de Ampliación STN de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_AMP_crud.get_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        return DA_AMP_crud.get_dato_ampliacion_STN_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")


# MOSTRAR TODAS LOS DATOS AMPLIACION STN POR FECHAS 
@app.get("/Datos_Ampliacion_STN/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = list[DA_AMP_schema.Dato_AMP_STN_Fechas], tags = ["Datos Ampliaciones del STN"])
def leer_dato_ampliacion_STN_por_fechas(Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios datos de Ampliación STN de acuerdo a:
        
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    if DA_AMP_crud.get_dato_ampliacion_STN_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        return DA_AMP_crud.get_dato_ampliacion_STN_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")






#* FUNCIONES DE DATO EXPANSION STR
# CREAR DATO EXPANSION STR ASOCIADO A UN PROYECTO
@app.post("/Dato_Expansion_OR_STR/{Proyecto}/Proyecto/", response_model = DA_EXP_schema.Dato_Expansion_OR_STR, tags = ["Datos Expansiones OR del STR"])
def crear_dato_expansion_OR_STR_por_proyecto(Proyecto: str, Dato_EXP_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Create, db: Session = Depends(get_db)):
    """
        Crear Dato para Expansión OR STR
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    **Datos Solicitados** 

    - **Periodo**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. Requerido
    - **Tasa_Retorno**: . Requerido
    - **BRAEN**: . Requerido
    - **RC**: . Requerido
    - **BRT**: . Requerido
    - **NE**: . Requerido
    - **BRA_IAOM**: . Requerido

    **Importante**: No se permite que exista mas de un Periodo igual para un Proyecto.

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    DA_EXP_validation.validar_datos_Exp_STR_crear(db, Dato_EXP_STR, Proyecto)
    return DA_EXP_crud.create_dato_expansion_OR_STR_en_proyecto(db, Dato_EXP_STR, Proyecto)


# ACTUALIZAR DATO EXPANSION STR
@app.put("/Dato_Expansion_OR_STR/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_EXP_schema.Dato_Expansion_OR_STR, tags = ["Datos Expansiones OR del STR"])
def actualizar_dato_expansion_OR_STR(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, Dato_EXP_STR: DA_EXP_schema.Dato_Expansion_OR_STR_Update, db: Session = Depends(get_db)):
    """
        Actualizar Dato para Expansión OR STR de acuerdo a:

    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
    - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd

    **Datos cambiables:**

    - **Periodo**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd.
    - **Tasa_Retorno**: 
    - **BRAEN**: 
    - **RC**: 
    - **BRT**: 
    - **NE**: 
    - **BRA_IAOM**: 

    """
    if not DA_EXP_crud.get_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")

    Dato_Exp_id = DA_EXP_crud.get_ID_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Exp_id = Dato_Exp_id.get("ID")
    DA_EXP_validation.verificar_dato_Exp_STR(db, Dato_Exp_id)
    DA_EXP_validation.validar_datos_Exp_STR_actualizar(db, Dato_EXP_STR, Dato_Exp_id)
    return DA_EXP_crud.update_dato_expansion_OR_STR(db, Dato_EXP_STR, Dato_Exp_id)


# ELIMINAR DATO EXPANSION STR
@app.delete("/Dato_Expansion_OR_STR/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", tags = ["Datos Expansiones OR del STR"])
def eliminar_dato_expansion_OR_STR(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Eliminar Dato para Expansión OR STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    if not DA_EXP_crud.get_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")

    Dato_Exp_id = DA_EXP_crud.get_ID_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    Dato_Exp_id = Dato_Exp_id.get("ID")
    DA_EXP_validation.verificar_dato_Exp_STR(db, Dato_Exp_id)
    return DA_EXP_crud.delete_dato_expansion_OR_STR(db, Dato_Exp_id)


# MOSTRAR TODOS LOS DATOS EXP STR
@app.get("/Datos_Expansiones_OR_STR/", response_model = list[DA_EXP_schema.Dato_Expansion_OR_STR], tags = ["Datos Expansiones OR del STR"])
def leer_datos_expansion_OR_STR(db: Session = Depends(get_db)):
    """
            Buscar todos los datos de Expansión OR STR
        No se requiere introducir datos

    """
    return DA_EXP_crud.get_dato_expansiones_OR_STR(db)


# MOSTRAR DATO EXPANSION STR
@app.get("/Dato_Expansion_OR_STR/{Proyecto}/Proyecto/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = DA_EXP_schema.Dato_Expansion_OR_STR, tags = ["Datos Expansiones OR del STR"])
def leer_dato_expansion_OR_STR(Proyecto: str, Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar un dato de Expansión OR STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_EXP_crud.get_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        DA_EXP_crud.get_dato_expansion_OR_STR_proyecto_periodo(db, Proyecto, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")


# MOSTRAR DATO EXPANSION STR POR PROYECTO
@app.get("/Datos_Expansion_OR_STR/{Proyecto}/Proyecto", response_model = list[DA_EXP_schema.Dato_EXP_STR_Proyecto], tags = ["Datos Expansiones OR del STR"])
def leer_datos_expansion_OR_STR_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar un dato de Expansión OR STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if DA_EXP_crud.get_dato_expansion_OR_STR_proyecto(db, Proyecto):
        return DA_EXP_crud.get_dato_expansion_OR_STR_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR TODAS LOS DATOS EXPANSIONES OR STR POR FECHAS 
@app.get("/Datos_Expansion_OR_STR/{Fecha_Inicio_Vigen}/Fecha_Incio_Vigen/{Fecha_Fin_Vigen}/Fecha_Fin_Vigen", response_model = list[DA_EXP_schema.Dato_EXP_STR_Fechas], tags = ["Datos Expansiones OR del STR"])
def leer_dato_expansion_OR_STR_por_fechas(Fecha_Inicio_Vigen: date, Fecha_Fin_Vigen: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios datos de Expansión OR STR de acuerdo a:
        
        - **Fecha_Inicio_Vigen**: Fecha de Inicio de Vigencia con formato YYYY-mm-dd
        - **Fecha_Fin_Vigen**: Fecha de Fin de Vigencia con formato YYYY-mm-dd
    """
    if DA_EXP_crud.get_dato_expansion_OR_STR_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen):
        return DA_EXP_crud.get_dato_expansion_OR_STR_periodo(db, Fecha_Inicio_Vigen, Fecha_Fin_Vigen)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fechas {Fecha_Inicio_Vigen} - {Fecha_Fin_Vigen}")






#* FUNCIONES DE SEGUIMIENTO FPO
# CREAR SEGUIMIENTO FPO ASOCIADO A UN PROYECTO
@app.post("/Seguimiento_FPO/{Proyecto}/Proyecto/", response_model = SE_FPO_schema.Seguimiento_FPO, tags = ["Seguimientos del FPO"])
def crear_seguimiento_FPO_por_proyecto(Proyecto: str, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Create, db: Session = Depends(get_db)):
    """
        Crear Seguimiento FPO Manual
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    **Datos Solicitados** 

    - **Fecha_Oficial**: formato YYYY-mm-dd. Opcional
    - **Fecha_Real**: formato YYYY-mm-dd. Opcional
    - **Fecha_Inicio_Vigen**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. Requerido
    - **Tipo_Doc**: Tipo de Documento por el que se informo las fechas que puede ser. Requerido
        - *CC*: Carta de Compromiso
        - *MME*: Ministerio de Minas y Energia
        - *CREG*: Resolución CREG
        - *UPME*: Convocatoria UPME 
    - **Descrip_Doc**: Descripción del Documento. Opcional
    - **Documento**: Ruta de almacenamiento del Documento. Opcional

    **Importante**
    
    - **Fecha_Fin_Vigen** se actualizara automaticamente cada vez que se cree un registro nuevo. 
    Si existe un ultimo registro del mismo proyecto la **Fecha_Fin_Vigen** se actualizara con la 
    **Fecha_Inicio_Vigen** del nuevo registro y su **Fecha_Fin_Vigen** estara null 

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    SE_FPO_validation.validar_seguimientos_FPO_crear(db, seguimiento_FPO, Proyecto)
    return SE_FPO_crud.create_seguimiento_FPO_en_proyecto(db, seguimiento_FPO, Proyecto)


# CREAR SEGUIMIENTO FPO ASOCIADO A UN PROYECTO
@app.post("/Seguimiento_FPO/API_MDC", response_model = SE_FPO_schema.Seguimiento_FPO, tags = ["Seguimientos del FPO"])
def verificar_seguiemiento_FPO_por_API_MDC(db: Session = Depends(get_db)):
    """
        Crear Seguimiento FPO por API del MDC
    Busca los proyectos y FPO almacenados en la Base de Datos y realiza una comparación para comprobar que las fechas sean las actuales.
    
    **Importante**
        
    - Para **Fecha_Inicio_Vigen** se colocara la fecha del dia que se ejecute este proceso
    - Para **Fecha_Fin_Vigen** del ultimo registro para el mismo proyecto se le colocara Fecha_Inicio_Vigen mencionada anteriormente
    - Para **Tipo_Doc**, **Descrip_Doc** y **Documento** se enviara vacio ya que desde la API del MDC no se obtiene esa información
    """
    return SE_FPO_crud.create_seguimiento_FPO_por_API(db)


# ACTUALIZAR SEGUIMIENTO FPO
@app.put("/Seguimiento_FPO/{Seg_FPO_id}", response_model = SE_FPO_schema.Seguimiento_FPO, tags = ["Seguimientos del FPO"])
def actualizar_seguimiento_FPO(Seg_FPO_id: int, seguimiento_FPO: SE_FPO_schema.Seguimiento_FPO_Update, db: Session = Depends(get_db)):
    """
        Actualizar Seguimiento FPO de acuerdo a:

    - **Seg_FPO_id**: Posición del dato en la base de datos

    **Datos cambiables:**

    - **Fecha_Oficial**: formato YYYY-mm-dd.
    - **Fecha_Real**: formato YYYY-mm-dd.
    - **Fecha_Inicio_Vigen**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. 
    - **Tipo_Doc**: Tipo de Documento por el que se informo las fechas que puede ser.
        - *CC*: Carta de Compromiso
        - *MME*: Ministerio de Minas y Energia
        - *CREG*: Resolución CREG
        - *UPME*: Convocatoria UPME 
    - **Descrip_Doc**: Descripción del Documento. 
    - **Documento**: Ruta de almacenamiento del Documento.

    """
    SE_FPO_validation.verificar_seguimiento_FPO(db, Seg_FPO_id)
    SE_FPO_validation.validar_seguimientos_FPO_actualizar(seguimiento_FPO)
    return SE_FPO_crud.update_seguimiento_FPO(db, seguimiento_FPO, Seg_FPO_id)


# ELIMINAR SEGUIMIENTO FPO
@app.delete("/Seguimiento_FPO/{Seg_FPO_id}", tags = ["Seguimientos del FPO"])
def eliminar_seguimiento_FPO(Seg_FPO_id: int, db: Session = Depends(get_db)):
    """
            Eliminar Seguimiento FPO de acuerdo a:
        
        - **Seg_FPO_id**: Posición del dato en la base de datos
    """
    SE_FPO_validation.verificar_seguimiento_FPO(db, Seg_FPO_id)
    return SE_FPO_crud.delete_seguimiento_FPO(db, Seg_FPO_id)


# MOSTRAR TODOS LOS SEGUIMIENTOS FPO
@app.get("/Seguimientos_FPO/", response_model = list[SE_FPO_schema.Seguimiento_FPO], tags = ["Seguimientos del FPO"])
def leer_seguimientos_FPO(db: Session = Depends(get_db)):
    """
            Buscar todos los Seguimientos FPO
        No se requiere introducir datos

    """
    return SE_FPO_crud.get_seguimientos_FPO(db)


# MOSTRAR SEGUIMIENTO FPO
@app.get("/Seguimiento_FPO/{Seg_FPO_id}", response_model = SE_FPO_schema.Seguimiento_FPO, tags = ["Seguimientos del FPO"])
def leer_seguimiento_FPO(Seg_FPO_id: int, db: Session = Depends(get_db)):
    """
            Buscar un Seguimiento FPO de acuerdo a:
        
        - **Seg_FPO_id**: Posición del dato en la base de datos

    """
    SE_FPO_validation.verificar_seguimiento_FPO(db, Seg_FPO_id)
    return SE_FPO_crud.get_seguimiento_FPO(db, Seg_FPO_id)


# MOSTRAR SEGUIMIENTO FPO POR PROYECTO
@app.get("/Seguimientos_FPO/{Proyecto}/Proyecto/", response_model = list[SE_FPO_schema.Seguimiento_FPO_Proyecto], tags = ["Seguimientos del FPO"])
def leer_seguimientos_FPO_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar un Seguimiento FPO de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)

    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if SE_FPO_crud.get_seguimiento_FPO_proyecto(db, Proyecto):
        return SE_FPO_crud.get_seguimiento_FPO_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR SEGUIMIENTO FPO POR FECHA OFICIAL
@app.get("/Seguimientos_FPO/{Fecha_Oficial}/Fecha_Oficial/", response_model = list[SE_FPO_schema.Seguimiento_FPO_Oficial], tags = ["Seguimientos del FPO"])
def leer_seguimientos_FPO_por_fecha_oficial(Fecha_Oficial: date, db: Session = Depends(get_db)):
    """
            Buscar un Seguimiento FPO de acuerdo a:
        
        - **Fecha_Oficial**: FPO Oficial con formato YYYY-mm-dd

    """
    if SE_FPO_crud.get_seguimiento_FPO_oficial(db, Fecha_Oficial):
        return SE_FPO_crud.get_seguimiento_FPO_oficial(db, Fecha_Oficial)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fecha_Oficial {Fecha_Oficial}")


# MOSTRAR SEGUIMIENTO FPO POR FECHA REAL
@app.get("/Seguimientos_FPO/{Fecha_Real}/Fecha_Real/", response_model = list[SE_FPO_schema.Seguimiento_FPO_Real], tags = ["Seguimientos del FPO"])
def leer_seguimientos_FPO_por_fecha_real(Fecha_Real: date, db: Session = Depends(get_db)):
    """
            Buscar un Seguimiento FPO de acuerdo a:
        
        - **Fecha_Real**: FPO Real con formato YYYY-mm-dd

    """
    if SE_FPO_crud.get_seguimiento_FPO_real(db, Fecha_Real):
        return SE_FPO_crud.get_seguimiento_FPO_real(db, Fecha_Real)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fecha_Real {Fecha_Real}")


# MOSTRAR SEGUIMIENTO FPO POR FECHA OFICIAL Y FECHA REAL
@app.get("/Seguimientos_FPO/{Fecha_Oficial}/Fecha_Oficial/{Fecha_Real}/Fecha_Real/", response_model = list[SE_FPO_schema.Seguimiento_FPO_Oficial_Real], tags = ["Seguimientos del FPO"])
def leer_seguimientos_FPO_por_fecha_oficial_y_fecha_real(Fecha_Oficial: date, Fecha_Real: date, db: Session = Depends(get_db)):
    """
            Buscar un Seguimiento FPO de acuerdo a:
        
        - **Fecha_Oficial**: FPO Oficial con formato YYYY-mm-dd
        - **Fecha_Real**: FPO Real con formato YYYY-mm-dd

    """
    if SE_FPO_crud.get_seguimiento_FPO_oficial_real(db, Fecha_Oficial, Fecha_Real):
        return SE_FPO_crud.get_seguimiento_FPO_oficial_real(db, Fecha_Oficial, Fecha_Real)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con Fecha_Oficial {Fecha_Oficial} y Fecha_Real {Fecha_Real}")







#* FUNCIONES DE LIQUIDACION PPA
# CREAR LIQUIDACION PPA
@app.post("/Liquidacion_PPA/", response_model = LIQ_schema.Liquidacion_PPA, tags = ["Liquidaciones del PPA"])
def crear_liquidacion_PPA_por_proyecto(Proceso: str, liquidacion: LIQ_schema.Liquidacion_PPA_Create, db: Session = Depends(get_db)):
    """
        Crear Liquidaciones PPA 
    
    - **Proceso**: Proceso que quiere liquidar, tiene que ser STN o STR
    
    **Datos Solicitados** 

    - **Periodo**: Fecha que se quiere liquidar con formato YYYY-mm-dd. Requerido
    - **Version**: Versionamiento de la liquidación que puede ser. Requerido
        - **Est**: Estimados
        - **Liq**: Liquidaciones
        - **Aju1**: Ajustes 1
        - **Aju2**: Ajustes 2

    **Importante**

    Busca los proyectos y FPO almacenados en la Base de Datos, comprueba si esta atrasado el proyecto y lo esta,
    crea un registro de liquidacion para este.
    """
    LIQ_validation.validar_liquidaciones_crear(liquidacion, Proceso)
    return LIQ_crud.create_liquidacion_PPA(db, liquidacion, Proceso)


# ACTUALIZAR LIQUIDACION PPA
@app.put("/Liquidacion_PPA/{Proyecto}/Proyecto/{Periodo}/Periodo/{Version}/Version", response_model = LIQ_schema.Liquidacion_PPA, tags = ["Liquidaciones del PPA"])
def actualizar_liquidacion_PPA(Proyecto: str, Periodo: date, Version: str, liquidacion: LIQ_schema.Liquidacion_PPA_Update, db: Session = Depends(get_db)):
    """
        Actualizar Liquidacion PPA de acuerdo a:

    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Periodo**: Fecha de la validez con formato YYYY-mm-dd
    - **Version**: Est, Liq, Aju1 o Aju2

    **Datos cambiables:**

    - **Fecha_Oficial**: formato YYYY-mm-dd.
    - **Fecha_Real**: formato YYYY-mm-dd.
    - **Fecha_Inicio_Vigen**: Fecha donde empieza a ser valido los datos con formato YYYY-mm-dd. 
    - **Tipo_Doc**: Tipo de Documento por el que se informo las fechas que puede ser.
        - *CC*: Carta de Compromiso
        - *MME*: Ministerio de Minas y Energia
        - *CREG*: Resolución CREG
        - *UPME*: Convocatoria UPME 
    - **Descrip_Doc**: Descripción del Documento. 
    - **Documento**: Ruta de almacenamiento del Documento.

    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Periodo, Version)
    LIQ_validation.validar_liquidaciones_actualizar(liquidacion)
    return LIQ_crud.update_liquidacion_PPA(db, liquidacion, Proyecto, Periodo, Version)


# ELIMINAR LIQUIDACION PPA
@app.delete("/Liquidacion_PPA/{Proyecto}/Proyecto/{Periodo}/Periodo/{Version}/Version", tags = ["Liquidaciones del PPA"])
def eliminar_liquidacion_PPA(Proyecto: str, Periodo: date, Version: str, db: Session = Depends(get_db)):
    """
            Eliminar Liquidacion PPA de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Periodo**: Fecha de la validez con formato YYYY-mm-dd
        - **Version**: Est, Liq, Aju1 o Aju2
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Periodo, Version)
    return LIQ_crud.delete_liquidacion_PPA(db, Proyecto, Periodo, Version)


# MOSTRAR TODAS LAS LIQUIDACIONES PPA
@app.get("/Liquidaciones_PPA/", response_model = list[LIQ_schema.Liquidacion_PPA], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes(db: Session = Depends(get_db)):
    """
            Buscar todos las Liquidaciones PPA
        No se requiere introducir datos

    """
    return LIQ_crud.get_liquidaciones_PPA(db)


# MOSTRAR LIQUIDACION PPA
@app.get("/Liquidacion_PPA/{Proyecto}/Proyecto/{Periodo}/Periodo/{Version}/Version", response_model = LIQ_schema.Liquidacion_PPA, tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPA(Proyecto: str, Periodo: date, Version: str, db: Session = Depends(get_db)):
    """
            Buscar una Liquidacion PPA de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Periodo**: Fecha de la validez con formato YYYY-mm-dd
        - **Version**: Est, Liq, Aju1 o Aju2

    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Periodo, Version)
    return LIQ_crud.get_liquidacion_PPA(db, Proyecto, Periodo, Version)


# MOSTRAR TODAS LAS LIQUIDACION PPA POR AGENTE
@app.get("/Liquidaciones_PPA/{Agente}/Agente", response_model = list[LIQ_schema.Liquidacion_PPA_Agente], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Agente**: ASIC del Agente
    """
    AGE_validation.verificar_agente(db, Agente)
    if LIQ_crud.get_liquidacion_PPA_agente(db, Agente):
        return LIQ_crud.get_liquidacion_PPA_agente(db, Agente)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR TODAS LAS LIQUIDACION PPA POR PROYECTO
@app.get("/Liquidaciones_PPA/{Proyecto}/Proyecto", response_model = list[LIQ_schema.Liquidacion_PPA_Proyecto], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if LIQ_crud.get_liquidacion_PPA_proyecto(db, Proyecto):
        return LIQ_crud.get_liquidacion_PPA_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR TODAS LAS LIQUIDACION PPA POR PERIODO
@app.get("/Liquidaciones_PPA/{Periodo}/Periodo", response_model = list[LIQ_schema.Liquidacion_PPA_Periodo], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_periodo(Periodo: date, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Periodo**: Fecha de la validez con formato YYYY-mm-dd
    """
    if LIQ_crud.get_liquidacion_PPA_periodo(db, Periodo):
        return LIQ_crud.get_liquidacion_PPA_periodo(db, Periodo)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con el Periodo {Periodo}")


# MOSTRAR TODAS LAS LIQUIDACION PPA POR PROYECTO Y PERIODO
@app.get("/Liquidaciones_PPA/{Proyecto}/Proyecto/{Periodo}/Periodo", response_model = list[LIQ_schema.Liquidacion_PPA_Proyecto_Periodo], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_proyecto_y_periodo(Proyecto: str, Periodo: date, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Periodo**: Fecha de la validez con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if LIQ_crud.get_liquidacion_PPA_proyecto_periodo(db, Proyecto, Periodo):
        return LIQ_crud.get_liquidacion_PPA_proyecto_periodo(db, Proyecto, Periodo)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} con el Periodo {Periodo}")


# MOSTRAR TODAS LAS LIQUIDACION PPA POR PERIODO RANGO
@app.get("/Liquidaciones_PPA/Rango/{Fecha_Desde}/{Fecha_Hasta}", response_model = list[LIQ_schema.Liquidacion_PPA_Periodo], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_rango_de_fechas(Fecha_Desde: date, Fecha_Hasta: date, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Fecha_Desde**: Fecha Desde la que se quiere buscar la liquidacion con formato YYYY-mm-dd
        - **Fecha_Hasta**: Fecha Hasta la que se quiere buscar la liquidacion con formato YYYY-mm-dd
    """
    if LIQ_crud.get_liquidacion_PPA_periodo_rango(db, Fecha_Desde, Fecha_Hasta):
        return LIQ_crud.get_liquidacion_PPA_periodo_rango(db, Fecha_Desde, Fecha_Hasta)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación entre {Fecha_Desde} y {Fecha_Hasta}")


# MOSTRAR TODAS LAS LIQUIDACION PPA POR CATEGORIA
@app.get("/Liquidaciones_PPA/{Categoria}/Categoria", response_model = list[LIQ_schema.Liquidacion_PPA_Categoria], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_categoria(Categoria: str, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Categoria**: STN o STR
    """
    if LIQ_crud.get_liquidacion_PPA_categoria(db, Categoria):
        return LIQ_crud.get_liquidacion_PPA_categoria(db, Categoria)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación con la Categoria {Categoria}")


# MOSTRAR TODAS LAS LIQUIDACION PPAES POR SUBCATEGORIA
@app.get("/Liquidaciones_PPA/{Subcategoria}/Subcategoria", response_model = list[LIQ_schema.Liquidacion_PPA_Subcategoria], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_subcategoria(Subcategoria: str, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Subcategoria**: Convocatoria, Ampliación o Expansión OR
    """
    if LIQ_crud.get_liquidacion_PPA_subcategoria(db, Subcategoria):
        return LIQ_crud.get_liquidacion_PPA_subcategoria(db, Subcategoria)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación con la Subcategoria {Subcategoria}")


# MOSTRAR TODAS LAS LIQUIDACION PPAES POR CATEGORIA Y SUBCATEGORIA
@app.get("/Liquidaciones_PPA/{Categoria}/Categoria/{Subcategoria}/Subcategoria", response_model = list[LIQ_schema.Liquidacion_PPA_Categoria_Subcategoria], tags = ["Liquidaciones del PPA"])
def leer_liquidacion_PPAes_por_categoria_y_subcategoria(Categoria: str, Subcategoria: str, db: Session = Depends(get_db)):
    """
            Buscar una o varias Liquidaciones PPA de acuerdo a:
        
        - **Categoria**: STN o STR
        - **Subcategoria**: Convocatoria, Ampliación o Expansión OR
    """
    if LIQ_crud.get_liquidacion_PPA_categoria_subcategoria(db, Categoria, Subcategoria):
        return LIQ_crud.get_liquidacion_PPA_categoria_subcategoria(db, Categoria, Subcategoria)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación con la Categoria {Categoria} y Subcategoria {Subcategoria}")






#* FUNCIONES DE CONVOCATORIA STN
# CREAR CONVOCATORIA STN A UNA LIQUIDACION PPA
@app.post("/Convocatoria_STN/{Proyecto}/Proyecto/{Liquidacion}/Liquidacion_PPA/{Version}/Version", response_model = CO_STN_schema.Convocatoria_STN, tags = ["Convocatorias del STN"])
def crear_convocatoria_STN_por_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, Version: str, Conv_STN: CO_STN_schema.Convocatoria_STN_Create, db: Session = Depends(get_db)):
    """
        Crear Calculo de Convocatoria STN
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    - **Version**: Est, Liq, Aju1 o Aju2

    
    **Datos Solicitados** 

    - **Capacidad_O**: Capacidad en Operación. Opcional
    - **Capacidad_T**: Capacidad Total. Opcional

    **Importante**

    Las Capacidades se utilizan cuando es un Agente con Rol Generador, de lo contrario deben ir en cero.
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Liquidacion_PPA, Version)
    LIQ_validation.verificar_calculo_unico(db, Proyecto, Liquidacion_PPA, Version)
    CO_STN_validation.validar_convocatoria_STN_crear(db, Conv_STN, Proyecto) 
    return CO_STN_crud.create_convocatoria_STN_en_liq(db, Conv_STN, Proyecto, Liquidacion_PPA, Version)


# ACTUALIZAR CONVOCATORIA STN
@app.put("/Convocatoria_STN/{Conv_STN_id}", response_model = CO_STN_schema.Convocatoria_STN, tags = ["Convocatorias del STN"])
def actualizar_convocatoria_STN(Conv_STN_id: int, Conv_STN: CO_STN_schema.Convocatoria_STN_Update, db: Session = Depends(get_db)):
    """
        Actualizar Calculo de Convocatoria STN de acuerdo a:

    - **Conv_STN_id**: Posición del dato en la base de datos

    **Datos cambiables:**

    - **Capacidad_O**: Capacidad en Operación. Opcional
    - **Capacidad_T**: Capacidad Total. Opcional

    """
    CO_STN_validation.verificar_convocatoria_STN(db, Conv_STN_id)
    CO_STN_validation.validar_convocatoria_STN_actualizar(db, Conv_STN, Conv_STN_id) 
    return CO_STN_crud.update_convocatoria_STN(db, Conv_STN, Conv_STN_id)


# ELIMINAR CONVOCATORIA STN
@app.delete("/Convocatoria_STN/{Conv_STN_id}", tags = ["Convocatorias del STN"])
def eliminar_convocatoria_STN(Conv_STN_id: int, db: Session = Depends(get_db)):
    """
            Eliminar Calculo de Convocatoria STN de acuerdo a:
        
        - **Conv_STN_id**: Posición del dato en la base de datos
    """
    CO_STN_validation.verificar_convocatoria_STN(db, Conv_STN_id)
    return CO_STN_crud.delete_convocatoria_STN(db, Conv_STN_id)


# MOSTRAR TODAS LAS CONVOCATORIAS STN 
@app.get("/Convocatorias_STN/", response_model = list[CO_STN_schema.Convocatoria_STN], tags = ["Convocatorias del STN"])
def leer_convocatorias_STN(db: Session = Depends(get_db)):
    """
            Buscar todos los Calculos de Convocatorias STN
        No se requiere introducir datos

    """
    return CO_STN_crud.get_convocatorias_STN(db)


# MOSTRAR CONVOCATORIA STN
@app.get("/Convocatoria_STN/{Conv_STN_id}", response_model = CO_STN_schema.Convocatoria_STN, tags = ["Convocatorias del STN"])
def leer_convocatoria_STN(Conv_STN_id: int, db: Session = Depends(get_db)):
    """
            Buscar uno Calculo de Convocatoria STN de acuerdo a:
        
        - **Conv_STN_id**: Posición del dato en la base de datos
    """
    CO_STN_validation.verificar_convocatoria_STN(db, Conv_STN_id)
    return CO_STN_crud.get_convocatoria_STN(db, Conv_STN_id)


# MOSTRAR CONVOCATORIA STN POR AGENTE
@app.get("/Convocatorias_STN/{Agente}/Agente", response_model = list[CO_STN_schema.Convocatoria_STN_Agente], tags = ["Convocatorias del STN"])
def leer_convocatoria_STN_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar una o varios Calculos de Convocatorias STN de acuerdo a:
        
        - **Agente**: ASIC del Agente
    """
    AGE_validation.verificar_agente(db, Agente)
    if CO_STN_crud.get_convocatoria_STN_agente(db, Agente):
        return CO_STN_crud.get_convocatoria_STN_agente(db, Agente)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR CONVOCATORIA STN POR PROYECTO
@app.get("/Convocatorias_STN/{Proyecto}/Proyecto", response_model = list[CO_STN_schema.Convocatoria_STN_Proyecto], tags = ["Convocatorias del STN"])
def leer_convocatoria_STN_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STN de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if CO_STN_crud.get_convocatoria_STN_proyecto(db, Proyecto):
        return CO_STN_crud.get_convocatoria_STN_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR CONVOCATORIA STN POR LIQUIDACION PPA
@app.get("/Convocatorias_STN/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[CO_STN_schema.Convocatoria_STN_Liquidacion], tags = ["Convocatorias del STN"])
def leer_convocatoria_STN_por_liquidacion_PPA(Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STN de acuerdo a:
        
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    if CO_STN_crud.get_convocatoria_STN_liquidacion_PPA(db, Liquidacion_PPA):
        return CO_STN_crud.get_convocatoria_STN_liquidacion_PPA(db, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS CONVOCATORIAS STN POR PROYECTO Y LIQUIDACION PPA
@app.get("/Convocatorias_STN/{Proyecto}/Proyecto/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[CO_STN_schema.Convocatoria_STN_Proyecto_Liquidacion], tags = ["Convocatorias del STN"])
def leer_convocatoria_STN_por_proyecto_y_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STN de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if CO_STN_crud.get_convocatoria_STN_proyecto_liquidacion_PPA(db, Proyecto, Liquidacion_PPA):
        return CO_STN_crud.get_convocatoria_STN_proyecto_liquidacion_PPA(db, Proyecto, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS CONVOCATORIAS STN POR LIQUIDACION PPA PPA RANGO
@app.get("/Convocatorias_STN/Rango/{Fecha_Desde}/{Fecha_Hasta}", response_model = list[CO_STN_schema.Convocatoria_STN_Liquidacion], tags = ["Convocatorias del STN"])
def leer_convocatoria_STN_por_rango_de_liquidaciones_PPA(Fecha_Desde: date, Fecha_Hasta: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STN de acuerdo a:
        
        - **Fecha_Desde**: Fecha Desde la que se quiere buscar la liquidacion con formato YYYY-mm-dd
        - **Fecha_Hasta**: Fecha Hasta la que se quiere buscar la liquidacion con formato YYYY-mm-dd
    """
    if CO_STN_crud.get_convocatoria_STN_liquidacion_PPA_rango(db, Fecha_Desde, Fecha_Hasta):
        return CO_STN_crud.get_convocatoria_STN_liquidacion_PPA_rango(db, Fecha_Desde, Fecha_Hasta)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación entre {Fecha_Desde} y {Fecha_Hasta}")






#* FUNCIONES DE CONVOCATORIA STR
# CREAR CONVOCATORIA STR A UNA LIQUIDACION PPA
@app.post("/Convocatoria_STR/{Proyecto}/Proyecto/{Liquidacion}/Liquidacion_PPA/{Version}/Version", response_model = CO_STR_schema.Convocatoria_STR, tags = ["Convocatorias del STR"])
def crear_convocatoria_STR_por_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, Version: str, db: Session = Depends(get_db)):
    """
        Crear Calculo de Convocatoria STR
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    - **Version**: Est, Liq, Aju1 o Aju2

    **Importante**

    Esta función se utiliza solo cuando por alguna razón, sea quee faltaron datos o falta de actualización la liquidación quedo en cero.
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Liquidacion_PPA, Version)
    LIQ_validation.verificar_calculo_unico(db, Proyecto, Liquidacion_PPA, Version)
    return CO_STR_crud.create_convocatoria_STR_individual(db, Proyecto, Liquidacion_PPA, Version)


# ACTUALIZAR CONVOCATORIA STR
@app.put("/Convocatoria_STR/{Conv_STR_id}", response_model = CO_STR_schema.Convocatoria_STR, tags = ["Convocatorias del STR"])
def actualizar_convocatoria_STR(Conv_STR_id: int, Conv_STR: CO_STR_schema.Convocatoria_STR_Create, db: Session = Depends(get_db)):
    """
        Actualizar Calculo de Convocatoria STR de acuerdo a:

    - **Conv_STR_id**: Posición del dato en la base de datos

    """
    CO_STR_validation.verificar_convocatoria_STR(db, Conv_STR_id)
    return CO_STR_crud.update_convocatoria_STR(db, Conv_STR, Conv_STR_id)


# ELIMINAR CONVOCATORIA STR
@app.delete("/Convocatoria_STR/{Conv_STR_id}", tags = ["Convocatorias del STR"])
def eliminar_convocatoria_STR(Conv_STR_id: int, db: Session = Depends(get_db)):
    """
            Eliminar Calculo de Convocatoria STR de acuerdo a:
        
        - **Conv_STR_id**: Posición del dato en la base de datos
    """
    CO_STR_validation.verificar_convocatoria_STR(db, Conv_STR_id)
    return CO_STR_crud.delete_convocatoria_STR(db, Conv_STR_id)


# MOSTRAR TODAS LAS CONVOCATORIAS STR 
@app.get("/Convocatorias_STR/", response_model = list[CO_STR_schema.Convocatoria_STR], tags = ["Convocatorias del STR"])
def leer_convocatorias_STR(db: Session = Depends(get_db)):
    """
            Buscar todos los Calculos de Convocatorias STR
        No se requiere introducir datos

    """
    return CO_STR_crud.get_convocatorias_STR(db)


# MOSTRAR CONVOCATORIA STR
@app.get("/Convocatoria_STR/{Conv_STR_id}", response_model = CO_STR_schema.Convocatoria_STR, tags = ["Convocatorias del STR"])
def leer_convocatoria_STR(Conv_STR_id: int, db: Session = Depends(get_db)):
    """
            Buscar uno Calculo de Convocatoria STR de acuerdo a:
        
        - **Conv_STR_id**: Posición del dato en la base de datos
    """
    CO_STR_validation.verificar_convocatoria_STR(db, Conv_STR_id)
    return CO_STR_crud.get_convocatoria_STR(db, Conv_STR_id)


# MOSTRAR CONVOCATORIA STR POR AGENTE
@app.get("/Convocatorias_STR/{Agente}/Agente", response_model = list[CO_STR_schema.Convocatoria_STR_Agente], tags = ["Convocatorias del STR"])
def leer_convocatoria_STR_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar una o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Agente**: ASIC del Agente
    """
    AGE_validation.verificar_agente(db, Agente)
    if CO_STR_crud.get_convocatoria_STR_agente(db, Agente):
        return CO_STR_crud.get_convocatoria_STR_agente(db, Agente)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR CONVOCATORIA STR POR PROYECTO
@app.get("/Convocatorias_STR/{Proyecto}/Proyecto", response_model = list[CO_STR_schema.Convocatoria_STR_Proyecto], tags = ["Convocatorias del STR"])
def leer_convocatoria_STR_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if CO_STR_crud.get_convocatoria_STR_proyecto(db, Proyecto):
        return CO_STR_crud.get_convocatoria_STR_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR CONVOCATORIA STR POR LIQUIDACION PPA
@app.get("/Convocatorias_STR/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[CO_STR_schema.Convocatoria_STR_Liquidacion], tags = ["Convocatorias del STR"])
def leer_convocatoria_STR_por_liquidacion_PPA(Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if CO_STR_crud.get_convocatoria_STR_liquidacion(db, Liquidacion_PPA):
        return CO_STR_crud.get_convocatoria_STR_liquidacion(db, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS CONVOCATORIAS STR POR PROYECTO Y LIQUIDACION PPA
@app.get("/Convocatorias_STR/{Proyecto}/Proyecto/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[CO_STR_schema.Convocatoria_STR_Proyecto_Liquidacion], tags = ["Convocatorias del STR"])
def leer_convocatoria_STR_por_proyecto_y_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if CO_STR_crud.get_convocatoria_STR_proyecto_liquidacion(db, Proyecto, Liquidacion_PPA):
        return CO_STR_crud.get_convocatoria_STR_proyecto_liquidacion(db, Proyecto, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS CONVOCATORIAS STR POR LIQUIDACION PPA PPA RANGO
@app.get("/Convocatorias_STR/Rango/{Fecha_Desde}/{Fecha_Hasta}", response_model = list[CO_STR_schema.Convocatoria_STR_Liquidacion], tags = ["Convocatorias del STR"])
def leer_convocatoria_STR_por_rango_de_liquidaciones_PPA(Fecha_Desde: date, Fecha_Hasta: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Fecha_Desde**: Fecha Desde la que se quiere buscar la liquidacion con formato YYYY-mm-dd
        - **Fecha_Hasta**: Fecha Hasta la que se quiere buscar la liquidacion con formato YYYY-mm-dd
    """
    if CO_STR_crud.get_convocatoria_STR_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta):
        return CO_STR_crud.get_convocatoria_STR_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación entre {Fecha_Desde} y {Fecha_Hasta}")






#* FUNCIONES DE AMPLIACION STN
# CREAR AMPLIACION STN A UNA LIQUIDACION PPA
@app.post("/Ampliacion_STN/{Proyecto}/Proyecto/{Liquidacion}/Liquidacion_PPA/{Version}/Version", response_model = AMP_STN_schema.Ampliacion_STN, tags = ["Ampliaciones del STN"])
def crear_ampliacion_STN_por_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, Version: str, db: Session = Depends(get_db)):
    """
        Crear Calculo de Ampliación STN
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    - **Version**: Est, Liq, Aju1 o Aju2

    **Importante**

    Esta función se utiliza solo cuando por alguna razón, sea quee faltaron datos o falta de actualización la liquidación quedo en cero.
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Liquidacion_PPA, Version)
    LIQ_validation.verificar_calculo_unico(db, Proyecto, Liquidacion_PPA, Version)
    return AMP_STN_crud.create_ampliacion_STN_individual(db, Proyecto, Liquidacion_PPA, Version)


# ACTUALIZAR AMPLIACION STN
@app.put("/Ampliacion_STN/{Amp_id}", response_model = AMP_STN_schema.Ampliacion_STN, tags = ["Ampliaciones del STN"])
def actualizar_ampliacion_STN(Amp_id: int, db: Session = Depends(get_db)):
    """
        Actualizar Calculo de Ampliación STN de acuerdo a:

    - **Amp_id**: Posición del dato en la base de datos

    """
    AMP_STN_validation.verificar_ampliacion_STN(db, Amp_id)
    return AMP_STN_crud.update_ampliacion_STN(db, Amp_id)


# ELIMINAR AMPLIACION STN
@app.delete("/Ampliacion_STN/{Amp_id}", tags = ["Ampliaciones del STN"])
def eliminar_ampliacion_STN(Amp_id: int, db: Session = Depends(get_db)):
    """
            Eliminar Calculo de Ampliación STN de acuerdo a:
        
        - **Amp_id**: Posición del dato en la base de datos
    """
    AMP_STN_validation.verificar_ampliacion_STN(db, Amp_id)
    return AMP_STN_crud.delete_ampliacion_STN(db, Amp_id)


# MOSTRAR TODAS LAS AMPLIACIONES STN
@app.get("/Ampliaciones_STN/", response_model = list[AMP_STN_schema.Ampliacion_STN], tags = ["Ampliaciones del STN"])
def leer_ampliaciones_STN(db: Session = Depends(get_db)):
    """
            Buscar todos los Calculos de Ampliaciones STN
        No se requiere introducir datos

    """
    return AMP_STN_crud.get_ampliaciones_STN(db)


# MOSTRAR AMPLIACION STN
@app.get("/Ampliacion_STN/{Amp_id}", response_model = AMP_STN_schema.Ampliacion_STN, tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN(Amp_id: int, db: Session = Depends(get_db)):
    """
            Buscar uno Calculo de Ampliación STN de acuerdo a:
        
        - **Amp_id**: Posición del dato en la base de datos
    """
    AMP_STN_validation.verificar_ampliacion_STN(db, Amp_id)
    return AMP_STN_crud.get_ampliacion_STN(db, Amp_id)


# MOSTRAR AMPLIACION STN POR AGENTE
@app.get("/Ampliaciones_STN/{Agente}/Agente", response_model = list[AMP_STN_schema.Ampliacion_STN_Agente], tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar una o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Agente**: ASIC del Agente
    """
    AGE_validation.verificar_agente(db, Agente)
    if AMP_STN_crud.get_ampliacion_STN_agente(db, Agente):
        return AMP_STN_crud.get_ampliacion_STN_agente(db, Agente)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR AMPLIACION STN POR PROYECTO
@app.get("/Ampliaciones_STN/{Proyecto}/Proyecto", response_model = list[AMP_STN_schema.Ampliacion_STN_Proyecto], tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if AMP_STN_crud.get_ampliacion_STN_proyecto(db, Proyecto):
        return AMP_STN_crud.get_ampliacion_STN_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR AMPLIACION STN POR LIQUIDACION PPA
@app.get("/Ampliaciones_STN/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[AMP_STN_schema.Ampliacion_STN_Liquidacion], tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN_por_liquidacion_PPA(Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if AMP_STN_crud.get_ampliacion_STN_liquidacion_PPA(db, Liquidacion_PPA):
        return AMP_STN_crud.get_ampliacion_STN_liquidacion_PPA(db, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS AMPLIACION STN POR PROYECTO Y LIQUIDACION PPA
@app.get("/Ampliaciones_STN/{Proyecto}/Proyecto/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[AMP_STN_schema.Ampliacion_STN_Proyecto_Liquidacion], tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN_por_proyecto_y_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if AMP_STN_crud.get_ampliacion_STN_proyecto_liquidacion_PPA(db, Proyecto, Liquidacion_PPA):
        return AMP_STN_crud.get_ampliacion_STN_proyecto_liquidacion_PPA(db, Proyecto, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS AMPLIACION STN POR LIQUIDACION PPA PPA RANGO
@app.get("/Ampliaciones_STN/Rango/{Fecha_Desde}/{Fecha_Hasta}", response_model = list[AMP_STN_schema.Ampliacion_STN_Liquidacion], tags = ["Ampliaciones del STN"])
def leer_ampliacion_STN_por_rango_de_liquidaciones_PPA(Fecha_Desde: date, Fecha_Hasta: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Convocatorias STR de acuerdo a:
        
        - **Fecha_Desde**: Fecha Desde la que se quiere buscar la liquidacion con formato YYYY-mm-dd
        - **Fecha_Hasta**: Fecha Hasta la que se quiere buscar la liquidacion con formato YYYY-mm-dd
    """
    if AMP_STN_crud.get_ampliacion_STN_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta):
        return AMP_STN_crud.get_ampliacion_STN_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación entre {Fecha_Desde} y {Fecha_Hasta}")





#* FUNCIONES DE EXPANSION OR STR
# CREAR EXPANSION OR STR A UNA LIQUIDACION PPA
@app.post("/Expansion_OR_STR/{Proyecto}/Proyecto/{Liquidacion}/Liquidacion_PPA/{Version}/Version", response_model = EXP_STR_schema.Expansion_OR_STR, tags = ["Expansiones OR del STR"])
def crear_expansion_OR_STR_por_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, Version: str, db: Session = Depends(get_db)):
    """
        Crear Calculo de Expansión STR
    
    - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    - **Version**: Est, Liq, Aju1 o Aju2

    **Importante**

    Esta función se utiliza solo cuando por alguna razón, sea quee faltaron datos o falta de actualización la liquidación quedo en cero.
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Proyecto, Liquidacion_PPA, Version)
    LIQ_validation.verificar_calculo_unico(db, Proyecto, Liquidacion_PPA, Version)
    return EXP_STR_crud.create_expansion_OR_STR_individual(db, Proyecto, Liquidacion_PPA, Version)


# ACTUALIZAR EXPANSION OR STR
@app.put("/Expansion_OR_STR/{EXP_STR_id}", response_model = EXP_STR_schema.Expansion_OR_STR, tags = ["Expansiones OR del STR"])
def actualizar_expansion_OR_STR(EXP_STR_id: int, db: Session = Depends(get_db)):
    """
        Actualizar Calculo de Expansión STR de acuerdo a:

    - **EXP_STR_id**: Posición del dato en la base de datos

    """
    EXP_STR_validation.verificar_expansion_OR_STR(db, EXP_STR_id) 
    return EXP_STR_crud.update_expansion_OR_STR(db, EXP_STR_id)


# ELIMINAR EXPANSION OR STR
@app.delete("/Expansion_OR_STR/{EXP_STR_id}", tags = ["Expansiones OR del STR"])
def eliminar_expansion_OR_STR(EXP_STR_id: int, db: Session = Depends(get_db)):
    """
            Eliminar Calculo de Expansión STR de acuerdo a:
        
        - **EXP_STR_id**: Posición del dato en la base de datos
    """
    EXP_STR_validation.verificar_expansion_OR_STR(db, EXP_STR_id)
    return EXP_STR_crud.delete_expansion_OR_STR(db, EXP_STR_id)


# MOSTRAR TODAS LAS AMPLIACIONES STR
@app.get("/Expansiones_OR_STR/", response_model = list[EXP_STR_schema.Expansion_OR_STR], tags = ["Expansiones OR del STR"])
def leer_expansiones_OR_STR(db: Session = Depends(get_db)):
    """
            Buscar todos los Calculos de Expansiones STR
        No se requiere introducir datos

    """
    return EXP_STR_crud.get_expansiones_OR_STR(db)


# MOSTRAR EXPANSION OR STR
@app.get("/Expansion_OR_STR/{EXP_STR_id}", response_model = EXP_STR_schema.Expansion_OR_STR, tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR(EXP_STR_id: int, db: Session = Depends(get_db)):
    """
            Buscar uno Calculo de Expansión STR de acuerdo a:
        
        - **EXP_STR_id**: Posición del dato en la base de datos
    """
    EXP_STR_validation.verificar_expansion_OR_STR(db, EXP_STR_id)
    return EXP_STR_crud.get_expansion_OR_STR(db, EXP_STR_id)


# MOSTRAR EXPANSION OR STR POR AGENTE
@app.get("/Expansiones_OR_STR/{Agente}/Agente", response_model = list[EXP_STR_schema.Expansion_OR_STR_Agente], tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR_por_agente(Agente: str, db: Session = Depends(get_db)):
    """
            Buscar una o varios Calculos de Expansiones STR de acuerdo a:
        
        - **Agente**: ASIC del Agente
    """
    AGE_validation.verificar_agente(db, Agente)
    if EXP_STR_crud.get_expansion_OR_STR_agente(db, Agente):
        return EXP_STR_crud.get_expansion_OR_STR_agente(db, Agente)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Agente {Agente}")


# MOSTRAR EXPANSION OR STR POR PROYECTO
@app.get("/Expansiones_OR_STR/{Proyecto}/Proyecto", response_model = list[EXP_STR_schema.Expansion_OR_STR_Proyecto], tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR_por_proyecto(Proyecto: str, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Expansiones STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    if EXP_STR_crud.get_expansion_OR_STR_proyecto(db, Proyecto):
        return EXP_STR_crud.get_expansion_OR_STR_proyecto(db, Proyecto)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto}")


# MOSTRAR EXPANSION OR STR POR LIQUIDACION PPA
@app.get("/Expansiones_OR_STR/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[EXP_STR_schema.Expansion_OR_STR_Liquidacion], tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR_por_liquidacion_PPA(Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Expansiones STR de acuerdo a:
        
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if EXP_STR_crud.get_expansion_OR_STR_liquidacion(db, Liquidacion_PPA):
        return EXP_STR_crud.get_expansion_OR_STR_liquidacion(db, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS AMPLIACION STN POR PROYECTO Y LIQUIDACION PPA
@app.get("/Expansiones_OR_STR/{Proyecto}/Proyecto/{Liquidacion_PPA}/Liquidacion_PPA", response_model = list[EXP_STR_schema.Expansion_OR_STR_Proyecto_Liquidacion], tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR_por_proyecto_y_liquidacion_PPA(Proyecto: str, Liquidacion_PPA: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Expansiones STR de acuerdo a:
        
        - **Proyecto**: Codigo del Proyecto (Codigo_Proyecto)
        - **Liquidacion_PPA**: Fecha de la validez con formato YYYY-mm-dd
    """
    PRO_validation.verificar_proyecto(db, Proyecto)
    LIQ_validation.verificar_liquidacion_PPA(db, Liquidacion_PPA)
    if EXP_STR_crud.get_expansion_OR_STR_proyecto_liquidacion(db, Proyecto, Liquidacion_PPA):
        return EXP_STR_crud.get_expansion_OR_STR_proyecto_liquidacion(db, Proyecto, Liquidacion_PPA)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros del Proyecto {Proyecto} y con la Liquidación {Liquidacion_PPA}")


# MOSTRAR TODAS LAS EXPANSION OR STR POR LIQUIDACION PPA PPA RANGO
@app.get("/Expansiones_OR_STR/Rango/{Fecha_Desde}/{Fecha_Hasta}", response_model = list[EXP_STR_schema.Expansion_OR_STR_Liquidacion], tags = ["Expansiones OR del STR"])
def leer_expansion_OR_STR_por_rango_de_liquidaciones_PPA(Fecha_Desde: date, Fecha_Hasta: date, db: Session = Depends(get_db)):
    """
            Buscar uno o varios Calculos de Expansiones STR de acuerdo a:
        
        - **Fecha_Desde**: Fecha Desde la que se quiere buscar la liquidacion con formato YYYY-mm-dd
        - **Fecha_Hasta**: Fecha Hasta la que se quiere buscar la liquidacion con formato YYYY-mm-dd
    """
    if EXP_STR_crud.get_expansion_OR_STR_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta):
        return EXP_STR_crud.get_expansion_OR_STR_liquidacion_rango(db, Fecha_Desde, Fecha_Hasta)
    else: 
        raise HTTPException(status_code = 400, detail = f"No existen registros de Liquidación entre {Fecha_Desde} y {Fecha_Hasta}")
