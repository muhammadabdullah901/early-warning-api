"""
Early Warning System endpoints (the "alerts" side of the task).

This module ties everything together and shows the ERP integration end-to-end:
  1. read a student from the ERP,
  2. run the prediction models,
  3. build all four alert types,
  4. optionally push the alerts back into the ERP.
"""

from fastapi import APIRouter, HTTPException, Query
from app.integrations.erp_client import erp_client
from app.models.predictor import predictor
from app.services import alert_service as alerts
from app.schemas.common import Alert

router = APIRouter(prefix="/alerts", tags=["Early Warning System"])


def _evaluate_student(student: dict) -> list[Alert]:
    """Run every model + every alert rule for one student record."""
    sid = student["student_id"]
    submitted_ratio = (
        student["assignments_submitted"] / student["assignments_total"]
        if student.get("assignments_total") else 0.0
    )

    risk_score = predictor.predict_student_risk(
        student["attendance_percentage"], student["current_gpa"],
        submitted_ratio, student.get("backlogs", 0),
    )
    dropout_score = predictor.predict_dropout(
        student["attendance_percentage"], student["current_gpa"],
        student.get("fee_overdue_days", 0), student.get("engagement_score", 0.5),
    )
    fee_score = predictor.predict_fee_default(
        student.get("fee_overdue_days", 0), 0, 1,
    )

    return alerts.collect_alerts(
        alerts.may_fail_alert(sid, risk_score),
        alerts.attendance_alert(sid, student["attendance_percentage"]),
        alerts.dropout_alert(sid, dropout_score),
        alerts.fee_risk_alert(sid, fee_score),
    )


@router.get("/student/{student_id}", response_model=list[Alert])
def alerts_for_student(
    student_id: str,
    push_to_erp: bool = Query(False, description="Also save the alerts back into the ERP"),
):
    """
    Fetch a student from the ERP and return all early-warning alerts.

    Try `STU-1001` (a risky student) or `STU-1002` (a healthy student)
    while running in mock mode.
    """
    student = erp_client.get_student(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"Student '{student_id}' not found in ERP")

    raised = _evaluate_student(student)

    if push_to_erp:
        for alert in raised:
            erp_client.push_alert(alert)

    return raised
