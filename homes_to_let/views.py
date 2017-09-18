import urllib, hashlib
from urlparse import urlparse, parse_qsl

from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import HttpResponseRedirect, reverse, Http404
from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.measure import D
from django.conf import settings

from homes.forms import SearchForm
from homes.views import BaseSearchPageView
from .models import Letting, LettingFavourite
from .forms import LettingContactForm, LettingDistanceForm
from homes.models import Alert


class HomePageView(TemplateView):
    template_name = "homes-to-let-home.html"


class SearchPageView(BaseSearchPageView, ListView):
    template_name = "homes-to-let-search.html"
    form_class = SearchForm
    paginate_by = 9
    model = Letting

    def __get_point(self):
        try:
            return GEOSGeometry('POINT(%s %s)' % (self.request.GET.get('longitude'),self.request.GET.get('latitude')), srid=4326)
        except GEOSException as ex:
            super(SearchPageView,self).logger.error(ex)
            raise Http404('Location not found')

    def __get_alert_key(self):
        return hashlib.sha1(str(self.__get_request_items())).hexdigest()

    def __get_request_items(self):
        values = {}
        for key, value in self.request.GET.items():
            values[str(key)] = str(value)
        return values

    def __is_user_subscribed(self):
        return Alert.objects.filter(user=self.request.user, key=self.__get_alert_key()).exists()

    def get_queryset(self):
        lettings = Letting.filtered.published().unexpired()
        lettings = lettings.filter(
            rental__range=(
                self.request.GET.get('min_price',10000),
                self.request.GET.get('max_price',1000000)
            )
        )
        lettings = lettings.filter(bedrooms__gte=self.request.GET.get('min_bedrooms',0))
        lettings = lettings.filter(property_type__slug=self.request.GET.get('property_type','house'))
        lettings = lettings.filter(location__distance_lte=(self.__get_point(),D(mi=self.request.GET.get('distance',10))))
        lettings = lettings.order_by('-rental')        
        return lettings

    def get_context_data(self, **kwargs):
        context = super(SearchPageView, self).get_context_data(**kwargs)
        context['distance'] = LettingDistanceForm()
        if self.request.user.is_authenticated:
            context['subscribed'] = self.__is_user_subscribed()
        else:
            context['subscribed'] = False
        return context


class DetailPageView(BaseSearchPageView, DetailView):
    template_name = "homes-to-let-detail.html"
    form_class = SearchForm

    def __is_user_favourite(self):
        if self.request.user.is_authenticated and self.object:
            return LettingFavourite.objects.filter(user=self.request.user, property__slug=self.object.slug).exists()
        return False

    def get_context_data(self, **kwargs):
        context = super(DetailPageView, self).get_context_data(**kwargs)
        context['contact'] = LettingContactForm()
        context['favourited'] = self.__is_user_favourite()
        context['google'] = settings.GOOGLE_MAPS_API_KEY
        context['recaptcha'] = settings.RECAPTCHA_SITE_KEY
        return context

    def get_queryset(self):
        return Letting.filtered.published().unexpired()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj = queryset.filter(slug=self.kwargs['slug']).first()
        if obj is None:
            raise Http404('Letting matching query does not exist')
        return obj

class UpdateDistanceView(View):
    def __get_distance_params(self, form):
        url = urlparse(self.request.META.get('HTTP_REFERER'))
        params = dict(parse_qsl(url.query))
        params['distance'] = form.cleaned_data['distance']
        return params

    def post(self, request, *args, **kwargs):
        form = LettingDistanceForm(request.POST)
        if form.is_valid():
            params = self.__get_distance_params(form)
            return HttpResponseRedirect(reverse('lettings:search') + '?' + urllib.urlencode(params))
        else:
            raise Http404('Distance not chosen')
