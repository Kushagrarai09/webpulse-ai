# WebPulse AI — Website Behaviour & Conversion Intelligence

A full-stack MVP for ingesting website events and turning them into conversion analytics and actionable insights.

## Stack
- FastAPI, SQLAlchemy, Pydantic
- PostgreSQL (SQLite fallback for local development)
- Next.js App Router, TypeScript, Tailwind CSS, Recharts
- Docker Compose
- Python analytics and rule-based recommendations

> This is a portfolio MVP using synthetic/demo events. It does not contain real data from 30 million websites and is not production-ready for that scale.

## Quick start
1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. API docs: http://localhost:8000/docs
4. Dashboard: http://localhost:3000
5. Seed sample events: `docker compose exec api python /workspace/scripts/seed_demo.py`

## API endpoints
- `POST /api/v1/events`
- `POST /api/v1/events/batch`
- `GET /api/v1/analytics/overview?website_id=demo-store&days=30`
- `GET /api/v1/analytics/funnel?website_id=demo-store`
- `GET /api/v1/analytics/forms?website_id=demo-store`
- `GET /api/v1/analytics/email?website_id=demo-store`
- `GET /api/v1/analytics/plugins?website_id=demo-store`
- `GET /api/v1/insights?website_id=demo-store`

## Scaling path
FastAPI ingestion -> Kafka -> stream processors -> ClickHouse, with Redis caching and object storage for raw events.

## Tests
From `apps/api`, run `pytest -q`.

See the repository folders for API services, frontend components, infrastructure, tests, and demo-data scripts.