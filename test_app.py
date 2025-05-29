import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Prueba unitaria: verificar que la ruta '/' responde correctamente."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.data

def test_procesar_interpolacion(client):
    """Prueba de integración: verificar el procesamiento e interpolación de datos."""
    data = {
        "datos": "1,2,3,4,5",
        "metodo": "interpolacion"
    }
    response = client.post("/procesar", data=data)
    assert response.status_code == 200
    assert b"Interpolaci" in response.data
