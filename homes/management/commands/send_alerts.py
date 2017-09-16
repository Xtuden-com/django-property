from django.core.management.base import BaseCommand, CommandError
from homes.alerter import Alerter


class Command(BaseCommand):
    help = 'Sends emails for property matching saved user alerts'

    def handle(self, *args, **options):
        alerter = Alerter()
        alerter.process()
