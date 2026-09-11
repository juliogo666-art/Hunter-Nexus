import pytest
from src.data.database import obtener_conexion

@pytest.fixture(scope="session", autouse=True)
def crear_tablas_db():
    """
    Fixture de sesión que crea las tablas necesarias en la base de datos
    una sola vez antes de ejecutar la suite de pruebas.
    """
    sql_crear_tabla = """
    CREATE TABLE IF NOT EXISTS hunters (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        nivel INT DEFAULT 1,
        rango VARCHAR(50) DEFAULT 'E',
        clase VARCHAR(50),
        experiencia INT DEFAULT 0,
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
    Fixture de Pytest que se ejecuta automáticamente antes de cada test.
    Limpia la tabla 'hunters' y reinicia los IDs autonuméricos.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE hunters RESTART IDENTITY CASCADE;")
        conn.commit()
    yield