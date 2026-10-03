# VetFlow Workspace Guidance

- Keep workflow transitions in `apps/workflow/services.py` and permission decisions in `apps/core/services.py`.
- Validate metadata-backed field paths before building ORM queries; deny access when configuration is invalid.
- Keep fictional sample data only. Never add real client or patient information.
- Run `python manage.py check` and `python manage.py test apps.core.tests apps.workflow.tests` after backend changes.
- Generate and commit schema migrations with `python manage.py makemigrations` when models change.
- PostgreSQL is used when `DB_HOST` is set; otherwise local development and tests use SQLite.