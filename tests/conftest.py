import pytest
from src.data.database import obtener_conexion

@pytest.fixture(scope="session", autouse=True)
def crear_tablas_db():
    """
    Crea la tabla 'hunters' con la estructura exacta requerida por la API.
    """
    sql_crear_tabla = """
    CREATE TABLE IF NOT EXISTS hunters (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        tipo_nen VARCHAR(50) NOT NULL,
        nivel INT DEFAULT 1,
        fuerza INT DEFAULT 10,
        hp INT DEFAULT 100,
        aura INT DEFAULT 10,
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_crear_tabla)
        conn.commit()

@pytest.fixture(autouse=True)
def limpiar_tabla_hunters(crear_tablas_db):
    """
    Limpia la tabla 'hunters' e inicializa los IDs antes de cada test.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE hunters RESTART IDENTITY CASCADE;")
        conn.commit()
    yield