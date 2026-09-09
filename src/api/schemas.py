from pydantic import BaseModel, Field
from typing import Optional

# Esquema Base: Los atributos compartidos por un cazador
class HunterBase(BaseModel):
    nombre: str
    tipo_nen: str
    hp: float = Field(gt=0, description="Puntos de vida del cazador")
    fuerza: float = Field(gt=0, description="Estadística de fuerza")
    aura: float = Field(gt=0, description="Estadística de aura")

# Esquema de Creación:  Añade el nivel como un campo opcional cuyo valor por defecto sea 1
class HunterCreate(HunterBase):
    nivel: Optional[int] = 1

# Esquema de Respuesta:incluimos los campos que la base de datos o el sistema calculan
class HunterResponse(HunterBase):
    id: int
    nivel: int
    poder_combate: Optional[float] = None

# Esquema de Acción: Un objeto pequeño con el campo niveles para controlar cuántos niveles se suben
class SubirNivelRequest(BaseModel):
    niveles: int = Field(default=1, ge=1, description="Número de niveles a subir")