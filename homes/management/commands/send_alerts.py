from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from homes.alerter import Alerter


class Command(BaseCommand):
    help = 'Sends emails for property matching saved user alerts'

    def handle(self, *args, **options):
        alerter = Alerter(
            subject='Property Alert',
            from_email=settings.DO_NOT_REPLY_EMAIL,
            template='emails/alerts.txt'
        )
        alerter.process()
