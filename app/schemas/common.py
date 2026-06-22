"""
Shared data shapes used by many endpoints.

A "schema" describes what data looks like. FastAPI uses these to:
  1. Validate incoming requests (reject bad data automatically)
  2. Document the API (the /docs page is built from these)
"""

from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """How serious a situation is. Used everywhere for consistency."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    """The four early-warning alert categories from the task."""
    MAY_FAIL = "may_fail"
    LOW_ATTENDANCE = "low_attendance"
    FEE_PAYMENT_RISK = "fee_payment_risk"
    DROPOUT_RISK = "dropout_risk"


class Alert(BaseModel):
    """One early-warning alert about a single student."""
    student_id: str = Field(..., examples=["STU-1001"])
    type: AlertType
    severity: RiskLevel
    message: str = Field(..., examples=["Attendance is 55%, below the 75% requirement."])
    score: float = Field(..., ge=0, le=1, description="Risk score between 0 and 1")
