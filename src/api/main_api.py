from fastapi import FastAPI, HTTPException, status
from typing import List

from src.api.schemas import HunterCreate, HunterResponse, SubirNivelRequest
from src.data.repository import listar_hunters, obtener_hunter_por_nombre , crear_hunter, eliminar_hunter
from src.domain.services import calcular_poder_combate, subir_nivel_cazador


app = FastAPI(title="Hunter-Nexus API",description="APP de gestion de cazadores de la asociacion HXH", version="1.0.0")

######################################################################################################
# Ejemplo explicativo

'''#1. Decorador ( ruta, metodo HTTP y metadato)
@app.post("/hunters/{nombre}/entrenar",response_model=HunterResponse, status_code=status.HTTP_200_OK)

    # Dirección de la ruta: Define la URL (ej. "/hunters" o "/hunters/{nombre}"
    # response_model: Obliga a FastAPI a filtrar y validar la respuesta usando un esquema de Pydantic. 
    #   Si tu función devuelve un diccionario con 20 campos pero tu HunterResponse solo define 5,
    #   FastAPI descartará los 15 sobrantes antes de enviar el JSON.
    # status_code: Define el código de estado HTTP predeterminado al responder con éxito

def entrenar_hunter(
    #2. Inyeccion de parametros (path, body, query)
    nombre: str, # parametro de ruta : Si el nombre del argumento coincide con una variable de la URL (/hunters/{nombre} --> nombre: str), FastAPI lo extrae directamente de la dirección web
    datos: SubirNivelRequest # cuerpo de la peticion: Si defines un argumento cuyo tipo es un modelo de Pydantic (req: SubirNivelRequest), FastAPI asume automáticamente que esos datos vienen en el cuerpo JSON de la petición HTTP. Valida su estructura antes de ejecutar la función.
):
    #3. Logica y validacion de negocio
    hunter = obtener_hunter_por_nombre(nombre)
    if not hunter:
        #4. Si hay error http
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cazador {nombre} no existe"
        )

    #5. retorno , serializado auto a JSON
    return hunter
'''

######################################################################################################

@app.get("/",tags=["Healthcheck"])
def root ():
    return {"status": "ok", "message":"Hunter-Nexus API activa"}

######################################################################################################

@app.get("/hunters", response_model=List[HunterResponse], tags=["Hunters"])
def get_hunters():
    hunters = listar_hunters()
    for h in hunters:
        h["poder_combate"] = calcular_poder_combate(h)
    return hunters

######################################################################################################

@app.get("/hunters/{nombre}", response_model=HunterResponse, tags=["Hunters"])
def get_hunter( nombre: str):
    hunter = obtener_hunter_por_nombre(nombre)
    if not hunter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=F"Cazador '{nombre}' no encontrado"
        )
    hunter["poder_combate"] = calcular_poder_combate(hunter)
    return hunter

######################################################################################################

@app.post("/hunters", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Hunters"])
def registrar_hunter(hunter: HunterCreate):
    try:
        hunter_id = crear_hunter(
            nombre= hunter.nombre,
            tipo_nen= hunter.tipo_nen,
            hp= hunter.hp,
            fuerza= hunter.fuerza,
            aura= hunter.aura,
            nivel= hunter.nivel
        )
        return {"id":hunter_id, "message":f"Cazador {hunter.nombre} registrado"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo crear el cazador: {str(e)}"
        )

######################################################################################################

@app.post("/hunters/{nombre}/subir-nivel", response_model=HunterResponse, tags=["Acciones"])
def trigger_subir_nivel(nombre:str, req:SubirNivelRequest):
    hunter_actualizado = subir_nivel_cazador(nombre, niveles_ganados=req.niveles)
    if not hunter_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se pudo actualizar a {nombre}"
        )
    hunter_actualizado["poder_combate"] = calcular_poder_combate(hunter_actualizado)
    return hunter_actualizado


######################################################################################################

@app.delete("/hunters/{hunter_id}", status_code=status.HTTP_200_OK)
def hunter_delete (hunter_id:  int):
    exito = eliminar_hunter(hunter_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cazador no encontrado"
        )
    return{ "message": f"Cazador con ID {hunter_id} eliminado"}

######################################################################################################