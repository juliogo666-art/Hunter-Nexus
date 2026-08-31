from src.models.hunter import Hunter, Tipo_Nen

gon = Hunter(nombre="Gon Freecss",  tipo_nen=Tipo_Nen.INTENSIFICACION, fuerza=20.0)
Killua = Hunter(nombre="Killua zoldyck", tipo_nen=Tipo_Nen.TRANSMUTACION, fuerza=18.0)

print(f"vide inicial gon: {gon.hp}")
print(f"vida inicial Killua {Killua.hp}")

gon.atacar(Killua)

print(f"vida Killua tras golpe de Gon: {Killua.hp}")
print(f"¿sigue vido killua? {Killua.esta_vivo()}")