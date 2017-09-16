import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SaleContact

logger = logging.getLogger('email')


@receiver(post_save, sender=SaleContact)
def send_notification(sender, **kwargs):
    logger.debug('I have been called')