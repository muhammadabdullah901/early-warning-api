"""
ERP integration layer.

This is the ONLY file that knows how to talk to the ERP system. Everything
else in the app just calls these functions. If the ERP changes, you fix it
here and nowhere else.

Two modes (controlled by ERP_MOCK_MODE in the .env file):
  * mock mode  -> returns realistic fake data, no internet needed (great for dev)
  * real mode  -> sends real HTTP requests to your ERP using httpx
"""

import httpx
from app.config import settings
from app.schemas.common import Alert


# A few fake students used while ERP_MOCK_MODE is true.
_FAKE_STUDENTS = {
    "STU-1001": {
        "student_id": "STU-1001",
        "name": "Ali Khan",
        "attendance_percentage": 62,
        "current_gpa": 2.1,
        "assignments_submitted": 6,
        "assignments_total": 10,
        "backlogs": 2,
        "fee_overdue_days": 30,
        "engagement_score": 0.4,
    },
    "STU-1002": {
        "student_id": "STU-1002",
        "name": "Sara Ahmed",
        "attendance_percentage": 91,
        "current_gpa": 3.6,
        "assignments_submitted": 10,
        "assignments_total": 10,
        "backlogs": 0,
        "fee_overdue_days": 0,
        "engagement_score": 0.9,
    },
}


class ERPClient:
    def __init__(self) -> None:
        self.base_url = settings.erp_base_url
        self.api_key = settings.erp_api_key
        self.mock = settings.erp_mock_mode

    # Standard auth header most ERPs expect.
    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"}

    # ---- Read a student's record from the ERP ----
    def get_student(self, student_id: str) -> dict | None:
        if self.mock:
            return _FAKE_STUDENTS.get(student_id)

        # Real call (used when ERP_MOCK_MODE=false)
        url = f"{self.base_url}/students/{student_id}"
        response = httpx.get(url, headers=self._headers(), timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    # ---- Push an alert back into the ERP so staff can see it ----
    def push_alert(self, alert: Alert) -> bool:
        if self.mock:
            # Pretend it was saved. In real life this would be an HTTP POST.
            print(f"[ERP-MOCK] Saved alert for {alert.student_id}: {alert.message}")
            return True

        url = f"{self.base_url}/alerts"
        response = httpx.post(url, headers=self._headers(),
                              json=alert.model_dump(), timeout=10)
        response.raise_for_status()
        return True


# A single shared ERP client for the whole app.
erp_client = ERPClient()
