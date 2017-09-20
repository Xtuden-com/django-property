from django.contrib import admin
from django.utils.translation import ugettext as _

from mapwidgets.widgets import GooglePointFieldWidget

from homes_to_let.models import *


class LettingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_filter = ['branch__name', 'property_type__name', 'type_of_let', 'furnished', 'status']
    list_display = ['title', 'address_1', 'town_city', 'postcode', 'type_of_let', 'status']
    search_fields = ['title', 'address_1', 'town_city', 'postcode']
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
    fieldsets = (
        (_('General'), {
            'fields': ['title', 'slug', 'status']
        }),
        (_('Address'), {
            'fields': ['address_1', 'address_2', 'address_3', 'town_city', 'county', 'postcode', 'display_address'],
        }),
        (_('Geographic'), {
            'fields': ['location']
        }),
        (_('Categorisation'), {
            'fields': [
                'branch', 'type_of_let', 'property_type', 'bedrooms', 'en_suites', 'receptions', 'garden', 'parking',
                'retirement', 'furnished', 'house_share', 'let_agreed'
            ]
        }),
        (_('Detail'), {
            'fields': ['details', 'summary']
        }),
        (_('Price'), {
            'fields': ['rental', 'period']
        }),
        (_('Date'), {
            'fields': ['available_at', 'expires_at']
        }),
    )

    class Media:
        css = {
            'all':['build/css/admin/override/map.min.css']
        }


class LettingFeatureAdmin(admin.ModelAdmin):
    fields = ('property','text','display_order')
    list_display = ['property','text']
    

class LettingContactAdmin(admin.ModelAdmin):
    fields = (
        'property','title','forename','surname','message','telephone',
        'email','country','postcode','more_details','view_property'
    )


class LettingPictureAdmin(admin.ModelAdmin):
    list_display = ['property','caption']
    fields = ('property','caption','attachment','display_order','status')


class LettingMediaAdmin(admin.ModelAdmin):
    fields = ('property','media_type','description','attachment','status')
    list_display = ['property', 'media_type','description','status']


class LettingNoteAdmin(admin.ModelAdmin):
    fields = ('property','text')
    list_display = ['property']


admin.site.register(Letting, LettingAdmin)
admin.site.register(LettingFeature, LettingFeatureAdmin)
admin.site.register(LettingPicture, LettingPictureAdmin)
admin.site.register(LettingMedia, LettingMediaAdmin)
admin.site.register(LettingContact, LettingContactAdmin)
admin.site.register(LettingNote, LettingNoteAdmin)
