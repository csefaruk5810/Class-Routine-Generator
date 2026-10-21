# Automated Class Routine Generator

Initial scaffold for a constraint-based university routine generator using Django, Django REST Framework, PostgreSQL, and an OR-Tools-oriented scheduler module.

## Current milestone

This repository currently includes:

- Backend project scaffold
- Normalized academic and scheduling data models
- Scheduler domain package
- JSON importer scaffolding aligned to the provided routine files
- Documentation skeleton
- Frontend placeholder shell

## Project structure

- `backend/`: Django backend and scheduling engine
- `frontend/`: React/Vite placeholder shell
- `docs/`: architecture and domain documentation
- `docker-compose.yml`: development services

## Next steps

1. Create and activate a Python virtual environment.
2. Install backend dependencies from `backend/pyproject.toml`.
3. Run migrations.
4. Implement serializers, APIs, importer services, and solver constraints.

