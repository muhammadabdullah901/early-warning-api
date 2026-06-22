"""
Request (input) and Response (output) shapes for every prediction endpoint.

Each endpoint gets its own Request and Response model so the API is
self-documenting and the inputs are validated automatically.
"""

from pydantic import BaseModel, Field
from app.schemas.common import RiskLevel, Alert


# ─────────────────────────────────────────────────────────────────────
# 1) STUDENT RISK  →  POST /prediction/student-risk
# ─────────────────────────────────────────────────────────────────────
class StudentRiskRequest(BaseModel):
    student_id: str = Field(..., examples=["STU-1001"])
    attendance_percentage: float = Field(..., ge=0, le=100, examples=[62])
    current_gpa: float = Field(..., ge=0, le=4, examples=[2.1])
    assignments_submitted: int = Field(..., ge=0, examples=[6])
    assignments_total: int = Field(..., ge=0, examples=[10])
    backlogs: int = Field(0, ge=0, description="Number of failed/pending subjects", examples=[2])


class StudentRiskResponse(BaseModel):
    student_id: str
    risk_score: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    may_fail: bool
    alerts: list[Alert] = []


# ─────────────────────────────────────────────────────────────────────
# 2) DROPOUT  →  POST /prediction/dropout
# ─────────────────────────────────────────────────────────────────────
class DropoutRequest(BaseModel):
    student_id: str = Field(..., examples=["STU-1001"])
    attendance_percentage: float = Field(..., ge=0, le=100, examples=[55])
    current_gpa: float = Field(..., ge=0, le=4, examples=[1.8])
    fee_overdue_days: int = Field(0, ge=0, examples=[30])
    engagement_score: float = Field(..., ge=0, le=1, description="Class participation 0-1", examples=[0.3])


class DropoutResponse(BaseModel):
    student_id: str
    dropout_probability: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    alerts: list[Alert] = []


# ─────────────────────────────────────────────────────────────────────
# 3) GPA PREDICTION  →  POST /prediction/gpa
# ─────────────────────────────────────────────────────────────────────
class GpaRequest(BaseModel):
    student_id: str = Field(..., examples=["STU-1001"])
    previous_gpa: float = Field(..., ge=0, le=4, examples=[3.0])
    attendance_percentage: float = Field(..., ge=0, le=100, examples=[85])
    study_hours_per_week: float = Field(..., ge=0, examples=[12])
    assignments_submitted: int = Field(..., ge=0, examples=[9])
    assignments_total: int = Field(..., ge=0, examples=[10])


class GpaResponse(BaseModel):
    student_id: str
    predicted_gpa: float = Field(..., ge=0, le=4)
    confidence: float = Field(..., ge=0, le=1)


# ─────────────────────────────────────────────────────────────────────
# 4) FEE DEFAULT  →  POST /prediction/fee-default
# ─────────────────────────────────────────────────────────────────────
class FeeDefaultRequest(BaseModel):
    student_id: str = Field(..., examples=["STU-1001"])
    outstanding_amount: float = Field(..., ge=0, examples=[45000])
    days_overdue: int = Field(0, ge=0, examples=[20])
    previous_late_payments: int = Field(0, ge=0, examples=[3])
    total_payments: int = Field(..., ge=1, description="Total payments made so far", examples=[8])


class FeeDefaultResponse(BaseModel):
    student_id: str
    default_probability: float = Field(..., ge=0, le=1)
    risk_level: RiskLevel
    alerts: list[Alert] = []


# ─────────────────────────────────────────────────────────────────────
# 5) ADMISSIONS  →  POST /prediction/admissions
# ─────────────────────────────────────────────────────────────────────
class AdmissionsRequest(BaseModel):
    applicant_id: str = Field(..., examples=["APP-2025-077"])
    entry_test_score: float = Field(..., ge=0, le=100, examples=[78])
    previous_grade_percentage: float = Field(..., ge=0, le=100, examples=[82])
    interview_score: float = Field(0, ge=0, le=100, examples=[70])


class AdmissionsResponse(BaseModel):
    applicant_id: str
    admission_probability: float = Field(..., ge=0, le=1)
    decision: str = Field(..., description="admit / waitlist / reject")


# ─────────────────────────────────────────────────────────────────────
# 6) RECOMMENDATIONS  →  POST /prediction/recommendations
# ─────────────────────────────────────────────────────────────────────
class RecommendationsRequest(BaseModel):
    student_id: str = Field(..., examples=["STU-1001"])
    attendance_percentage: float = Field(..., ge=0, le=100, examples=[60])
    current_gpa: float = Field(..., ge=0, le=4, examples=[2.2])
    weak_subjects: list[str] = Field(default_factory=list, examples=[["Math", "Physics"]])


class RecommendationsResponse(BaseModel):
    student_id: str
    recommendations: list[str]
