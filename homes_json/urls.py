from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import SearchPriceView, SearchPlacesView, ContactView, FavouriteView

urlpatterns = [
    url(r'prices/(?P<type>1|2)/$', SearchPriceView.as_view(), name='search_prices'),
    url(r'places/(?P<name>\w+)/$', SearchPlacesView.as_view(), name='search_places'),
    url(r'contact/(?P<type>sale|letting)/$', csrf_exempt(ContactView.as_view()), name='contact'),
    url(r'favourite/(?P<type>sale|letting)/(?P<slug>[-\w]+)/$', csrf_exempt(FavouriteView.as_view()), name='favourite')
]
