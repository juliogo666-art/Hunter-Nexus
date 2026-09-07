from src.data.repository import obtener_hunter_por_nombre, actualizar_hunter

def calcular_poder_combate(hunter: dict) -> float:
    """Calcula el poder de combate basado en HP, Fuerza y Aura."""
    multiplicador_nen = 1.2 if hunter["tipo_nen"] == "Intensificación" else 1.0
    poder_base = (hunter["hp"] * 0.3) + (hunter["fuerza"] * 1.5) + (hunter["aura"] * 2.0)
    return round(poder_base * multiplicador_nen, 2)

def subir_nivel_cazador(nombre: str, niveles_ganados: int = 1):
    """Incrementa el nivel y stats de un cazador en la base de datos."""
    hunter = obtener_hunter_por_nombre(nombre)
    if not hunter:
        print(f"Cazador '{nombre}' no encontrado.")
        return None

    nuevo_nivel = hunter["nivel"] + niveles_ganados
    nuevo_hp = hunter["hp"] + (10.0 * niveles_ganados)
    nueva_fuerza = hunter["fuerza"] + (5.0 * niveles_ganados)
    nueva_aura = hunter["aura"] + (8.0 * niveles_ganados)

    hunter_actualizado = actualizar_hunter(
        hunter_id=hunter["id"],
        nivel=nuevo_nivel,
        hp=nuevo_hp,
        fuerza=nueva_fuerza,
        aura=nueva_aura
    )
    print(f" ¡{nombre} subió al nivel {nuevo_nivel}!")
    return hunter_actualizado

if __name__ == "__main__":
    # Prueba rápida de servicio
    gon = obtener_hunter_por_nombre("Gon Freecss")
    if gon:
        poder = calcular_poder_combate(gon)
        print(f"Poder inicial de {gon['nombre']}: {poder}")
        
        # Subimos de nivel a Gon
        subir_nivel_cazador("Gon Freecss", niveles_ganados=2)
        gon_subido = obtener_hunter_por_nombre("Gon Freecss")
        nuevo_poder = calcular_poder_combate(gon_subido)
        print(f"Nuevo poder de {gon_subido['nombre']}: {nuevo_poder}")