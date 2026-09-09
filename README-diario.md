# Dia 1 y 2

Recordadon conceptos basicos arquitectura, programas base con: class , metodos ....

# Dia 3

Instalacion y preparacion de docker
Infraestructura Docker: Contenedor de PostgreSQL (hunter_postgres) estable en el puerto 5433 evadiendo conflictos de red.

Capa de Datos (src/data/):

- database.py: Manejo de conexiones y creación de tablas.

- repository.py: CRUD completo (Insertar, Listar, Buscar por nombre, Actualizar y Eliminar).

- seed.py: Carga inicial de cazadores (Gon, Killua, Kurapika, Hisoka) lista y probada.

Capa de Dominio (src/domain/):

- services.py: Primeros algoritmos de cálculo de poder de combate y escalado de niveles.

# Día 4 y 5

- Comprension dockerdesktop --> visualizacion de datos por terminal
- DBeaver para visualiza la base de datos como una tabla de excel

- Servidor FastAPI 
    * Conexión
    * lectura lista
    * busqueda
    * registro
    * Actualizar
    * borrar