# Testing Guide — Sample Data for Every Route

Yeh file har endpoint ke liye **4 ready-to-use test inputs** deti hai. Inhe
copy karke **Swagger `/docs`** ke "Try it out" box mein paste karo, ya niche
diye `curl` commands chala lo.

- **Live base URL:** `https://muhammadabdullah31808-early-warning-api.hf.space`
- **Local base URL:** `http://127.0.0.1:8000`

> Tip: niche `BASE` ko apni pasand ke URL se badal lo.

```bash
BASE="https://muhammadabdullah31808-early-warning-api.hf.space"
```

---

## 1) POST `/prediction/student-risk`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | High risk | `{"student_id":"STU-1001","attendance_percentage":45,"current_gpa":1.6,"assignments_submitted":2,"assignments_total":10,"backlogs":3}` |
| 2 | Medium risk | `{"student_id":"STU-1002","attendance_percentage":68,"current_gpa":2.4,"assignments_submitted":6,"assignments_total":10,"backlogs":1}` |
| 3 | Low risk | `{"student_id":"STU-1003","attendance_percentage":92,"current_gpa":3.7,"assignments_submitted":10,"assignments_total":10,"backlogs":0}` |
| 4 | Edge (no backlogs field) | `{"student_id":"STU-1004","attendance_percentage":75,"current_gpa":3.0,"assignments_submitted":8,"assignments_total":10}` |

```bash
curl -X POST "$BASE/prediction/student-risk" -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","attendance_percentage":45,"current_gpa":1.6,"assignments_submitted":2,"assignments_total":10,"backlogs":3}'
```

---

## 2) POST `/prediction/dropout`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | High dropout | `{"student_id":"STU-1001","attendance_percentage":40,"current_gpa":1.5,"fee_overdue_days":90,"engagement_score":0.2}` |
| 2 | Medium | `{"student_id":"STU-1002","attendance_percentage":65,"current_gpa":2.3,"fee_overdue_days":30,"engagement_score":0.5}` |
| 3 | Low | `{"student_id":"STU-1003","attendance_percentage":90,"current_gpa":3.6,"fee_overdue_days":0,"engagement_score":0.9}` |
| 4 | Edge (default fee days) | `{"student_id":"STU-1004","attendance_percentage":80,"current_gpa":3.1,"engagement_score":0.7}` |

```bash
curl -X POST "$BASE/prediction/dropout" -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","attendance_percentage":40,"current_gpa":1.5,"fee_overdue_days":90,"engagement_score":0.2}'
```

---

## 3) POST `/prediction/gpa`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | Strong student | `{"student_id":"STU-1001","previous_gpa":3.6,"attendance_percentage":95,"study_hours_per_week":20,"assignments_submitted":10,"assignments_total":10}` |
| 2 | Average | `{"student_id":"STU-1002","previous_gpa":2.8,"attendance_percentage":78,"study_hours_per_week":10,"assignments_submitted":7,"assignments_total":10}` |
| 3 | Weak | `{"student_id":"STU-1003","previous_gpa":1.9,"attendance_percentage":55,"study_hours_per_week":4,"assignments_submitted":3,"assignments_total":10}` |
| 4 | Edge (zero study hours) | `{"student_id":"STU-1004","previous_gpa":2.5,"attendance_percentage":70,"study_hours_per_week":0,"assignments_submitted":5,"assignments_total":10}` |

```bash
curl -X POST "$BASE/prediction/gpa" -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","previous_gpa":3.6,"attendance_percentage":95,"study_hours_per_week":20,"assignments_submitted":10,"assignments_total":10}'
```

---

## 4) POST `/prediction/fee-default`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | High default risk | `{"student_id":"STU-1001","outstanding_amount":120000,"days_overdue":90,"previous_late_payments":5,"total_payments":8}` |
| 2 | Medium | `{"student_id":"STU-1002","outstanding_amount":45000,"days_overdue":25,"previous_late_payments":2,"total_payments":10}` |
| 3 | Low | `{"student_id":"STU-1003","outstanding_amount":5000,"days_overdue":0,"previous_late_payments":0,"total_payments":12}` |
| 4 | Edge (defaults) | `{"student_id":"STU-1004","outstanding_amount":30000,"total_payments":6}` |

```bash
curl -X POST "$BASE/prediction/fee-default" -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","outstanding_amount":120000,"days_overdue":90,"previous_late_payments":5,"total_payments":8}'
```

---

## 5) POST `/prediction/admissions`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | Strong applicant (admit) | `{"applicant_id":"APP-2025-001","entry_test_score":92,"previous_grade_percentage":88,"interview_score":85}` |
| 2 | Borderline (waitlist) | `{"applicant_id":"APP-2025-002","entry_test_score":68,"previous_grade_percentage":70,"interview_score":60}` |
| 3 | Weak applicant (reject) | `{"applicant_id":"APP-2025-003","entry_test_score":40,"previous_grade_percentage":50,"interview_score":35}` |
| 4 | Edge (no interview) | `{"applicant_id":"APP-2025-004","entry_test_score":75,"previous_grade_percentage":80}` |

```bash
curl -X POST "$BASE/prediction/admissions" -H "Content-Type: application/json" \
  -d '{"applicant_id":"APP-2025-001","entry_test_score":92,"previous_grade_percentage":88,"interview_score":85}'
```

---

## 6) POST `/prediction/recommendations`

| # | Scenario | JSON body |
|---|----------|-----------|
| 1 | Weak in 2 subjects | `{"student_id":"STU-1001","attendance_percentage":55,"current_gpa":2.0,"weak_subjects":["Math","Physics"]}` |
| 2 | Low attendance | `{"student_id":"STU-1002","attendance_percentage":48,"current_gpa":2.6,"weak_subjects":["Chemistry"]}` |
| 3 | Good student | `{"student_id":"STU-1003","attendance_percentage":90,"current_gpa":3.6,"weak_subjects":[]}` |
| 4 | Edge (no weak subjects field) | `{"student_id":"STU-1004","attendance_percentage":72,"current_gpa":2.9}` |

```bash
curl -X POST "$BASE/prediction/recommendations" -H "Content-Type: application/json" \
  -d '{"student_id":"STU-1001","attendance_percentage":55,"current_gpa":2.0,"weak_subjects":["Math","Physics"]}'
```

---

## 7) GET `/alerts/student/{student_id}` (Early Warning System)

Yeh route mock ERP se student ka record uthata hai aur saare alerts deta hai.
4 ready students mojood hain:

| # | Student ID | Profile |
|---|-----------|---------|
| 1 | `STU-1001` | Ali Khan — at risk (low attendance) |
| 2 | `STU-1002` | Sara Ahmed — healthy (koi alert nahi) |
| 3 | `STU-1003` | Bilal Hussain — medium + fee overdue |
| 4 | `STU-1004` | Hina Raza — high dropout risk |

```bash
curl "$BASE/alerts/student/STU-1001"
curl "$BASE/alerts/student/STU-1004"
```

> Jo student ID list mein nahi (jaise `STU-9999`) us par `404 Not Found` aata hai.
