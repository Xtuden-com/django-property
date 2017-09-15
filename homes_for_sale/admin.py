# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.gis.db import models

from mapwidgets.widgets import GooglePointFieldWidget

from homes_for_sale.models import *


class SaleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_filter = ['branch__name', 'property_type__name', 'property_tenure__name', 'status']
    list_display = ['title', 'address_1', 'town_city', 'postcode', 'status']
    search_fields = ['title', 'address_1', 'town_city', 'postcode']
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    fieldsets = (
        ('General', {
            'fields': ['title', 'slug', 'status']
        }),
        ('Address', {
            'fields': ['address_1', 'address_2', 'address_3', 'town_city', 'county', 'postcode', 'display_address'],
        }),
        ('Geographic', {
            'fields': ['location']
        }),
        ('Categorisation', {
            'fields': ['branch', 'property_tenure', 'property_type', 'bedrooms', 'en_suites', 'receptions', 'garden', 'parking', 'retirement', 'new_home', 'shared_ownership', 'auction']
        }),
        ('Detail', {
            'fields': ['details', 'summary']
        }),
        ('Price', {
            'fields': ['price', 'qualifier']
        }),
        ('Date', {
            'fields': ['expires_at']
        }),
    )

    class Media:
        css = {
            'all':['build/css/admin/override/map.min.css']
        }


class SaleFeatureAdmin(admin.ModelAdmin):
    fields = ('property','text','display_order')
    list_display = ['property','text']


class SaleContactAdmin(admin.ModelAdmin):
    fields = ('property','title','forename','surname','message','telephone','email','country','postcode','more_details','view_property')


class SalePictureAdmin(admin.ModelAdmin):
    fields = ('property','caption','attachment','display_order','status')
    list_display = ['property','caption']


class SaleMediaAdmin(admin.ModelAdmin):
    fields = ('property','media_type','description','attachment','status')
    list_display = ['property', 'media_type','description','status']


class SaleNoteAdmin(admin.ModelAdmin):
    fields = ('property','text')
    list_display = ['property']


admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleFeature, SaleFeatureAdmin)
admin.site.register(SalePicture, SalePictureAdmin)
admin.site.register(SaleMedia, SaleMediaAdmin)
admin.site.register(SaleContact, SaleContactAdmin)
admin.site.register(SaleNote, SaleNoteAdmin)
