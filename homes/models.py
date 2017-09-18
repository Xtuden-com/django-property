# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.gis.db import models
from django.contrib.auth.models import User

from picklefield.fields import PickledObjectField
from model_utils.managers import QueryManager

from .behaviours import Publishable, Expireable, Timestampable, Orderable


class SearchPrice(models.Model):
    SEARCH_PRICE_LETTING = 1
    SEARCH_PRICE_SALE = 2
    SEARCH_PRICE_TYPES = (
        (SEARCH_PRICE_LETTING, 'Letting'),
        (SEARCH_PRICE_SALE, 'Sale')
    )
    type = models.IntegerField(choices=SEARCH_PRICE_TYPES)
    label = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return self.label

    class Meta:
        pass


class PropertyType(Publishable, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Branch(Publishable, Timestampable, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    address_3 = models.CharField(max_length=100, blank=True, null=True)
    town_city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    location = models.PointField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    details = models.TextField()
    opening_hours = models.TextField()
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "branch"
        verbose_name_plural = "branches"


class Property(Publishable, Expireable, Timestampable, models.Model):
    branch = models.ForeignKey(Branch)
    property_type = models.ForeignKey(PropertyType)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    address_3 = models.CharField(max_length=100, blank=True, null=True)
    town_city = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    location = models.PointField()
    display_address = models.CharField(max_length=200, blank=True, null=True)
    bedrooms = models.IntegerField()
    en_suites = models.IntegerField()
    receptions = models.IntegerField()
    details = models.TextField()
    summary = models.TextField(max_length=2000)
    garden = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    retirement = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['-updated_at']
        verbose_name = "property"
        verbose_name_plural = "properties"


class Feature(Timestampable, Orderable, models.Model):
    text = models.CharField(max_length=200)
    objects = models.Manager()

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Picture(Publishable, Timestampable, Orderable, models.Model):
    caption = models.CharField(max_length=200)
    attachment = models.ImageField(upload_to='pictures/')
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.caption

    class Meta:
        abstract = True


class MediaType(Publishable, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Media(Publishable, models.Model):
    media_type = models.ForeignKey(MediaType)
    description = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='media/')
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.description

    class Meta:
        abstract = True


class PropertyTenure(Publishable, models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    objects = models.Manager()
    active = QueryManager(status=Publishable.STATUS_CHOICE_ACTIVE)
    inactive = QueryManager(status=Publishable.STATUS_CHOICE_INACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Contact(Timestampable, models.Model):
    more_details = models.BooleanField(default=True)
    view_property = models.BooleanField(default=True)
    title = models.CharField(max_length=10)
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    message = models.CharField(max_length=2000)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s (%s)" % (self.forename, self.surname, self.email)

    class Meta:
        abstract = True


class Note(Timestampable, models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class Favourite(Timestampable, models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username

    class Meta:
        abstract = True


class Alert(Timestampable, models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=40)
    criteria = PickledObjectField()

    def __str__(self):
        return self.user.username

    class Meta:
        pass


class Block(Publishable, models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        pass


class SEO(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    title = models.CharField(max_length=100)
    keywords = models.CharField(max_length=500)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.url

    class Meta:
        pass