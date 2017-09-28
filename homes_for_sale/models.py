from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.sites.models import Site

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

    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'slug':self.slug})

    def get_full_absolute_url(self):
        site = Site.objects.get_current()
        return '{}{}'.format(str(site.domain), self.get_absolute_url())

    class Meta:
        verbose_name = _('property')
        verbose_name_plural = _('properties')


class SaleFeature(Feature):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


class SalePicture(Picture):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')


class SaleMedia(Media):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('media item')
        verbose_name_plural = _('media items')


class SaleContact(Contact):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')


class SaleNote(Note):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')


class SaleFavourite(Favourite):
    property = models.ForeignKey(Sale)

    class Meta:
        verbose_name = _('favourite')
        verbose_name_plural = _('favourites')