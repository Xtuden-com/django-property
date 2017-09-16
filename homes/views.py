import geocoder
import logging

from registration.backends.hmac.views import RegistrationView
from django.views.generic import FormView
from django.shortcuts import HttpResponseRedirect, reverse
from django.http import QueryDict
from django.contrib.auth.models import Group

from .forms import SearchForm, CustomRegistrationForm
from homes_for_sale.models import Sale
from homes_to_let.models import Letting


class BaseSearchPageView(FormView):

    logger = logging.getLogger('app')

    def get_initial(self):
        initial = super(BaseSearchPageView, self).get_initial()
        if self.request.method == 'GET' and 'search_type' in self.request.GET:
            initial['search_type'] = self.request.GET['search_type']
            initial['location'] = self.request.GET['location']
            initial['min_price'] = self.request.GET['min_price']
            initial['max_price'] = self.request.GET['max_price']
            initial['min_bedrooms'] = self.request.GET['min_bedrooms']
            initial['property_type'] = self.request.GET['property_type']
        return initial

    def geocode_location(self, location):
        latlng = False
        try:
            google = geocoder.google(location)
            latlng = google.latlng
        except Exception as ex:
            self.logger.error(ex)
        return latlng

    def form_valid(self, form):
        latlng = self.geocode_location(form.cleaned_data['location'])
        if latlng:
            qs = QueryDict('', mutable=True)
            qs.update({
                'search_type': form.cleaned_data['search_type'],
                'min_price': form.cleaned_data['min_price'],
                'max_price': form.cleaned_data['max_price'],
                'location': form.cleaned_data['location'],
                'min_bedrooms': form.cleaned_data['min_bedrooms'],
                'property_type': form.cleaned_data['property_type'].slug,
                'latitude': latlng[0],
                'longitude': latlng[1],
                'distance': 10
            })
            if form.cleaned_data['search_type'] == 'lettings':
                return HttpResponseRedirect(reverse('lettings:search') + '?' + qs.urlencode())
            else:
                return HttpResponseRedirect(reverse('sales:search') + '?' + qs.urlencode())
        else:
            return HttpResponseRedirect('/search/error')


class HomePageView(BaseSearchPageView):
    template_name = "home.html"
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest'] = {
            'sale': Sale.filtered.published().unexpired().order_by('-created_at')[:6],
            'let': Letting.filtered.published().unexpired().order_by('-created_at')[:6]
        }
        return context

class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm

    def __get_group(self):
        try:
            group = Group.objects.get(name='general')
        except:
            group = False
        return group

    def register(self, request, **kwargs):
        user = super(CustomRegistrationView, self).register(request, **kwargs)
        group = self.__get_group()
        if group:
            user.groups.add(group)
            user.save