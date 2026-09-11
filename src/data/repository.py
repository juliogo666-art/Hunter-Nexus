import psycopg
from psycopg.rows import dict_row
from src.data.database import DSN

def obtener_conexion():
    # Usamos dict_row para que nos devuelva los resultados como diccionarios en lugar de tuplas
    return psycopg.connect(DSN, row_factory=dict_row)

####################################################################################################

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

####################################################################################################

def listar_hunters(tipo_nen: str = None, nivel_min: int = None, limit: int = 10, offset: int = 0):

    """Devuelve la lista de cazadores con opción de filtrado y paginación."""
    
    query = "SELECT * FROM hunters WHERE 1=1"
    params = []

    if tipo_nen:
        query += " AND LOWER(tipo_nen) = LOWER(%s)"
        params.append(tipo_nen)

    if nivel_min is not None:
        query += " AND nivel >= %s"
        params.append(nivel_min)

    query += " ORDER BY id ASC LIMIT %s OFFSET %s;"
    params.extend([limit, offset])

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            return cursor.fetchall()

####################################################################################################

def obtener_hunter_por_nombre(nombre: str):
    """Busca un cazador específico por su nombre."""
    query = "SELECT * FROM hunters WHERE nombre = %s;"
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (nombre,))
            return cursor.fetchone()

####################################################################################################

def actualizar_hunter(hunter_id: int, datos: dict = None, **kwargs):
    """Actualiza solo los campos especificados de un cazador."""
    payload = {}
    if datos:
        payload.update(datos)
    if kwargs:
        payload.update(kwargs)

    if not payload:
        return None

    campos = [f"{clave} = %s" for clave in payload.keys()]
    valores = list(payload.values())
    valores.append(hunter_id)

    query = f"""
        UPDATE hunters 
        SET {', '.join(campos)}
        WHERE id = %s
        RETURNING *;
    """

    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(valores))
            hunter = cursor.fetchone()
            conn.commit()
            return hunter

####################################################################################################

def eliminar_hunter(hunter_id: int) -> bool:
    """Elimina un cazador por su ID y devuelve True si existía."""
    query = "DELETE FROM hunters WHERE id = %s RETURNING id;"
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (hunter_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None