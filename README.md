# VetFlow

VetFlow is a sample Django platform for workflow-driven scheduling in fictional multi-branch veterinary clinics. It includes visit and procedure records, database-configured visit transitions, an MPTT-backed organisation hierarchy, activity permissions, resource records, a clinic dashboard and a polling worker for session overruns.

This is a portfolio MVP, not a production-ready clinical or billing system. The workflow engine and admin screens are usable; scheduling optimization, row-filtered querysets, Jalali UI, billing, reports, and generic AJAX CRUD are not implemented yet. Do not use it with real patient or client data.

## Stack

- Python 3.12 and Django 5
- PostgreSQL 17 in Docker; SQLite for local development and tests
- django-mptt for the organisation tree
- pytest and pytest-django

## Run locally on Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Sign in through the Django admin login. The dashboard and admin are the current UI; create owners, patients, visits and workflow rules in `/admin/`.

## Docker Compose

Copy `.env.example` to `.env`, replace `SECRET_KEY` and database credentials, then run:

```sh
docker compose up --build
docker compose exec web python manage.py createsuperuser
```

The web app listens on port 8000. The worker polls for overdue sessions. Review and harden deployment settings, secret handling, HTTPS, backups and worker idempotency before production use.

## Configure visit transitions

In Django admin, add `StateNavigation` rows using model label `clinic.visit`, a source state and destination state from `Visit.State`. A condition may be empty, use `{ "type": "no_open_sessions" }`, or use a validated direct field equality/inequality condition. Transitions are executed through `WorkflowService` or `POST /workflow/visits/<id>/transition/` with `{"to_state":"CHECK_IN"}`. The endpoint requires login and an update permission; superusers are allowed.

`CRUDPermission` rows associate an activity and organisation node with CRUD flags, optional states, and a simple row condition. Menu items become visible when the user has read permission for the linked activity. Create an organisation node linked to a Django group before assigning permissions.

## Tests

```sh
pytest
pytest apps/workflow -k transition
```

## Environment

`SECRET_KEY`, `DEBUG`, and comma-separated `ALLOWED_HOSTS` configure Django. Setting `DB_HOST` selects PostgreSQL; without it, local SQLite is used. `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_PORT` configure the database.

## License

MIT. See [LICENSE](LICENSE).