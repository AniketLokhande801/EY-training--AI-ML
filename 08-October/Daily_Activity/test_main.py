from fastapi.testclient import TestClient
from main import app

client= TestClient(app)

def test_get_all():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(),list)

def test_post_emp():
    new_emp = {"id":2,"name":"soham","department":"hr","salary":20000}
    response = client.post("/employees",json=new_emp)
    assert response.status_code == 200
    assert response.json()["name"]=="soham"

def test_get_eid():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"]=="aniket"

def test_get_eid_EH():
    response = client.get("/employees/999")
    assert response.status_code == 404
    # assert response.json()["name"]=="aniket"

def test_put():
    new_emp={"id":1,"name":"rohit","department":"IT","salary":2000}
    response = client.put("/employees/1",json=new_emp)
    assert response.status_code == 200
    assert response.json()["name"]=="rohit"
    # assert isinstance(response.json(),list)

def test_delete():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()["message"]=="SUCCESS!"