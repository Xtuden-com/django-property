from django.contrib.gis.db import models
from django.utils.translation import ugettext as _


class Publishable(models.Model):
    STATUS_CHOICE_INACTIVE = 0
    STATUS_CHOICE_ACTIVE = 1
    STATUS_CHOICES = (
        (STATUS_CHOICE_INACTIVE, _('Unpublished')),
        (STATUS_CHOICE_ACTIVE, _('Published')),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)

    class Meta:
        abstract = True


class Expireable(models.Model):
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Orderable(models.Model):
    display_order = models.IntegerField()

    class Meta:
        abstract = True
