"""
PLACEHOLDER for the real Machine Learning models.

Right now each method uses simple, explainable rules (weighted scoring) so
the whole API works today. When the data-science team gives you trained
models (e.g. a .pkl file), you only change the INSIDE of these methods,
for example:

    self.model = joblib.load("dropout_model.pkl")
    return float(self.model.predict_proba([[...features...]])[0][1])

As long as the inputs and outputs stay the same, NO other file needs to change.
That is the whole point of keeping the model behind this class.
"""


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Keep a number inside a range, e.g. never below 0 or above 1."""
    return max(low, min(high, value))


class RiskPredictor:
    # ---- 1) Will the student fail / how risky are they? (score 0-1) ----
    def predict_student_risk(self, attendance: float, gpa: float,
                             submitted_ratio: float, backlogs: int) -> float:
        score = (
            0.35 * (1 - attendance / 100) +     # low attendance -> higher risk
            0.35 * (1 - gpa / 4) +              # low gpa        -> higher risk
            0.20 * (1 - submitted_ratio) +     # missing work   -> higher risk
            0.10 * _clamp(backlogs / 5)        # backlogs       -> higher risk
        )
        return round(_clamp(score), 3)

    # ---- 2) Probability the student drops out (0-1) ----
    def predict_dropout(self, attendance: float, gpa: float,
                        fee_overdue_days: int, engagement: float) -> float:
        score = (
            0.30 * (1 - attendance / 100) +
            0.30 * (1 - gpa / 4) +
            0.20 * _clamp(fee_overdue_days / 60) +
            0.20 * (1 - engagement)
        )
        return round(_clamp(score), 3)

    # ---- 3) Predicted future GPA (0-4) + confidence ----
    def predict_gpa(self, previous_gpa: float, attendance: float,
                    study_hours: float, submitted_ratio: float) -> tuple[float, float]:
        # Start from past GPA, then nudge up/down based on current habits.
        effort = (
            0.5 * (attendance / 100) +
            0.3 * _clamp(study_hours / 20) +
            0.2 * submitted_ratio
        )  # 0 = poor habits, 1 = excellent habits
        predicted = previous_gpa + (effort - 0.5) * 1.0   # +/- up to 0.5 points
        confidence = round(0.6 + 0.4 * submitted_ratio, 3)
        return round(_clamp(predicted, 0, 4), 2), confidence

    # ---- 4) Probability the student defaults on fee (0-1) ----
    def predict_fee_default(self, days_overdue: int, previous_late: int,
                            total_payments: int) -> float:
        late_ratio = previous_late / total_payments if total_payments else 0
        score = (
            0.55 * _clamp(days_overdue / 45) +
            0.45 * _clamp(late_ratio)
        )
        return round(_clamp(score), 3)

    # ---- 5) Probability an applicant should be admitted (0-1) ----
    def predict_admission(self, entry_test: float, prev_grade: float,
                          interview: float) -> float:
        score = (
            0.45 * (entry_test / 100) +
            0.35 * (prev_grade / 100) +
            0.20 * (interview / 100)
        )
        return round(_clamp(score), 3)


# A single shared predictor instance for the whole app.
predictor = RiskPredictor()
