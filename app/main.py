"""HTTP entry point. Contract: monedasegura-infra/docs/api/scoring-api.yaml."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MonedaSegura scoring-api", version="1.0.0")


class Health(BaseModel):
    status: Literal["UP", "DEGRADED"]
    activeModel: str | None  # noqa: N815 - field name fixed by the contract


@app.get("/health", response_model=Health, tags=["health"])
def health() -> Health:
    # No model is trained yet, so the service is up but cannot score.
    return Health(status="DEGRADED", activeModel=None)
