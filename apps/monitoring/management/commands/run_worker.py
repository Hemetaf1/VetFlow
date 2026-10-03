import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.clinic.models import ProcedureSession
from apps.monitoring.models import UnpredictedEvent


class Command(BaseCommand):
    help = "Extend overdue procedure sessions and record overrun events."

    def add_arguments(self, parser):
        parser.add_argument("--interval", type=int, default=30)
        parser.add_argument("--once", action="store_true")

    def handle(self, *args, **options):
        while True:
            now = timezone.now()
            overdue = ProcedureSession.objects.filter(
                is_complete=False, vet_confirmed_completion=False,
                starts_at__lte=now - timedelta(minutes=1),
            )
            for session in overdue:
                if session.planned_end <= now:
                    session.planned_minutes += 15
                    session.save(update_fields=["planned_minutes"])
                    UnpredictedEvent.objects.create(
                        category=UnpredictedEvent.Category.OVERRUN,
                        description="Session automatically extended by 15 minutes.",
                        related_session=session,
                    )
            if options["once"]:
                break
            time.sleep(max(options["interval"], 1))