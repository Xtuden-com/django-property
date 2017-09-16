import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import LettingContact

logger = logging.getLogger('email')


@receiver(post_save, sender=LettingContact)
def send_notification(sender, **kwargs):
    logger.debug('I have been called')