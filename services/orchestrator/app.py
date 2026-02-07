from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import load_settings
from .openclaw_client import OpenClawError, run_openclaw


app = FastAPI(title="BioFi-Nexus Orchestrator")
settings = load_settings()


class PlanRequest(BaseModel):
    message: str = Field(..., min_length=1)
    thinking: str | None = None


class PlanResponse(BaseModel):
    provider: str
    response: str


@app.post("/api/v1/assistant/plan", response_model=PlanResponse)
def plan(request: PlanRequest) -> PlanResponse:
    if not settings.openclaw_enabled:
        raise HTTPException(
            status_code=503,
            detail="OpenClaw integration is disabled. Set OPENCLAW_ENABLED=true to enable.",
        )

    thinking = request.thinking or settings.openclaw_thinking

    try:
        response = run_openclaw(request.message, thinking, settings)
    except OpenClawError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return PlanResponse(provider="openclaw", response=response)
