# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.gis.db import models

from mapwidgets.widgets import GooglePointFieldWidget

from homes.models import Block, SearchPrice, Branch, PropertyTenure, PropertyType, Alert, MediaType


class SearchPriceAdmin(admin.ModelAdmin):
    fields = ('type', 'label', 'price')


class BranchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    fieldsets = (
        ('General', {
            'fields': ['name', 'slug', 'status']
        }),
        ('Address', {
            'fields': ['address_1', 'address_2', 'address_3', 'town_city', 'county', 'postcode'],
        }),
        ('Geographic', {
            'fields': ['location']
        }),
        ('Contact', {
            'fields': ['telephone', 'email']
        }),
        ('Details', {
            'fields': ['details', 'opening_hours']
        })
    )
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        css = {
            'all':['build/css/admin/override/map.min.css']
        }


class PropertyTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'status')


class MediaTypeAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'status')


class PropertyTenureAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'status')


class BlockAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', 'slug')
    fields = ('name','slug','content','status')

admin.site.register(SearchPrice, SearchPriceAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(PropertyTenure, PropertyTenureAdmin)
admin.site.register(MediaType, MediaTypeAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Alert)
