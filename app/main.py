"""
Application entry point.

This creates the FastAPI app, sets up the auto-generated documentation,
and plugs in our route modules. Run it with:

    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from app.config import settings
from app.api.routes import predictions, alerts

app = FastAPI(
    title=settings.app_name,
    description=(
        "Early Warning System & Prediction API for the Student ERP.\n\n"
        "Provides risk/dropout/GPA/fee/admission predictions and generates "
        "early-warning alerts that integrate with the ERP."
    ),
    version="1.0.0",
)


# ── Health-check endpoints (handy to confirm the server is alive) ────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": settings.app_name}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "erp_mock_mode": settings.erp_mock_mode}


# ── Plug in the feature routes ──────────────────────────────────────
app.include_router(predictions.router)
app.include_router(alerts.router)
