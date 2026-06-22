# API Documentation — Early Warning System & Prediction API

**Version:** 1.0.0
**Base URL:** `http://127.0.0.1:8000`
**Interactive docs:** `/docs` (Swagger UI) · `/redoc` (ReDoc) · `/openapi.json` (spec)

All prediction endpoints accept **JSON** in the request body and return **JSON**.
`Content-Type: application/json` is required for POST requests.

---

## Common concepts

**`risk_level`** — a human-friendly label derived from a 0–1 score:

| Score range | risk_level |
|-------------|------------|
| 0.00 – 0.29 | `low`      |
| 0.30 – 0.59 | `medium`   |
| 0.60 – 0.79 | `high`     |
| 0.80 – 1.00 | `critical` |

**`Alert` object** (returned inside several responses):

```json
{
  "student_id": "STU-1001",
  "type": "low_attendance",        // may_fail | low_attendance | fee_payment_risk | dropout_risk
  "severity": "medium",            // low | medium | high | critical
  "message": "Attendance is 62%, below the required 75%.",
  "score": 0.473
}
```

---

## Health

### `GET /health`
Confirms the server is running.

**Response 200**
```json
{ "status": "healthy", "erp_mock_mode": true }
```

---

## Predictions

### 1. `POST /prediction/student-risk`
Predicts whether a student is at academic risk / may fail.

**Request**
```json
{
  "student_id": "STU-1001",
  "attendance_percentage": 62,
  "current_gpa": 2.1,
  "assignments_submitted": 6,
  "assignments_total": 10,
  "backlogs": 2
}
```

**Response 200**
```json
{
  "student_id": "STU-1001",
  "risk_score": 0.419,
  "risk_level": "medium",
  "may_fail": false,
  "alerts": [
    {
      "student_id": "STU-1001",
      "type": "low_attendance",
      "severity": "medium",
      "message": "Attendance is 62%, below the required 75%.",
      "score": 0.473
    }
  ]
}
```

---

### 2. `POST /prediction/dropout`
Predicts the probability that a student drops out.

**Request**
```json
{
  "student_id": "STU-1001",
  "attendance_percentage": 55,
  "current_gpa": 1.8,
  "fee_overdue_days": 30,
  "engagement_score": 0.3
}
```

**Response 200**
```json
{
  "student_id": "STU-1001",
  "dropout_probability": 0.61,
  "risk_level": "high",
  "alerts": [ /* dropout_risk + low_attendance alerts */ ]
}
```

---

### 3. `POST /prediction/gpa`
Predicts a student's future GPA (0–4).

**Request**
```json
{
  "student_id": "STU-1001",
  "previous_gpa": 3.0,
  "attendance_percentage": 85,
  "study_hours_per_week": 12,
  "assignments_submitted": 9,
  "assignments_total": 10
}
```

**Response 200**
```json
{ "student_id": "STU-1001", "predicted_gpa": 3.25, "confidence": 0.96 }
```

---

### 4. `POST /prediction/fee-default`
Predicts the probability that a student defaults on fee payment.

**Request**
```json
{
  "student_id": "STU-1001",
  "outstanding_amount": 45000,
  "days_overdue": 20,
  "previous_late_payments": 3,
  "total_payments": 8
}
```

**Response 200**
```json
{
  "student_id": "STU-1001",
  "default_probability": 0.41,
  "risk_level": "medium",
  "alerts": []
}
```

---

### 5. `POST /prediction/admissions`
Predicts whether an applicant should be admitted.

**Request**
```json
{
  "applicant_id": "APP-2025-077",
  "entry_test_score": 78,
  "previous_grade_percentage": 82,
  "interview_score": 70
}
```

**Response 200**
```json
{
  "applicant_id": "APP-2025-077",
  "admission_probability": 0.77,
  "decision": "admit"      // admit (>=0.70) | waitlist (>=0.50) | reject (<0.50)
}
```

---

### 6. `POST /prediction/recommendations`
Generates personalised recommendations for a student.

**Request**
```json
{
  "student_id": "STU-1001",
  "attendance_percentage": 60,
  "current_gpa": 2.2,
  "weak_subjects": ["Math", "Physics"]
}
```

**Response 200**
```json
{
  "student_id": "STU-1001",
  "recommendations": [
    "Improve attendance to at least 75% to stay eligible for exams.",
    "Meet your academic advisor to build a GPA recovery plan.",
    "Attend extra tutoring / practice sessions for Math.",
    "Attend extra tutoring / practice sessions for Physics."
  ]
}
```

---

## Early Warning System (ERP integration)

### `GET /alerts/student/{student_id}`
Fetches a student from the ERP, runs every model, and returns all
early-warning alerts. Optional query param `push_to_erp=true` also saves the
alerts back into the ERP.

**Example:** `GET /alerts/student/STU-1001`

In mock mode try:
- `STU-1001` → a risky student (returns alerts)
- `STU-1002` → a healthy student (returns `[]`)
- unknown id → `404 Not Found`

**Response 200**
```json
[
  {
    "student_id": "STU-1001",
    "type": "low_attendance",
    "severity": "medium",
    "message": "Attendance is 62%, below the required 75%.",
    "score": 0.473
  }
]
```

**Response 404**
```json
{ "detail": "Student 'XYZ' not found in ERP" }
```

---

## Validation errors

If the request body is missing a field or a value is out of range (e.g.
`attendance_percentage` above 100), FastAPI returns **422 Unprocessable Entity**
with a detailed list of what was wrong. This validation is automatic.
