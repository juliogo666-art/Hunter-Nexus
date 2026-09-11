import psycopg

#DSN = "postgresql://hunter_admin:hunter_password@localhost:5433/hunter_nexus_db"
DSN = "postgresql://hunter_admin:hunter_password@127.0.0.1:5433/hunter_nexus_db?connect_timeout=5"

def obtener_conexion():
    return psycopg.connect(DSN)

def inicializar_bbdd():
    query_tabla_hunters = """
    CREATE TABLE IF NOT EXISTS hunters (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        tipo_nen VARCHAR(50) NOT NULL,
        nivel INT DEFAULT 1,
        hp FLOAT NOT NULL,
        fuerza FLOAT NOT NULL,
        aura FLOAT NOT NULL
    );
    """
    
    with obtener_conexion() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_tabla_hunters)
        conn.commit()
    print("Base de datos inicializada correctamente en PostgreSQL.")

if __name__ == "__main__":
    inicializar_bbdd()