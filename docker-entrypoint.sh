#!/bin/sh
# Commands expected by monedasegura-infra/docker-compose.yml:
#   serve (default) - run the API on port 8000
#   seed            - run the one-off seed job
set -e
case "${1:-serve}" in
  serve) exec uvicorn app.main:app --host 0.0.0.0 --port 8000 ;;
  seed)  exec python -m app.seed ;;
  *)     exec "$@" ;;
esac
