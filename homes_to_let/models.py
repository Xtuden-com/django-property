# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from homes.models import *
from .querysets import LettingQuerySet


class Letting(Property):
    RENTAL_PERIOD_WEEKLY = 1
    RENTAL_PERIOD_MONTHLY = 2
    RENTAL_PERIOD_ANNUALLY = 3
    RENTAL_PERIOD_CHOICES = (
        (RENTAL_PERIOD_WEEKLY, _('Weekly')),
        (RENTAL_PERIOD_MONTHLY, _('Monthly')),
        (RENTAL_PERIOD_ANNUALLY, _('Annually'))
    )
    TYPE_OF_LET_LONG_TERM = 1
    TYPE_OF_LET_SHORT_TERM = 2
    TYPE_OF_LET_STUDENT = 3
    TYPE_OF_LET_CHOICES = (
        (TYPE_OF_LET_LONG_TERM, _('Long Term')),
        (TYPE_OF_LET_SHORT_TERM, _('Short Term')),
        (TYPE_OF_LET_STUDENT, _('Student'))
    )
    rental = models.DecimalField(max_digits=11, decimal_places=2)
    period = models.IntegerField(choices=RENTAL_PERIOD_CHOICES)
    type_of_let = models.IntegerField(choices=TYPE_OF_LET_CHOICES)
    furnished = models.BooleanField(default=False)
    house_share = models.BooleanField(default=False)
    let_agreed = models.BooleanField(default=False)
    available_at = models.DateTimeField()
    filtered = LettingQuerySet.as_manager()

    class Meta:
        verbose_name = "property"
        verbose_name_plural = "properties"


class LettingFeature(Feature):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "feature"
        verbose_name_plural = "features"


class LettingPicture(Picture):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "picture"
        verbose_name_plural = "pictures"


class LettingMedia(Media):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "media item"
        verbose_name_plural = "media items"


class LettingContact(Contact):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"


class LettingNote(Note):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "note"
        verbose_name_plural = "notes"


class LettingFavourite(Favourite):
    property = models.ForeignKey(Letting)

    class Meta:
        verbose_name = "favourite"
        verbose_name_plural = "favourites"