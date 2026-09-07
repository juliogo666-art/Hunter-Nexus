from src.data.repository import crear_hunter, listar_hunters

HUNTERS_INICIALES = [
    {"nombre": "Gon Freecss", "tipo_nen": "Intensificación", "nivel": 10, "hp": 150.0, "fuerza": 85.0, "aura": 90.0},
    {"nombre": "Killua Zoldyck", "tipo_nen": "Transformación", "nivel": 12, "hp": 140.0, "fuerza": 88.0, "aura": 92.0},
    {"nombre": "Kurapika", "tipo_nen": "Materialización", "nivel": 11, "hp": 130.0, "fuerza": 80.0, "aura": 95.0},
    {"nombre": "Hisoka Morow", "tipo_nen": "Transformación", "nivel": 25, "hp": 220.0, "fuerza": 110.0, "aura": 130.0},
]

def cargar_datos_semilla():
    print("Cargando cazadores iniciales...")
    for h in HUNTERS_INICIALES:
        try:
            h_id = crear_hunter(
                nombre=h["nombre"],
                tipo_nen=h["tipo_nen"],
                nivel=h["nivel"],
                hp=h["hp"],
                fuerza=h["fuerza"],
                aura=h["aura"]
            )
            print(f" Registrado: {h['nombre']} (ID: {h_id})")
        except Exception as e:
            print(f" Omite {h['nombre']} (posiblemente ya existe o error: {e})")

    print("\n--- Estado actual de la base de datos ---")
    hunters = listar_hunters()
    for hunter in hunters:
        print(f"[{hunter['id']}] {hunter['nombre']} | Nen: {hunter['tipo_nen']} | Nivel: {hunter['nivel']} | HP: {hunter['hp']} | Fuerza: {hunter['fuerza']} | Aura: {hunter['aura']}")

if __name__ == "__main__":
    cargar_datos_semilla()