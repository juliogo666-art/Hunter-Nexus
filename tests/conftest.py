import pytest
from src.data.database import obtener_conexion

@pytest.fixture(autouse=True)
def limpiar_tabla_hunters():
    """
    Fixture de Pytest que se ejecuta automáticamente antes de cada test.
    Limpia la tabla 'hunters' y reinicia los IDs autonuméritos.
    """
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE hunters RESTART IDENTITY CASCADE;")
        conn.commit()
    yield
    