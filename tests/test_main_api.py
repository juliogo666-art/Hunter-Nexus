import uuid
import pytest
from fastapi.testclient import TestClient
from src.api.main_api import app

client = TestClient(app)

def get_unique_name(prefix="Hunter"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200

def test_registrar_hunter():
    nombre = get_unique_name("Reg")
    payload = {
        "nombre": nombre,
        "tipo_nen": "Materializacion",
        "nivel": 10,
        "fuerza": 70,
        "hp": 100,
        "aura": 80
    }
    response = client.post("/hunters", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert "message" in data

def test_registrar_hunter_duplicado():
    nombre = get_unique_name("Dup")
    payload = {
        "nombre": nombre,
        "tipo_nen": "Materializacion",
        "nivel": 10,
        "fuerza": 70,
        "hp": 100,
        "aura": 80
    }
    client.post("/hunters", json=payload)
    response = client.post("/hunters", json=payload)
    assert response.status_code == 400

def test_get_hunter_existente():
    nombre = get_unique_name("Get")
    payload = {
        "nombre": nombre,
        "tipo_nen": "Intensificacion",
        "nivel": 5,
        "fuerza": 50,
        "hp": 100,
        "aura": 50
    }
    client.post("/hunters", json=payload)
    response = client.get(f"/hunters/{nombre}")
    assert response.status_code == 200

def test_get_hunter_inexistente():
    nombre = get_unique_name("NoExist")
    response = client.get(f"/hunters/{nombre}")
    assert response.status_code == 404

def test_subir_nivel():
    # 1. Inspeccionar el esquema OpenAPI para detectar el nombre exacto de la clave/parámetro
    openapi_spec = client.get("/openapi.json").json()
    path_info = openapi_spec.get("paths", {}).get("/hunters/{nombre}/subir-nivel", {}).get("post", {})
    
    param_key = None
    
    # Si la API espera el parámetro en el cuerpo JSON (Body)
    if "requestBody" in path_info:
        content = path_info["requestBody"].get("content", {}).get("application/json", {})
        schema_ref = content.get("schema", {})
        
        if "$ref" in schema_ref:
            schema_name = schema_ref["$ref"].split("/")[-1]
            properties = openapi_spec.get("components", {}).get("schemas", {}).get(schema_name, {}).get("properties", {})
            if properties:
                param_key = list(properties.keys())[0]
        elif "properties" in schema_ref:
            param_key = list(schema_ref["properties"].keys())[0]
            
    # Si la API lo espera como Query Parameter
    elif "parameters" in path_info:
        for param in path_info["parameters"]:
            if param.get("name") != "nombre":
                query_param_name = param.get("name")
                
                # Caso Query Parameter
                nombre = get_unique_name("Lvl")
                client.post("/hunters", json={
                    "nombre": nombre, "tipo_nen": "Transformacion",
                    "nivel": 10, "fuerza": 70, "hp": 100, "aura": 80
                })
                
                res_get = client.get(f"/hunters/{nombre}")
                nivel_inicial = res_get.json()["nivel"]
                
                response = client.post(f"/hunters/{nombre}/subir-nivel", params={query_param_name: 3})
                assert response.status_code == 200
                assert response.json()["nivel"] == nivel_inicial + 3
                return

    # Si no se detectó parámetro específico, intentamos con la clave encontrada o un fallback directo
    field_name = param_key or "incremento_nivel"
    
    nombre = get_unique_name("Lvl")
    client.post("/hunters", json={
        "nombre": nombre, "tipo_nen": "Transformacion",
        "nivel": 10, "fuerza": 70, "hp": 100, "aura": 80
    })

    res_get = client.get(f"/hunters/{nombre}")
    nivel_inicial = res_get.json()["nivel"]
    
    response = client.post(f"/hunters/{nombre}/subir-nivel", json={field_name: 3})
    assert response.status_code == 200
    assert response.json()["nivel"] == nivel_inicial + 3