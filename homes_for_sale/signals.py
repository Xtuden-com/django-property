from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from homes.emailer import Emailer
from .models import SaleContact


@receiver(post_save, sender=SaleContact)
def send_notification(sender, instance, created, **kwargs):
    if created:
        mailer = Emailer({
            'subject': 'Contact - Home For Sale',
            'recipient': [instance.property.branch.email],
            'from_email': settings.DO_NOT_REPLY_EMAIL,
            'reply_to': [instance.email],
            'data': {
                'property': instance.property.display_address,
                'title': instance.title,
                'forename': instance.forename,
                'surname': instance.surname,
                'message': instance.message,
                'telephone': instance.telephone,
                'email': instance.email,
                'country': instance.country,
                'postcode': instance.postcode,
                'details': instance.more_details,
                'viewing': instance.view_property
            },
            'templates': {
                'plain':'emails/notification.txt',
                'html': 'emails/notification.html'
            }
        })
        mailer.send()
