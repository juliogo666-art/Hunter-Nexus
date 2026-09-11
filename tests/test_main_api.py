'''
Para ejecutar el test en terminal  --> python -m pytest -v
'''
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
    nombre = get_unique_name("Lvl")
    payload_reg = {
        "nombre": nombre,
        "tipo_nen": "Transformacion",
        "nivel": 10,
        "fuerza": 70,
        "hp": 100,
        "aura": 80
    }
    client.post("/hunters", json=payload_reg)
    
    response = client.post(f"/hunters/{nombre}/subir-nivel", json={"niveles": 3})
    assert response.status_code == 200
    assert response.json()["nivel"] == 13


def test_listar_hunters_con_filtros_y_paginacion():
    # Insertar 2 cazadores
    client.post("/hunters", json={
        "nombre": "Gon", "tipo_nen": "Intensificacion", "nivel": 10, "fuerza": 80, "hp": 100, "aura": 90
    })
    client.post("/hunters", json={
        "nombre": "Killua", "tipo_nen": "Transformacion", "nivel": 12, "fuerza": 85, "hp": 95, "aura": 95
    })

    # Test 1: Filtrar por tipo_nen
    res_nen = client.get("/hunters?tipo_nen=intensificacion")
    assert res_nen.status_code == 200
    assert len(res_nen.json()) == 1
    assert res_nen.json()[0]["nombre"] == "Gon"

    # Test 2: Filtrar por nivel_min
    res_lvl = client.get("/hunters?nivel_min=11")
    assert res_lvl.status_code == 200
    assert len(res_lvl.json()) == 1
    assert res_lvl.json()[0]["nombre"] == "Killua"

    # Test 3: Paginación (limit=1)
    res_pag = client.get("/hunters?limit=1&offset=0")
    assert res_pag.status_code == 200
    assert len(res_pag.json()) == 1

def test_actualizar_hunter_parcial():
    # Insertar un cazador base
    res_crear = client.post("/hunters", json={
        "nombre": "Leorio", "tipo_nen": "Emision", "nivel": 10, "fuerza": 60, "hp": 90, "aura": 70
    })
    hunter_id = res_crear.json()["id"]

    # PATCH: Modificar solo el nivel y la fuerza
    res_patch = client.patch(f"/hunters/{hunter_id}", json={"nivel": 15, "fuerza": 75})
    assert res_patch.status_code == 200
    assert res_patch.json()["nivel"] == 15
    assert res_patch.json()["fuerza"] == 75
    # Los demás campos deben permanecer intactos
    assert res_patch.json()["nombre"] == "Leorio"

def test_eliminar_hunter():
    res_crear = client.post("/hunters", json={
        "nombre": "Tonpa", "tipo_nen": "Intensificacion", "nivel": 1, "fuerza": 10, "hp": 10, "aura": 10
    })
    hunter_id = res_crear.json()["id"]

    # DELETE exitoso
    res_del = client.delete(f"/hunters/{hunter_id}")
    assert res_del.status_code == 204

    # Intentar eliminarlo de nuevo debe devolver 404
    res_del_404 = client.delete(f"/hunters/{hunter_id}")
    assert res_del_404.status_code == 404