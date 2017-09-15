# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from django.contrib.gis.db import models

from homes.models import *

from .querysets import SaleQuerySet


class Sale(Property):
    QUALIFIER_CHOICE_OIRO = 1
    QUALIFIER_CHOICE_OFFERS_IN_EXCESS = 2
    QUALIFIER_CHOICE_FROM = 3
    QUALIFIER_CHOICE_POA = 4
    QUALIFIER_CHOICES = (
        (QUALIFIER_CHOICE_OIRO, _('OIRO')),
        (QUALIFIER_CHOICE_OFFERS_IN_EXCESS, _('Offers in Excess of')),
        (QUALIFIER_CHOICE_FROM, _('Price from')),
        (QUALIFIER_CHOICE_POA, _('Price on Application'))
    )
    price = models.DecimalField(max_digits=11, decimal_places=2)
    qualifier = models.IntegerField(choices=QUALIFIER_CHOICES)
    new_home = models.BooleanField(default=False)
    shared_ownership = models.BooleanField(default=False)
    auction = models.BooleanField(default=False)
    property_tenure = models.ForeignKey(PropertyTenure)
    filtered = SaleQuerySet.as_manager()

    class Meta:
        verbose_name = "property"
        verbose_name_plural = "properties"


class SaleFeature(Feature):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "feature"
        verbose_name_plural = "features"


class SalePicture(Picture):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "picture"
        verbose_name_plural = "pictures"


class SaleMedia(Media):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "media item"
        verbose_name_plural = "media items"


class SaleContact(Contact):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"


class SaleNote(Note):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "note"
        verbose_name_plural = "notes"


class SaleFavourite(Favourite):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = "favourite"
        verbose_name_plural = "favourites"