# AGENTS.md — monedasegura-scoring-service

Instructions for any coding agent (Claude Code, Antigravity, others) working in this repo.

## What this repo is
The **scoring-service** of MonedaSegura (Python 3.12, FastAPI, LightGBM): it returns the fraud probability of one transaction (`POST /score`), trains candidate models on labeled rows (`POST /retrain`), stores model files and serves the version the decision-service tells it to (`PUT /active-model`). It also owns the **seed job** that downloads the Sparkov dataset, colombianizes it and loads it into Postgres.

Owners: Nicholas, Laura (supervised by Nicolás). Status: **skeleton** — `/health` and the seed entry point exist; the rest starts once the data model (ERD) is approved.

## Read first (shared context)
The shared specification lives in the sibling repo `../monedasegura-infra/docs/`. Read it; never copy it here.

| File | Why |
|---|---|
| `CONTEXT.md`, `MVP_PLAN.md` | the challenge and the MVP scope |
| `api/scoring-api.yaml` | **the contract this service implements** |
| `features.md` | the exact feature vector (names, types, defaults) the model consumes |
| `data.md` | the Sparkov dataset, its limitations and the colombianization the seed job must do |
| `model.md` | the tables the seed job writes into, and the retraining quality gate (§8) |

If the code and those documents disagree, the documents win: change them first with a PR against `monedasegura-infra`, then the code.

## Language policy
- **Everything is in English**: code, identifiers, comments, logs, error messages, docs, notebooks, commit messages, PR titles and descriptions.
- The only Spanish in the system is user-facing text in the Flutter app.

## Rules for this repo
- Implement the contract exactly: paths, status codes, field names and RFC 9457 errors.
- **Never use `scenario` or `source` as features.** `scenario` is the answer: it is only a label.
- The feature vector is exactly `Features` in `scoring-api.yaml` / `docs/features.md`; adding a feature is a PR against `monedasegura-infra` first.
- `/score` is on the critical path: keep the model loaded in memory; target p99 under 50 ms; return `503` when no model is loaded so the decision-service degrades to rules.
- `/retrain` never activates a model; the decision-service decides after its quality gate.
- Measure with PR-AUC, precision and recall — never accuracy (fraud is ~0.5 % of rows).
- Use a fixed random seed for sampling and training so results are reproducible.
- The dataset is never committed (no CSVs, Parquet or model files in git). Model files live in `MODEL_DIR`; downloads in `/data`.
- Every request must carry `X-Service-Token` (except `/health`); the token comes from the environment.
- Do not modify the other repos from here.

## Commands
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
ruff check . && ruff format --check .   # lint and format
pytest                                   # tests
uvicorn app.main:app --reload --port 8000
docker build -t monedasegura/scoring-service:dev .
docker run --rm monedasegura/scoring-service:dev seed   # seed job entry point
```
The image's entry point accepts `serve` (default) and `seed`, as expected by `../monedasegura-infra/docker-compose.yml`.

## Branches and commits
- Never push to `develop` or `main`. Create `feature/<task>`, `fix/<task>` or `docs/<task>` and open a PR against `develop`.
- `develop → main` is opened and merged only by Nicolás.
- CI (`.github/workflows/ci.yml`) must pass before merging.
- One topic per PR; commit messages in English, imperative mood.

## Skills
Repo-specific skills go in `.agents/skills/<name>/SKILL.md` (`.claude/skills` is a symlink to it), so they stay versioned with the code.
