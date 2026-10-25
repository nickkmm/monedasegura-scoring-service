# monedasegura-scoring-service

Fraud scoring and model training for MonedaSegura, plus the Sparkov seed job.

**Stack:** FastAPI · Python 3.12 · LightGBM · **Owners:** Nicholas, Laura (supervised by Nicolás) · **Status:** skeleton

Part of MonedaSegura (Universidad Icesi + Lovelytics). The shared specification — context, MVP plan, data model, architecture and API contracts — lives in [`monedasegura-infra`](https://github.com/nickkmm/monedasegura-infra), cloned next to this repo inside a `SecureMoney/` workspace folder. Contract: `../monedasegura-infra/docs/api/scoring-api.yaml`.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check . && ruff format --check . && pytest
uvicorn app.main:app --reload --port 8000   # http://localhost:8000/health
docker build -t monedasegura/scoring-service:dev .
```

The whole stack (Postgres, Redis, Kafka and the three services) runs from `../monedasegura-infra` with `docker compose --profile apps up -d --build`.

## Contributing

Branch from `develop` (`feature/…`, `fix/…`, `docs/…`) and open a PR against `develop`; `main` only receives `develop → main` from Nicolás. CI must pass. Everything is in English; only user-facing app text is in Spanish. Agent instructions: [`AGENTS.md`](AGENTS.md).
