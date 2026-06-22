"""
Automated tests. Run them with:  pytest

These send fake requests to the API (without starting a real server) and
check the responses are correct. Good tests let other developers change the
code with confidence.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_student_risk_high_for_weak_student():
    response = client.post("/prediction/student-risk", json={
        "student_id": "STU-1001",
        "attendance_percentage": 50,
        "current_gpa": 1.8,
        "assignments_submitted": 3,
        "assignments_total": 10,
        "backlogs": 3,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["may_fail"] is True
    assert len(data["alerts"]) >= 1


def test_gpa_prediction_in_range():
    response = client.post("/prediction/gpa", json={
        "student_id": "STU-1002",
        "previous_gpa": 3.4,
        "attendance_percentage": 90,
        "study_hours_per_week": 15,
        "assignments_submitted": 10,
        "assignments_total": 10,
    })
    assert response.status_code == 200
    assert 0 <= response.json()["predicted_gpa"] <= 4


def test_admissions_decision():
    response = client.post("/prediction/admissions", json={
        "applicant_id": "APP-1",
        "entry_test_score": 90,
        "previous_grade_percentage": 88,
        "interview_score": 85,
    })
    assert response.status_code == 200
    assert response.json()["decision"] in {"admit", "waitlist", "reject"}


def test_erp_alerts_for_known_student():
    response = client.get("/alerts/student/STU-1001")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_erp_unknown_student_returns_404():
    response = client.get("/alerts/student/DOES-NOT-EXIST")
    assert response.status_code == 404
