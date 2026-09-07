import psycopg
from psycopg.rows import dict_row
from src.data.database import DSN

def obtener_conexion():
    # Usamos dict_row para que nos devuelva los resultados como diccionarios en lugar de tuplas
    return psycopg.connect(DSN, row_factory=dict_row)

def crear_hunter(nombre: str, tipo_nen: str, hp: float, fuerza: float, aura: float, nivel: int = 1):
    """Inserta un nuevo cazador en la base de datos."""
    query = """
    INSERT INTO hunters (nombre, tipo_nen, nivel, hp, fuerza, aura)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (nombre, tipo_nen, nivel, hp, fuerza, aura))
            hunter_id = cursor.fetchone()["id"]
        conn.commit()
    return hunter_id

def listar_hunters():
    """Devuelve la lista de todos los cazadores registrados."""
    query = "SELECT * FROM hunters ORDER BY id ASC;"
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

def obtener_hunter_por_nombre(nombre: str):
    """Busca un cazador específico por su nombre."""
    query = "SELECT * FROM hunters WHERE nombre = %s;"
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (nombre,))
            return cursor.fetchone()


def actualizar_hunter(hunter_id: int, nivel: int = None, hp: float = None, fuerza: float = None, aura: float = None):
    """Actualiza las estadísticas de un cazador existente."""
    query = """
    UPDATE hunters
    SET nivel = COALESCE(%s, nivel),
        hp = COALESCE(%s, hp),
        fuerza = COALESCE(%s, fuerza),
        aura = COALESCE(%s, aura)
    WHERE id = %s
    RETURNING *;
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (nivel, hp, fuerza, aura, hunter_id))
            updated = cursor.fetchone()
        conn.commit()
    return updated

def eliminar_hunter(hunter_id: int) -> bool:
    """Elimina un cazador por su ID."""
    query = "DELETE FROM hunters WHERE id = %s RETURNING id;"
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (hunter_id,))
            deleted = cursor.fetchone()
        conn.commit()
    return deleted is not None