"""
The 6 prediction endpoints required by the task.

Notice how SHORT each function is. The route's only job is to receive the
request and hand it to the service. All the real work lives in the services.
This is what keeps the code clean and testable.
"""

from fastapi import APIRouter
from app.services import prediction_service as service
from app.schemas.prediction import (
    StudentRiskRequest, StudentRiskResponse,
    DropoutRequest, DropoutResponse,
    GpaRequest, GpaResponse,
    FeeDefaultRequest, FeeDefaultResponse,
    AdmissionsRequest, AdmissionsResponse,
    RecommendationsRequest, RecommendationsResponse,
)

# All routes here start with /prediction and are grouped under "Predictions"
# in the auto-generated docs.
router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post("/student-risk", response_model=StudentRiskResponse)
def student_risk(request: StudentRiskRequest):
    """Predict whether a student is at academic risk / may fail."""
    return service.predict_student_risk(request)


@router.post("/dropout", response_model=DropoutResponse)
def dropout(request: DropoutRequest):
    """Predict the probability that a student drops out."""
    return service.predict_dropout(request)


@router.post("/gpa", response_model=GpaResponse)
def gpa(request: GpaRequest):
    """Predict a student's future GPA."""
    return service.predict_gpa(request)


@router.post("/fee-default", response_model=FeeDefaultResponse)
def fee_default(request: FeeDefaultRequest):
    """Predict the probability that a student defaults on fee payment."""
    return service.predict_fee_default(request)


@router.post("/admissions", response_model=AdmissionsResponse)
def admissions(request: AdmissionsRequest):
    """Predict whether an applicant should be admitted."""
    return service.predict_admissions(request)


@router.post("/recommendations", response_model=RecommendationsResponse)
def recommendations(request: RecommendationsRequest):
    """Generate personalised recommendations for a student."""
    return service.generate_recommendations(request)
