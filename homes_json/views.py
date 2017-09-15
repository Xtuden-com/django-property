import json

from googleplaces import GooglePlaces, types
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.shortcuts import get_object_or_404

from homes.models import SearchPrice
from homes_for_sale.forms import SaleContactForm
from homes_to_let.forms import LettingContactForm
from homes_for_sale.models import Sale, SaleFavourite
from homes_to_let.models import Letting, LettingFavourite


class SearchPriceView(View):
    def get(self, request, type):
        prices = SearchPrice.objects.filter(type=type)
        return HttpResponse(
            serializers.serialize('json', prices, fields=('label','price')),
            content_type='application/json'
        )


class SearchPlacesView(View):
    def get(self, request, name):
        places = GooglePlaces(settings.GOOGLE_MAPS_API_KEY)
        results = places.autocomplete(input=name,types=types.AC_TYPE_CITIES, components=[('country','gb')])
        return HttpResponse(
            json.dumps([prediction.description for prediction in results.predictions]),
            content_type='application/json'
        )


class ContactView(View):
    STATUS_FAILURE = 'failure'
    STATUS_SUCCESS = 'success'

    def __get_response_object(self, status, messages):
        return {'status':status, 'messages': messages}

    def __get_success_response_object(self, messages):
        return self.__get_response_object(self.STATUS_SUCCESS, messages)

    def __get_failure_response_object(self, messages):
        return self.__get_response_object(self.STATUS_FAILURE, messages)

    def __get_validation_failure_response_object(self, form):
        messages = []
        for key, errors in form.errors.items():
            for error in errors:
                messages.append({'name':key, 'label': error})
        return self.__get_response_object(self.STATUS_FAILURE, messages)

    def __get_single_message(self, label, name = ''):
        return [{'name':name, 'label':label}]

    def post(self, request, *args, **kwargs):
        contact_type = kwargs['type']
        form = SaleContactForm(request.POST) if contact_type == 'sale' else LettingContactForm(request.POST)
        message = {}
        if form.is_valid():
            if contact_type == 'sale':
                obj = Sale.filtered.published().unexpired().filter(slug=request.POST.get('property')).first()
            else:
                obj = Letting.filtered.published().unexpired().filter(slug=request.POST.get('property')).first()
            if obj:
                form.instance.property = obj
                if form.save():
                    message = self.__get_success_response_object([])
                else:
                    message = self.__get_failure_response_object(self.__get_single_message('Unable to save contact'))
            else:
                message = self.__get_failure_response_object(self.__get_single_message('Unable to find property'))
        else:
            message = self.__get_validation_failure_response_object(form)
        return HttpResponse(
            json.dumps(message),
            content_type='application/json'
        )

class FavouriteView(View):
    group_required = "general"
    STATUS_FAILURE = 'failure'
    STATUS_SUCCESS = 'success'

    def __create_letting_favourite(self, slug):
        letting = get_object_or_404(Letting, slug=slug)
        return LettingFavourite.objects.get_or_create(
            user=self.request.user,
            property=letting
        )

    def __create_sale_favourite(self, slug):
        sale = get_object_or_404(Sale, slug=slug)
        return SaleFavourite.objects.get_or_create(
            user=self.request.user,
            property=sale
        )

    def __delete_favourite(self, obj):
        obj.delete()

    def __get_single_message(self, status):
        return {'status':status}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if kwargs['type'] == 'sale':
                obj, created = self.__create_sale_favourite(kwargs['slug'])
            else:
                obj, created = self.__create_letting_favourite(kwargs['slug'])
            if not created:
                self.__delete_favourite(obj)
            return HttpResponse(
                json.dumps(self.__get_single_message(200)),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps(self.__get_single_message(403)),
                content_type='application/json'
            )
