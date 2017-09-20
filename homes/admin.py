from mapwidgets.widgets import GooglePointFieldWidget

from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

from homes.models import Block, SEO, SearchPrice, Branch, PropertyTenure, PropertyType, Alert, MediaType


class SearchPriceAdmin(admin.ModelAdmin):
    fields = ('type', 'label', 'price')


class BranchAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    fieldsets = (
        (_('General'), {
            'fields': ['name', 'slug', 'status']
        }),
        (_('Address'), {
            'fields': ['address_1', 'address_2', 'address_3', 'town_city', 'county', 'postcode'],
        }),
        (_('Geographic'), {
            'fields': ['location']
        }),
        (_('Contact'), {
            'fields': ['telephone', 'email']
        }),
        (_('Details'), {
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


class SEOAdmin(admin.ModelAdmin):
    list_display = ('url', 'title')


admin.site.register(SearchPrice, SearchPriceAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(PropertyTenure, PropertyTenureAdmin)
admin.site.register(MediaType, MediaTypeAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(SEO, SEOAdmin)
admin.site.register(Alert)
