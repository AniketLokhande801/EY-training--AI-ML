from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_course():
    course = {
        "id": 2,
        "title": "Data Science",
        "duration": 40,
        "fee": 4500,
        "is_active": True
    }
    response = client.post("/courses", json=course)
    assert response.status_code == 201
    assert response.json()["title"] == course["title"]

@pytest.mark.parametrize("course", [
    {"id": 1, "title": "Python Advanced", "duration": 35, "fee": 3500, "is_active": True},
    {"id": 2, "title": "ML Basics", "duration": 25, "fee": 2500, "is_active": True}
])
def test_duplicate_course(course):
    response = client.post("/courses", json=course)
    assert response.status_code == 400
    assert response.json()["detail"] == "Course ID already exists"

def test_invalid_course():
    course = {
        "id": 3,
        "title": "AI",
        "duration": 0,
        "fee": -500,
        "is_active": True
    }
    response = client.post("/courses", json=course)
    assert response.status_code == 422
    assert "greater_than" in response.text
    assert "string_too_short" in response.text


def test_get_courses():
    response = client.get("/courses")
    data = response.json()
    assert isinstance(data, list)
    for i in data:
        assert "id" in i
        assert "title" in i
        assert "duration" in i
        assert "fee" in i
        assert "is_active" in i