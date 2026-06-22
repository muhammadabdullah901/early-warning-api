"""
Business logic for predictions.

The routes (waiters) just hand the request to these functions. Each function:
  1. asks the predictor (model) for a score,
  2. asks the alert_service for any warnings,
  3. builds and returns the final response object.

Keeping this logic OUT of the route files makes everything easy to test
and easy to read.
"""

from app.models.predictor import predictor
from app.services import alert_service as alerts
from app.schemas.prediction import (
    StudentRiskRequest, StudentRiskResponse,
    DropoutRequest, DropoutResponse,
    GpaRequest, GpaResponse,
    FeeDefaultRequest, FeeDefaultResponse,
    AdmissionsRequest, AdmissionsResponse,
    RecommendationsRequest, RecommendationsResponse,
)


def _ratio(part: int, whole: int) -> float:
    """Safe division: returns 0 instead of crashing when whole is 0."""
    return part / whole if whole else 0.0


# ── 1) Student risk ─────────────────────────────────────────────────
def predict_student_risk(req: StudentRiskRequest) -> StudentRiskResponse:
    submitted_ratio = _ratio(req.assignments_submitted, req.assignments_total)
    score = predictor.predict_student_risk(
        req.attendance_percentage, req.current_gpa, submitted_ratio, req.backlogs
    )
    raised = alerts.collect_alerts(
        alerts.may_fail_alert(req.student_id, score),
        alerts.attendance_alert(req.student_id, req.attendance_percentage),
    )
    return StudentRiskResponse(
        student_id=req.student_id,
        risk_score=score,
        risk_level=alerts.score_to_risk_level(score),
        may_fail=score >= 0.50,
        alerts=raised,
    )


# ── 2) Dropout ──────────────────────────────────────────────────────
def predict_dropout(req: DropoutRequest) -> DropoutResponse:
    score = predictor.predict_dropout(
        req.attendance_percentage, req.current_gpa,
        req.fee_overdue_days, req.engagement_score,
    )
    raised = alerts.collect_alerts(
        alerts.dropout_alert(req.student_id, score),
        alerts.attendance_alert(req.student_id, req.attendance_percentage),
    )
    return DropoutResponse(
        student_id=req.student_id,
        dropout_probability=score,
        risk_level=alerts.score_to_risk_level(score),
        alerts=raised,
    )


# ── 3) GPA ──────────────────────────────────────────────────────────
def predict_gpa(req: GpaRequest) -> GpaResponse:
    submitted_ratio = _ratio(req.assignments_submitted, req.assignments_total)
    predicted, confidence = predictor.predict_gpa(
        req.previous_gpa, req.attendance_percentage,
        req.study_hours_per_week, submitted_ratio,
    )
    return GpaResponse(
        student_id=req.student_id,
        predicted_gpa=predicted,
        confidence=confidence,
    )


# ── 4) Fee default ──────────────────────────────────────────────────
def predict_fee_default(req: FeeDefaultRequest) -> FeeDefaultResponse:
    score = predictor.predict_fee_default(
        req.days_overdue, req.previous_late_payments, req.total_payments
    )
    raised = alerts.collect_alerts(
        alerts.fee_risk_alert(req.student_id, score),
    )
    return FeeDefaultResponse(
        student_id=req.student_id,
        default_probability=score,
        risk_level=alerts.score_to_risk_level(score),
        alerts=raised,
    )


# ── 5) Admissions ───────────────────────────────────────────────────
def predict_admissions(req: AdmissionsRequest) -> AdmissionsResponse:
    score = predictor.predict_admission(
        req.entry_test_score, req.previous_grade_percentage, req.interview_score
    )
    if score >= 0.70:
        decision = "admit"
    elif score >= 0.50:
        decision = "waitlist"
    else:
        decision = "reject"
    return AdmissionsResponse(
        applicant_id=req.applicant_id,
        admission_probability=score,
        decision=decision,
    )


# ── 6) Recommendations ──────────────────────────────────────────────
def generate_recommendations(req: RecommendationsRequest) -> RecommendationsResponse:
    tips: list[str] = []

    if req.attendance_percentage < 75:
        tips.append("Improve attendance to at least 75% to stay eligible for exams.")
    if req.current_gpa < 2.5:
        tips.append("Meet your academic advisor to build a GPA recovery plan.")
    for subject in req.weak_subjects:
        tips.append(f"Attend extra tutoring / practice sessions for {subject}.")
    if not tips:
        tips.append("You are on track. Keep up the good work!")

    return RecommendationsResponse(student_id=req.student_id, recommendations=tips)
