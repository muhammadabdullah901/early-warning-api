"""
The Early Warning System logic.

Given a student's numbers, this decides WHICH alerts to raise and how
serious each one is. These threshold rules are easy to read and easy to
tweak with your team (e.g. change 75 to 80 for the attendance rule).
"""

from app.schemas.common import Alert, AlertType, RiskLevel


def score_to_risk_level(score: float) -> RiskLevel:
    """Turn a 0-1 score into a human-friendly risk level."""
    if score >= 0.80:
        return RiskLevel.CRITICAL
    if score >= 0.60:
        return RiskLevel.HIGH
    if score >= 0.30:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


# ── Individual alert rules ──────────────────────────────────────────

def attendance_alert(student_id: str, attendance: float) -> Alert | None:
    """Raise an alert if attendance is below the 75% requirement."""
    if attendance >= 75:
        return None
    score = round((75 - attendance) / 75, 3)  # how far below the line
    return Alert(
        student_id=student_id,
        type=AlertType.LOW_ATTENDANCE,
        severity=score_to_risk_level(score + 0.3),  # attendance issues are serious
        message=f"Attendance is {attendance:.0f}%, below the required 75%.",
        score=min(score + 0.3, 1.0),
    )


def may_fail_alert(student_id: str, risk_score: float) -> Alert | None:
    """Raise an alert if the overall academic risk is medium or higher."""
    if risk_score < 0.50:
        return None
    return Alert(
        student_id=student_id,
        type=AlertType.MAY_FAIL,
        severity=score_to_risk_level(risk_score),
        message=f"High academic risk (score {risk_score:.2f}). Student may fail.",
        score=risk_score,
    )


def fee_risk_alert(student_id: str, default_probability: float) -> Alert | None:
    """Raise an alert if the chance of fee default is medium or higher."""
    if default_probability < 0.50:
        return None
    return Alert(
        student_id=student_id,
        type=AlertType.FEE_PAYMENT_RISK,
        severity=score_to_risk_level(default_probability),
        message=f"Fee default risk is {default_probability:.0%}.",
        score=default_probability,
    )


def dropout_alert(student_id: str, dropout_probability: float) -> Alert | None:
    """Raise an alert if the chance of dropping out is medium or higher."""
    if dropout_probability < 0.50:
        return None
    return Alert(
        student_id=student_id,
        type=AlertType.DROPOUT_RISK,
        severity=score_to_risk_level(dropout_probability),
        message=f"Dropout risk is {dropout_probability:.0%}.",
        score=dropout_probability,
    )


def collect_alerts(*alerts: Alert | None) -> list[Alert]:
    """Drop the None values and keep only the real alerts."""
    return [a for a in alerts if a is not None]
