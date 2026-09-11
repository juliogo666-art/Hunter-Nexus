# Ejemplo explicativo en main_api de accion con servidor

'''#1. Decorador ( ruta, metodo HTTP y metadato)
@app.post("/hunters/{nombre}/entrenar",response_model=HunterResponse, status_code=status.HTTP_200_OK)

    # Dirección de la ruta: Define la URL (ej. "/hunters" o "/hunters/{nombre}"
    # response_model: Obliga a FastAPI a filtrar y validar la respuesta usando un esquema de Pydantic. 
    #   Si tu función devuelve un diccionario con 20 campos pero tu HunterResponse solo define 5,
    #   FastAPI descartará los 15 sobrantes antes de enviar el JSON.
    # status_code: Define el código de estado HTTP predeterminado al responder con éxito

def entrenar_hunter(
    #2. Inyeccion de parametros (path, body, query)
    nombre: str, # parametro de ruta : Si el nombre del argumento coincide con una variable de la URL (/hunters/{nombre} --> nombre: str), FastAPI lo extrae directamente de la dirección web
    datos: SubirNivelRequest # cuerpo de la peticion: Si defines un argumento cuyo tipo es un modelo de Pydantic (req: SubirNivelRequest), FastAPI asume automáticamente que esos datos vienen en el cuerpo JSON de la petición HTTP. Valida su estructura antes de ejecutar la función.
):
    #3. Logica y validacion de negocio
    hunter = obtener_hunter_por_nombre(nombre)
    if not hunter:
        #4. Si hay error http
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cazador {nombre} no existe"
        )

    #5. retorno , serializado auto a JSON
    return hunter
'''