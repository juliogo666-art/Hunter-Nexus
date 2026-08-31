''' Tipo de Nen del Hunter'''

from enum import Enum

class Tipo_Nen(Enum):
    INTENSIFICACION = 1
    EMISION = 2
    TRANSMUTACION = 3
    MANIPULACION = 4
    MATERIALIZACION = 5
    ESPECIALIZACION = 6

class Hunter:
    def __init__(
            self,
            nombre: str,
            tipo_nen: Tipo_Nen, 
            nivel: int=1, 
            hp: float = 100.0 , 
            fuerza: float=10 , 
            aura: float=500 
    ):
        self.nombre = nombre
        self.tipo_nen = tipo_nen
        self.nivel = nivel
        self.hp = hp
        self.fuerza = fuerza
        self.aura = aura


    # 1. Personaje vivo
    def esta_vivo(self) -> bool:
        return self.hp > 0


    # 2. Ataque

    def atacar(self, objetivo: "Hunter"):
        dano = self.fuerza

        # Aplicamos multiplicador
        if self.tipo_nen == Tipo_Nen.INTENSIFICACION :
            dano *= 1.5

        objetivo.hp -= dano

