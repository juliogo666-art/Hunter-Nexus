from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from src.api.schemas import HunterCreate, HunterResponse, SubirNivelRequest
from src.data.repository import (
    actualizar_hunter,
    crear_hunter,
    eliminar_hunter,
    listar_hunters,
    obtener_hunter_por_nombre,
)
from src.domain.services import calcular_poder_combate, subir_nivel_cazador

app = FastAPI(
    title="Hunter-Nexus API",
    description="APP de gestión de cazadores de la asociación HXH",
    version="1.0.0",
)

######################################################################################################

@app.get("/", tags=["Healthcheck"])
def root():
    return {"status": "ok", "message": "Hunter-Nexus API activa y conectada a PostgreSQL"}

######################################################################################################

@app.get("/hunters", response_model=List[HunterResponse], tags=["Hunters"])
def get_hunters(
    tipo_nen: Optional[str] = Query(None, description="Filtrar por tipo de Nen"),
    nivel_min: Optional[int] = Query(None, ge=1, description="Nivel mínimo del cazador"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros por página"),
    offset: int = Query(0, ge=0, description="Número de registros a omitir"),
):
    hunters = listar_hunters(tipo_nen=tipo_nen, nivel_min=nivel_min, limit=limit, offset=offset)
    for h in hunters:
        h["poder_combate"] = calcular_poder_combate(h)
    return hunters

######################################################################################################

@app.get("/hunters/{nombre}", response_model=HunterResponse, tags=["Hunters"])
def get_hunter(nombre: str):
    hunter = obtener_hunter_por_nombre(nombre)
    if not hunter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cazador '{nombre}' no encontrado",
        )
    hunter["poder_combate"] = calcular_poder_combate(hunter)
    return hunter

######################################################################################################

@app.post("/hunters", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Hunters"])
def registrar_hunter(hunter: HunterCreate):
    try:
        hunter_id = crear_hunter(
            nombre=hunter.nombre,
            tipo_nen=hunter.tipo_nen,
            hp=hunter.hp,
            fuerza=hunter.fuerza,
            aura=hunter.aura,
            nivel=hunter.nivel,
        )
        return {"id": hunter_id, "message": f"Cazador {hunter.nombre} registrado"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo crear el cazador: {str(e)}",
        )

######################################################################################################

@app.post("/hunters/{nombre}/subir-nivel", response_model=HunterResponse, tags=["Acciones"])
def trigger_subir_nivel(nombre: str, req: SubirNivelRequest):
    hunter_actualizado = subir_nivel_cazador(nombre, niveles_ganados=req.niveles)
    if not hunter_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se pudo actualizar a {nombre}",
        )
    hunter_actualizado["poder_combate"] = calcular_poder_combate(hunter_actualizado)
    return hunter_actualizado

######################################################################################################

class HunterUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_nen: Optional[str] = None
    nivel: Optional[int] = Field(None, ge=1)
    fuerza: Optional[float] = Field(None, ge=0)
    hp: Optional[float] = Field(None, ge=0)
    aura: Optional[float] = Field(None, ge=0)


@app.patch("/hunters/{hunter_id}", response_model=HunterResponse, tags=["Hunters"])
def patch_hunter(hunter_id: int, datos: HunterUpdate):
    datos_dict = datos.model_dump(exclude_unset=True)
    if not datos_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )

    hunter_actualizado = actualizar_hunter(hunter_id, datos_dict)
    if not hunter_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún cazador con ID {hunter_id}",
        )

    hunter_actualizado["poder_combate"] = calcular_poder_combate(hunter_actualizado)
    return hunter_actualizado

######################################################################################################

@app.delete("/hunters/{hunter_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Hunters"])
def delete_hunter(hunter_id: int):
    exito = eliminar_hunter(hunter_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún cazador con ID {hunter_id}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
