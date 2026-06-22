# Early Warning System & Prediction API

A FastAPI backend for a Student ERP. It exposes prediction endpoints
(student risk, dropout, GPA, fee default, admissions, recommendations) and an
**Early Warning System** that raises alerts and integrates with the ERP.

---

## 1. Project structure

```
app/
├── main.py                 App entry point (creates FastAPI, plugs in routes)
├── config.py               Settings, loaded from .env
│
├── api/routes/             HTTP layer — the endpoints (the "waiters")
│   ├── predictions.py        6 POST /prediction/* endpoints
│   └── alerts.py             Early Warning endpoints + ERP integration
│
├── schemas/                Data shapes for validation & docs (the "menu")
│   ├── common.py             RiskLevel, AlertType, Alert
│   └── prediction.py         Request/Response for each endpoint
│
├── services/               Business logic (the "chef")
│   ├── prediction_service.py
│   └── alert_service.py      The early-warning rules
│
├── models/                 ML model placeholder (the "recipe")
│   └── predictor.py          Swap rules for a real ML model later
│
└── integrations/           External systems (the "supplier")
    └── erp_client.py         Talks to the ERP (mock or real)

tests/test_api.py           Automated tests
requirements.txt            Dependencies
.env.example                Copy to .env and fill in real values
```

**Design idea:** each layer has one job. To swap the ML model, edit only
`models/predictor.py`. To change the ERP, edit only `integrations/erp_client.py`.
Nothing else has to change.

---

## 2. How to run it

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate        # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) create your settings file
copy .env.example .env             # Windows
# cp .env.example .env             # macOS / Linux

# 4. Start the server
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/docs** — interactive API documentation
where you can try every endpoint in the browser.

Run the tests with:

```bash
pytest
```

---

## 3. Endpoints

| Method | Path                            | Purpose                              |
|--------|---------------------------------|--------------------------------------|
| GET    | `/health`                       | Server health check                  |
| POST   | `/prediction/student-risk`      | Is the student at risk / may fail?   |
| POST   | `/prediction/dropout`           | Dropout probability                  |
| POST   | `/prediction/gpa`               | Predicted future GPA                 |
| POST   | `/prediction/fee-default`       | Fee default probability              |
| POST   | `/prediction/admissions`        | Admission probability + decision     |
| POST   | `/prediction/recommendations`   | Personalised recommendations         |
| GET    | `/alerts/student/{student_id}`  | All early-warning alerts (uses ERP)  |

### Example request

```bash
curl -X POST http://127.0.0.1:8000/prediction/student-risk \
  -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","attendance_percentage":62,"current_gpa":2.1,"assignments_submitted":6,"assignments_total":10,"backlogs":2}'
```

---

## 4. ERP integration

`integrations/erp_client.py` is the only file that talks to the ERP.

- While `ERP_MOCK_MODE=true` (default) it returns realistic fake data and
  does not need the internet. Try student IDs `STU-1001` and `STU-1002`.
- Set `ERP_MOCK_MODE=false` and fill in `ERP_BASE_URL` + `ERP_API_KEY` in
  `.env` to talk to the real ERP.

---

## 5. Connecting a real ML model later

In `models/predictor.py`, replace the rule-based body of each method with a
real model call, e.g.:

```python
import joblib
self.model = joblib.load("dropout_model.pkl")
return float(self.model.predict_proba([[...features...]])[0][1])
```

As long as the inputs/outputs stay the same, the rest of the app is untouched.
```
